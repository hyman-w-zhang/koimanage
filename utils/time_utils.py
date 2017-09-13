import datetime
import pytz

tz = pytz.timezone('Asia/Shanghai')


def milli_second_time_stamp_to_str(ts):
    return datetime.datetime.fromtimestamp(int(ts) / 1000, tz).strftime('%Y-%m-%d %H:%M:%S')


def datetime_str_to_milli_second_time_stamp(date_string, date_format='%Y-%m-%d %H:%M:%S'):
    return int(datetime.datetime.strptime(date_string, date_format).timestamp() * 1000)
