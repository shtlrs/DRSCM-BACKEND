from datetime import datetime


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


def timestamp_to_date(timestamp: int, date_format: str = '%Y-%m-%d %H:%M'):
    """
    Returns a string representing a timestamp in a particular format
    """

    return datetime.utcfromtimestamp(timestamp).strftime(date_format)