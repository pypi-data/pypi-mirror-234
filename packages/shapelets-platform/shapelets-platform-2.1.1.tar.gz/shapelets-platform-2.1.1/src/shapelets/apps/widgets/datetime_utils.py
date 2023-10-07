from datetime import date, datetime, time
from typing import Union, Tuple

"""
Utils to deal with datetime inputs.
"""


def _date_to_string(given_date: Union[float, int, str, date, time]) -> str:
    """
    Convert the given data into YYYY-MM-DD format and return it as string.
    param given_date: date to be converted
    return date in string format
    """
    if isinstance(given_date, str):
        try:
            datetime.strptime(given_date, '%Y-%m-%d')
            return given_date
        except ValueError:
            raise ValueError("Incorrect date format, use YYYY-MM-DD for strings")
    elif isinstance(given_date, date):
        return given_date.isoformat()
    elif isinstance(given_date, (float, int)):
        try:
            return datetime.fromtimestamp(given_date).strftime('%Y-%m-%d')
        except:
            raise ValueError("Incorrect date format. Wrong float or int")
    else:
        raise ValueError(f"Unexpected type {type(given_date)}.")


def _transform_date_time_value(date_time: Union[float, int, str, datetime, date, time]) -> Tuple:
    """
    Given a datetime value, return its value as string and date format.
    """
    if isinstance(date_time, datetime):
        if date_time.tzinfo is not None and date_time.tzinfo.utcoffset(date_time) is not None:
            return date_time.strftime("%Y-%m-%d %H:%M:%S.%f %z"), 'YYYY-MM-DD HH:mm:ss TZ'

        else:
            return date_time.strftime("%Y-%m-%d %H:%M:%S"), 'YYYY-MM-DD HH:mm:ss'

    elif isinstance(date_time, date):
        return date_time.strftime("%Y-%m-%d"), 'YYYY-MM-DD'

    elif isinstance(date_time, time):
        if date_time.tzinfo is not None and date_time.tzinfo.utcoffset(None) is not None:
            return date_time.strftime("%H:%M:%S.%f %z"), 'HH:mm:ss TZ'
        else:
            return date_time.strftime("%H:%M:%S"), 'HH:mm:ss'

    elif isinstance(date_time, str):
        return _validate_datetime(date_time)

    elif isinstance(date_time, (int, float)):
        try:
            return datetime.fromtimestamp(date_time).strftime('%Y-%m-%d %H:%M:%S'), 'YYYY-MM-DD HH:mm:ss'
        except:
            raise ValueError("Incorrect date format. Wrong float or int")

    else:
        raise ValueError(f"Unexpected type {type(date_time)} in date input")


def _check_datetime_aware(input_date: str) -> Tuple:
    """
    Looks for datetime format with timezone YYYY-MM-DD hh:mm:ss TZ
    """
    try:
        datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S.%f %z')
        return input_date, 'YYYY-MM-DD HH:mm:ss TZ'

    except:
        try:
            datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S.%f%z')
            return input_date, 'YYYY-MM-DD HH:mm:ss TZ'
        except:
            return None


def _check_datetime(input_date: str) -> Tuple:
    """
    Looks for datetime format YYYY-MM-DD hh:mm:ss
    """
    try:
        datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
        return input_date, 'YYYY-MM-DD HH:mm:ss'
    except:
        try:
            datetime.strptime(input_date, '%Y-%m-%d %I:%M:%S %p')
            return input_date[:len(input_date) - 3], 'YYYY-MM-DD h:mm:ss a'
        except:
            return None


def _check_date(input_date: str) -> Tuple:
    """
    Looks for date format YYYY-MM-DD
    """
    try:
        datetime.strptime(input_date, '%Y-%m-%d').date()
        return input_date, 'YYYY-MM-DD'
    except:
        return None


def _check_time(input_date: str) -> Tuple:
    """
    Looks for time format hh:mm:ss
    """
    try:
        datetime.strptime(input_date, '%H:%M:%S').time()
        return input_date, 'HH:mm:ss'
    except:
        try:
            datetime.strptime(input_date, '%I:%M:%S %p').time()
            return input_date.time()[:len(input_date) - 3], 'h:mm:ss a'
        except:
            return None


def _validate_datetime(input_date: str) -> Tuple:
    """
    Go through different date formats to find a match for the given input date.
    Returns a tuple with the date and its format.
    """
    datetime_str = _check_datetime_aware(input_date)
    if datetime_str is None:
        datetime_str = _check_datetime(input_date)
        if datetime_str is None:
            datetime_str = _check_date(input_date)
            if datetime_str is None:
                datetime_str = _check_time(input_date)
                if datetime_str is None:
                    raise ValueError("Incorrect date format")
    return datetime_str
