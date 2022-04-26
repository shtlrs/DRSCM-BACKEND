from datetime import datetime


def purify_timestamp(timestamp: int) -> int:
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


def date_time_to_timestamp(date_time: datetime):
    """
    Transforms a datetime object into a timestamp with 0 seconds and microseconds
    """
    date_time = date_time.replace(second=0, microsecond=0)
    return date_time.timestamp()


def timestamp_to_date_string(timestamp: int, date_format: str = "%Y-%m-%d %H:%M"):
    """
    Returns a string representing a timestamp in a particular format
    """

    return datetime.utcfromtimestamp(timestamp).strftime(date_format)
