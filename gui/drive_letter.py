import wmi


def get_li_drive():
    device_id = None
    partition_name = None
    drive_letter_name = None

    for disk in wmi.WMI().Win32_DiskDrive():
        if '&VEN_LI&' in disk.PNPDeviceID:
            device_id = disk.DeviceID

    if device_id is not None:
        for d2p in wmi.WMI().Win32_DiskDriveToDiskPartition():
            if d2p.Antecedent.DeviceID == device_id:
                partition_name = d2p.Dependent.DeviceID

    if partition_name is not None:
        for p2ld in wmi.WMI().Win32_LogicalDiskToPartition():
            if p2ld.Antecedent.DeviceID == partition_name:
                drive_letter_name = p2ld.Dependent.DeviceID

    return drive_letter_name
