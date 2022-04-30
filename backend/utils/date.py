from __future__ import annotations
from datetime import datetime, timezone


def date_time_to_timestamp(date_time: datetime):
    """
    Transforms a datetime object into a timestamp with 0 seconds and microseconds
    """
    date_time = date_time.replace(second=0, microsecond=0)
    return date_time.timestamp()


def purify_timestamp(timestamp: float) -> float:
    """
    Removes the seconds & the milliseconds from the input timestamp
    """

    date = datetime.utcfromtimestamp(timestamp)
    return date_time_to_timestamp(date)


def get_current_timestamp_with_null_seconds():
    """
    Returns the current timestamp where seconds = 0 and microseconds = 0
    """

    now = datetime.now()
    return date_time_to_timestamp(now)


def seconds_to_hours(seconds: int):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if seconds >= 30:
        minutes += 1

    if hours > 0:
        return hours + round(minutes / 60, 2)

    return round(minutes / 60, 2)


def time_stamp_to_date_time(timestamp: int):
    """
    Returns a datetime object out of a timestamp
    """
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)


def timestamp_to_date_string(timestamp: float, date_format: str = "%Y-%m-%d %H:%M"):
    """
    Returns a string representing a timestamp in a particular format
    """

    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).strftime(date_format)
