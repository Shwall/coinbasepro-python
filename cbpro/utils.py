import datetime


def filter_empty(params: dict) -> dict:
    return dict((k, v) for k, v in params.items() if v is not None)


def get_time_intervals(params: dict):
    """Get all time intervals that allow querying of the coinbase pro api."""
    max_candles = 300
    interval_length = max_candles * params.get("granularity")
    start = datetime.datetime.fromisoformat(params.get("start"))
    end = datetime.datetime.fromisoformat(params.get("end"))

    if time_interval_ok(start, end, interval_length):
        return [(start, end)]

    return get_intervals(start, end, interval_length)


def get_intervals(start: datetime.datetime, end: datetime.datetime, interval_length: int):
    """Get all time intervals between start and end for the given interval_length.

    The function starts with the end of the time interval and goes back in interval_length steps to create all
    intervals.
    """
    start_init = start
    intervals = []
    start = end - datetime.timedelta(seconds=interval_length)
    while start >= start_init:
        start = end - datetime.timedelta(seconds=interval_length)
        if start <= start_init:
            intervals.append((start_init, end))
            break
        intervals.append((start, end))
        end = start
    return intervals


def time_interval_ok(start: datetime.datetime, end: datetime.datetime, interval_length: int):
    """Check if the [start, end] time interval is within the allowed interval_length."""
    return (end-start).total_seconds() <= interval_length
