from datetime import datetime


def get_timestamp_with_null_seconds():
    """
    Returns a timestamp where seconds = 0 and microseconds = 0
    """

    now = datetime.now()
    now = now.replace(second=0, microsecond=0)
    return now.timestamp()
