from math import isclose


def compare_files(path1, path2):
    with open(path1, 'r') as fid1, open(path2, 'r') as fid2:
        assert _n_lines(fid1) == _n_lines(fid2)
        assert _n_columns(fid1) == _n_columns(fid2)
        _values_are_close(zip(fid1, fid2))


def _n_lines(fid):
    count = sum([1 for line in fid])
    fid.seek(0)
    return count


def _n_columns(fid):
    line = fid.readline()
    return len(line.split(','))


def _values_are_close(zip_obj):
    row_count = 0
    legacy_check = False
    time_fields = 1
    for rows in zip_obj:
        file1 = rows[0].strip().split(',')
        file2 = rows[1].strip().split(',')
        if not legacy_check:
            state = 'checked'
            if len(file1) >= 2 and ':' in file1[1]:
                time_fields = 2

        for i in range(time_fields, len(file1)):
            assert isclose(float(file1[i]), float(file2[i]), abs_tol=0.01)
        row_count += 1