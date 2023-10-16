import time
from datetime import datetime, timedelta
import pytz


def get_current_ist_timestamp():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist_timezone)

def get_todays_date():
    return get_current_ist_timestamp()

def get_current_time_millis():
    return int(time.time_ns() / 1000000)  # milli seconds

def readable_timestamp():
    return str(get_current_ist_timestamp().strftime('%Y-%m-%d %H:%M:%S'))


def readable_timestamp_till_hours():
    return str(get_current_ist_timestamp().strftime('%Y-%m-%d %H'))


def get_current_date_str():
    return str(get_current_ist_timestamp().strftime('%Y-%m-%d'))

def get_current_timestamp():
    return get_current_ist_timestamp()

def get_previous_date_str(date_str):
    datetime_object = datetime.strptime(date_str, "%Y-%m-%d")
    time_delta = timedelta(days=1)
    return str((datetime_object - time_delta).strftime('%Y-%m-%d'))


# Note: return the same timestamp for case where now() is perfect hour timestamp.
def get_last_perfect_hour_ts_str():
    current_time = get_current_ist_timestamp()
    rounded_time = current_time.replace(minute=0, second=0, microsecond=0)
    return str(rounded_time.strftime('%Y-%m-%d %H:%M:%S'))


# Note: It would exclude hours that are after now()
def get_all_perfect_hour_ts_today():
    # todo
    result = []
    now_datetime = get_current_ist_timestamp()
    current_hour = int(now_datetime.strftime('%H'))
    current_minute = int(now_datetime.strftime('%M'))
    current_second = int(now_datetime.strftime('%S'))
    end = current_hour - 1
    return result


def get_all_perfect_hour_ts(date_str):
    # todo
    date_format = "%Y-%m-%d"
    datetime_object = datetime.strptime(date_str, date_format)
    result = []
    for i in range(24):
        i_rounded = datetime_object.replace(hour=i, minute=0, second=0, microsecond=0)
        result.append(str(i_rounded.strftime('%Y-%m-%d %H:%M:%S')))
    return result


def is_perfect_hour_ts(timestamp_str):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    datetime_object = datetime.strptime(timestamp_str, datetime_format)
    return datetime_object.minute == 0 and datetime_object.second == 0 and datetime_object.microsecond == 0


def get_current_time_millis():
    return int(time.time_ns() / 1000000)  # milli seconds


def get_readable_timestamp():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return str(get_current_ist_timestamp().strftime('%Y-%m-%d %H:%M:%S'))


def get_ist_timestamp():
    return get_current_ist_timestamp()

def to_ist(utc_timestamp):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return utc_timestamp.astimezone(ist_timezone)
