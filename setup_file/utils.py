from datetime import datetime


def date_string_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
