# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

"""
filewriter facilitates the writing of a data page to a datafile
The various formats subclass OutFile
"""

import datetime
import h5py
from os import path
import numpy as np


class OutFile:
    def set_datetime_format(self, datetime_format):
        if datetime_format.lower() == 'iso8601':
            self.datetime_format = '%Y-%m-%dT%H:%M:%S.%f'
            self.datetime_header = 'ISO 8601 Time'
        elif datetime_format == 'legacy':
            self.datetime_format = '%Y-%m-%d,%H:%M:%S.%f'
            self.datetime_header = 'Date,Time'
        else:
            raise ValueError('Unknown date format')

    def create_datasets(self, orient_time, accelerometer, magnetometer, current, temperature_time, temperature,
                        light, pressure_time, pressure):
        """
        abstract method. Implement for specific file type
        """
        pass

    def write_data(self, orient_time=None, accelerometer=None, magnetometer=None, current=None,
                   temperature_time=None, temperature=None, light=None,
                   pressure_time=None, pressure=None):
        pass


class Csv:
    def __init__(self, prefix, out_path, time_format):
        self.prefix = prefix
        self.out_path = out_path
        self.time_format = time_format

        self.orient_file = None
        self.current_file = None
        self.bearing_file = None
        self.temperature_file = None
        self.light_file = None
        self.pressure_file = None

        self.start_time = None
        self.is_first_page = True

    def _create_datasets(self, orient_time, accelerometer, magnetometer, current, temperature_time, temperature,
                         light, pressure_time, pressure, bearing):
        time_header = self.make_time_header()
        if accelerometer is not None or magnetometer is not None:
            self.orient_file = path.join(self.out_path, self.prefix + '_accelmag.csv')
            with open(self.orient_file, 'w') as fid:
                fid.write(time_header)
                if accelerometer is not None:
                    fid.write(',Ax (g),Ay (g),Az (g)')
                if magnetometer is not None:
                    fid.write(',Mx (mG),My (mG),Mz (mG)')
                fid.write('\n')
        if current is not None:
            self.current_file = path.join(self.out_path, self.prefix + '_current.csv')
            with open(self.current_file, 'w') as fid:
                fid.write('{},Speed (cm/s),Bearing (degrees),Velocity-N (cm/s),Velocity-E (cm/s)\n'.
                          format(time_header))
        if bearing is not None:
            self.bearing_file = path.join(self.out_path, self.prefix + '_bearing.csv')
            with open(self.bearing_file, 'w') as fid:
                fid.write('{},Bearing (degrees)\n'.format(time_header))
        if temperature is not None:
            self.temperature_file = path.join(self.out_path, self.prefix + '_temperature.csv')
            with open(self.temperature_file, 'w') as fid:
                fid.write('{},Temperature (C)\n'.format(time_header))
        if light is not None:
            self.light_file = path.join(self.out_path, self.prefix + '_light.csv')
            with open(self.light_file, 'w') as fid:
                fid.write('{},Light (%)\n'.format(time_header))
        if pressure is not None:
            self.pressure_file = path.join(self.out_path, self.prefix + '_pressure.csv')
            with open(self.pressure_file, 'w') as fid:
                fid.write('{},Pressure (psi)\n'.format(time_header))

    def write_data(self, orient_time=None, accelerometer=None, magnetometer=None, current=None,
                   temperature_time=None, temperature=None, light=None,
                   pressure_time=None, pressure=None, bearing=None):
        # Create the data sets if they haven't been already
        if self.is_first_page:
            self.start_time = np.min([start_time[0] for start_time in [orient_time, temperature_time, pressure_time]
                                      if start_time is not None])
            self._create_datasets(orient_time, accelerometer, magnetometer, current, temperature_time, temperature,
                                  light, pressure_time, pressure, bearing)
            self.is_first_page = False

        if accelerometer is not None or magnetometer is not None:
            accel_length = accelerometer.shape[1] if accelerometer is not None else 0
            mag_length = magnetometer.shape[1] if magnetometer is not None else 0
            orient_length = max(accel_length, mag_length)
            with open(self.orient_file, 'a') as fid:
                for i in range(orient_length):
                    time = self.make_time_string(orient_time[i])
                    fid.write('{}'.format(time))
                    if accelerometer is not None:
                        fid.write(',{:0.4f},{:0.4f},{:0.4f}'.format(*accelerometer[:, i]))
                    if magnetometer is not None:
                        fid.write(',{:0.2f},{:0.2f},{:0.2f}'.format(*magnetometer[:, i]))
                    fid.write('\n')

        if temperature is not None:
            with open(self.temperature_file, 'a') as fid:
                for i in range(temperature.shape[0]):
                    time = self.make_time_string(temperature_time[i])
                    fid.write('{}'.format(time))
                    fid.write(',{:0.4f}\n'.format(temperature[i]))

        if current is not None:
            with open(self.current_file, 'a') as fid:
                for i in range(current.shape[1]):
                    time = self.make_time_string(orient_time[i])
                    fid.write('{},{:0.2f},{:0.2f},{:0.2f},{:0.2f}\n'.format(time, *current[:, i]))

        if bearing is not None:
            with open(self.bearing_file, 'a') as fid:
                for i in range(bearing.shape[0]):
                    time = self.make_time_string(orient_time[i])
                    fid.write('{},{:0.2f}\n'.format(time, bearing[i]))

        if light is not None:
            with open(self.light_file, 'a') as fid:
                for i in range(light.shape[0]):
                    time = self.make_time_string(temperature_time[i])
                    fid.write('{},{:0.1f}\n'.format(time, light[i]))

        if pressure is not None:
            with open(self.pressure_file, 'a') as fid:
                for i in range(pressure.shape[0]):
                    time = self.make_time_string(pressure_time[i])
                    fid.write('{},{:0.2f}\n'.format(time, pressure[i]))

    def make_time_string(self, posix_time):
        """ Create a time string based on self.time_format """
        # The float functions converts the value from a np array to a python float
        # without it the number in the output file is in square braces
        if self.time_format == 'iso8601':
            return datetime.datetime.utcfromtimestamp(float(posix_time)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        elif self.time_format == 'legacy':
            return datetime.datetime.utcfromtimestamp(float(posix_time)).strftime('%Y-%m-%d,%H:%M:%S.%f')[:-3]
        elif self.time_format == 'elapsed':
            return '{:.3f}'.format(float(posix_time - self.start_time))
        elif self.time_format == 'posix':
            return '{:.3f}'.format(float(posix_time))

    def make_time_header(self):
        if self.time_format == 'iso8601':
            return 'ISO 8601 Time'
        elif self.time_format == 'legacy':
            return 'Date,Time'
        elif self.time_format == 'elapsed':
            return 'Elapsed Time (s)'
        elif self.time_format == 'posix':
            return 'POSIX Time (s)'

class Hdf5:
    def __init__(self, prefix, out_path, time_format):
        self.prefix = prefix
        self.out_path = out_path
        self.time_format = time_format
        self.start_time = None
        self.is_first_page = True

    def _create_datasets(self, orient_time, accelerometer, magnetometer, current, temperature_time, temperature,
                         light, pressure_time, pressure, bearing):

        with h5py.File(path.join(self.out_path, self.prefix + '.hdf5'), 'w') as hdf_file:
            if orient_time is not None:
                hdf_file.create_dataset('orient_time', (0,), maxshape=(None,), dtype='float64', compression='gzip')

            if accelerometer is not None:
                 hdf_file.create_dataset('accelerometer', (3, 0), maxshape=(3, None), dtype='float32', compression='gzip')

            if magnetometer is not None:
                hdf_file.create_dataset('magnetometer', (3, 0), maxshape=(3, None), dtype='float32', compression='gzip')

            if current is not None:
                hdf_file.create_dataset('current', (4, 0), maxshape=(4, None), dtype='float32', compression='gzip')

            if temperature_time is not None:
                hdf_file.create_dataset('temperature_time', (0,), maxshape=(None,), dtype='float64', compression='gzip')

            if temperature is not None:
                hdf_file.create_dataset('temperature', (0,), maxshape=(None,), dtype='float32', compression='gzip')

            if light is not None:
                hdf_file.create_dataset('light', (0,), maxshape=(None,), dtype='float32', compression='gzip')

            if pressure_time is not None:
                hdf_file.create_dataset('pressure_time', (0,), maxshape=(None,), dtype='float64', compression='gzip')

            if pressure is not None:
                hdf_file.create_dataset('pressure', (0,), maxshape=(None,), dtype='float32', compression='gzip')

            if bearing is not None:
                hdf_file.create_dataset('bearing', (0,), maxshape=(None,), dtype='float32', compression='gzip')

    def write_data(self, orient_time=None, accelerometer=None, magnetometer=None, current=None,
                   temperature_time=None, temperature=None, light=None,
                   pressure_time=None, pressure=None, bearing=None):
        # Create the data sets if they haven't been already
        if self.is_first_page:
            self.start_time = np.min([start_time[0] for start_time in [orient_time, temperature_time, pressure_time]
                                      if start_time is not None])
            self._create_datasets(orient_time, accelerometer, magnetometer, current, temperature_time, temperature,
                                  light, pressure_time, pressure, bearing)
            self.is_first_page = False

        with h5py.File(path.join(self.out_path, self.prefix + '.hdf5'), 'a') as hdf_file:
            if orient_time is not None:
                data_length = orient_time.shape[0]
                dset_length = hdf_file['orient_time'].shape[0]
                hdf_file['orient_time'].resize((dset_length + data_length,))
                hdf_file['orient_time'][dset_length:dset_length + data_length] = orient_time

            if accelerometer is not None:
                data_length = accelerometer.shape[1]
                dset_length = hdf_file['accelerometer'].shape[1]
                hdf_file['accelerometer'].resize((3, dset_length + data_length))
                hdf_file['accelerometer'][:, dset_length:dset_length + data_length] = accelerometer

            if magnetometer is not None:
                data_length = magnetometer.shape[1]
                dset_length = hdf_file['magnetometer'].shape[1]
                hdf_file['magnetometer'].resize((3, dset_length + data_length))
                hdf_file['magnetometer'][:, dset_length:dset_length + data_length] = magnetometer

            if current is not None:
                data_length = current.shape[1]
                dset_length = hdf_file['current'].shape[1]
                hdf_file['current'].resize((4, dset_length + data_length,))
                hdf_file['current'][:, dset_length:dset_length + data_length] = current

            if bearing is not None:
                data_length = bearing.shape[0]
                dset_length = hdf_file['bearing'].shape[0]
                hdf_file['bearing'].resize((dset_length + data_length,))
                hdf_file['bearing'][dset_length:dset_length + data_length] = bearing

            if temperature_time is not None:
                data_length = temperature_time.shape[0]
                dset_length = hdf_file['temperature_time'].shape[0]
                hdf_file['temperature_time'].resize((dset_length + data_length,))
                hdf_file['temperature_time'][dset_length:dset_length + data_length] = temperature_time

            if temperature is not None:
                data_length = temperature.shape[0]
                dset_length = hdf_file['temperature'].shape[0]
                hdf_file['temperature'].resize((dset_length + data_length,))
                hdf_file['temperature'][dset_length:dset_length + data_length] = temperature

            if light is not None:
                data_length = light.shape[0]
                dset_length = hdf_file['light'].shape[0]
                hdf_file['light'].resize((dset_length + data_length,))
                hdf_file['light'][dset_length:dset_length + data_length] = light

            if pressure_time is not None:
                data_length = pressure_time.shape[0]
                dset_length = hdf_file['pressure_time'].shape[0]
                hdf_file['pressure_time'].resize((dset_length + data_length,))
                hdf_file['pressure_time'][dset_length:dset_length + data_length] = pressure_time

            if pressure is not None:
                data_length = pressure.shape[0]
                dset_length = hdf_file['pressure'].shape[0]
                hdf_file['pressure'].resize((dset_length + data_length,))
                hdf_file['pressure'][dset_length:dset_length + data_length] = pressure
