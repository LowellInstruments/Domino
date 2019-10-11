from math import isclose


sensor_precision = {
    'Ax (g)': 0.01,
    'Ay (g)': 0.01,
    'Az (g)': 0.01,
    'Mx (mG)': 1,
    'My (mG)': 1,
    'Mz (mG)': 1,
    'Yaw (degrees)': 1,
    'Pitch (degrees)': 1,
    'Roll (degrees)': 1,
    'Temperature (C)': 0.01,
    'Heading (degrees)': 0.5
}



def compare_files(path1, path2):
    with open(path1, 'r') as fid1, open(path2, 'r') as fid2:
        assert isclose(_n_lines(fid1), _n_lines(fid2), rel_tol=0.05)
        columns_1 = fid1.readline()
        columns_2 = fid2.readline()
        assert columns_1 == columns_2
        _values_are_close(columns_1.strip().split(','), zip(fid1, fid2))


def _n_lines(fid):
    count = sum([1 for line in fid])
    fid.seek(0)
    return count


def _values_are_close(columns, zip_obj):
    row_count = 0
    legacy_check = False
    time_fields = 1
    for rows in zip_obj:
        file1 = rows[0].strip().split(',')
        file2 = rows[1].strip().split(',')
        if not legacy_check:
            if len(file1) >= 2 and ':' in file1[1]:
                time_fields = 2
                legacy_check = True

        for i in range(time_fields):
            try:
                assert file1[i] == file2[i]
            except:
                raise AssertionError(file1[i], file2[i])

        for i in range(time_fields, min(len(file1), len(file2))):
            try:
                assert isclose(float(file1[i]), float(file2[i]), abs_tol=sensor_precision[columns[i]])
            except AssertionError:
                raise AssertionError(float(file1[i]), float(file2[i]))
        row_count += 1
