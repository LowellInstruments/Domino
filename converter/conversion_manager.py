# GPLv3 License
# Copyright (c) 2018 Lowell Instruments, LLC, some rights reserved

from mat import odlfile, converter
from os import path
from converter import filewriter
import numpy as np
from mat.header import (
    IS_ACCELEROMETER,
    IS_MAGNETOMETER,
    IS_PHOTO_DIODE,
    IS_PRESSURE,
    IS_TEMPERATURE,
    ORIENTATION_BURST_COUNT,
)


MISSING_CONVERSION_ERROR = (
    'Accelerometer and magnetometer data are both required for current '
    'conversion')


class ConversionManager:
    def __init__(self, full_file_path, out_path=None, output_format='csv',
                 output_type='discrete', average=True,
                 tilt_curve=None, custom_calibration=None,
                 time_format='iso8601', declination=0, calibration=None):
        """
        If out_path is None, write output file same folder as input
        """
        self.full_file_path = full_file_path
        self.prefix = path.basename(full_file_path).split('.')[0]
        self.out_path = out_path if out_path else path.dirname(full_file_path)
        self.output_format = output_format
        self.output_type = output_type
        self.average = average
        self.tilt_curve = tilt_curve
        self.custom_calibration = custom_calibration
        self.time_format = time_format
        self.declination = declination
        self.calibration = calibration

        # Setup the file writer
        if output_format == 'csv':
            self.out_file = filewriter.Csv(self.prefix,
                                           self.out_path,
                                           time_format)
        elif output_format == 'hdf5':
            self.out_file = filewriter.Hdf5(self.prefix,
                                            self.out_path,
                                            time_format)
        else:
            raise(ValueError, 'Unknown output_format')

        self.observers = []
        self._is_running = True

    def add_observer(self, observer):
        self.observers.append(observer)

    def convert(self):
        orient_time, accelerometer, magnetometer, current, temperature_time, \
            temperature, light, pressure_time, pressure, bearing = (None,)*10

        with open(self.full_file_path, 'rb') as infile:
            odl = odlfile.load_file(infile)  # type: odlfile.OdlFile
            if self.calibration is not None:
                # If a host storage file was specified, use it
                conv = converter.Converter(self.calibration)
            else:
                # Otherwise use the factory host storage
                conv = converter.Converter(odl.calibration)

            bmn = odl.header.tag(ORIENTATION_BURST_COUNT)

            for i in range(odl.n_pages):
                if not self._is_running:
                    break
                odl.load_page(i)

                # TODO I *think* what I want to do here is if
                # averaging is enabled, average the channels first
                # here

                if odl.header.tag(IS_TEMPERATURE):
                    temperature_raw = odl.temperature()
                    temperature_raw[temperature_raw == 0] = 1
                    temperature = conv.temperature(temperature_raw)
                    shape_end = temperature.shape[0]
                    temperature_time = (
                        odl.page_start_times[i] +
                        odl.page_time_offset[odl.is_temp][:shape_end])

                if odl.header.tag(IS_PHOTO_DIODE):
                    light_raw = odl.light()
                    light = conv.light(light_raw)
                    temperature_time = (
                        odl.page_start_times[i] +
                        odl.page_time_offset[odl.is_light][:light.shape[0]])

                if odl.header.tag(IS_ACCELEROMETER):
                    accelerometer_raw = odl.accelerometer()
                    # make sure the length is n * bmn
                    orient_len = int(np.floor(accelerometer_raw.shape[1] /
                                              bmn) * bmn)
                    accelerometer_raw = accelerometer_raw[:, :orient_len]
                    orient_time = (
                        odl.page_start_times[i] +
                        odl.page_time_offset[odl.is_accel][::3][:orient_len])

                    if self.average:
                        accelerometer_raw = average_burst(accelerometer_raw,
                                                          bmn)
                        orient_time = orient_time[::bmn]

                    accelerometer = conv.accelerometer(accelerometer_raw)

                if odl.header.tag(IS_MAGNETOMETER):
                    magnetometer_raw = odl.magnetometer()
                    orient_len = int(
                        np.floor(magnetometer_raw.shape[1] / bmn) * bmn)
                    magnetometer_raw = magnetometer_raw[:, :orient_len]
                    orient_time = (
                        odl.page_start_times[i] +
                        odl.page_time_offset[odl.is_accel][::3][:orient_len])

                    if self.average:
                        magnetometer_raw = average_burst(magnetometer_raw, bmn)
                        orient_time = orient_time[::bmn]

                    magnetometer = conv.magnetometer(magnetometer_raw)

                if odl.header.tag(IS_PRESSURE):
                    pressure_raw = odl.pressure()
                    pressure = conv.pressure(pressure_raw)
                    pressure_time = (
                        odl.page_start_times[i] +
                        odl.page_time_offset[odl.is_pres][:len(pressure)])

                if self.output_type == 'current':
                    if accelerometer is None or magnetometer is None:
                        raise ValueError(MISSING_CONVERSION_ERROR)
                    current = self.tilt_curve.calc_current(accelerometer,
                                                           magnetometer,
                                                           self.declination)
                    accelerometer, magnetometer = None, None

                elif self.output_type == 'compass':
                    bearing = calc_compass(accelerometer,
                                           magnetometer,
                                           self.declination)
                    accelerometer, magnetometer = None, None

                self.out_file.write_data(orient_time, accelerometer,
                                         magnetometer, current,
                                         temperature_time, temperature, light,
                                         pressure_time, pressure, bearing)

                # If there is an observer, update the percent progress
                for observer in self.observers:
                    observer((i+1)/odl.n_pages*100)


def average_burst(data, bmn):
    intervals = int(data.shape[1] / bmn)
    data = np.stack(np.hsplit(data, intervals))
    data = np.transpose(np.mean(data, 2))
    return data


def calc_compass(accel, mag, declination=0):
    # The channels need to be adjusted because compass mode has the
    # logger horizontal, not vertical like current
    m = np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]])
    accel = np.dot(m, accel)
    mag = np.dot(m, mag)

    roll = np.arctan2(accel[1], accel[2])
    pitch = np.arctan2(-accel[0],
                       accel[1] * np.sin(roll) + accel[2] * np.cos(roll))
    by = mag[2] * np.sin(roll) - mag[1] * np.cos(roll)
    bx = (mag[1] * np.cos(pitch) +
          mag[1] * np.sin(pitch) * np.sin(roll) +
          mag[2] * np.sin(pitch) * np.cos(roll))

    heading = np.arctan2(by, bx)
    heading = np.rad2deg(heading)
    heading = np.mod(heading + declination, 360)
    return heading
