import datetime
from math import ceil

import pytest

from cbpro.utils import get_time_intervals, get_intervals, time_interval_ok, dt_string_to_datetime


def test_window_size_ok():
    """Test if the [start, end] time interval is larger than the interval_length or not.

    The test time interval is 10 seconds, for interval_length below 10 the function
    should return false, for 10 or more seconds it should return true
    """
    # arrange
    start = datetime.datetime(2021, 1, 1, 0, 0, 0)
    end = datetime.datetime(2021, 1, 1, 0, 0, 10)

    # act / assert
    assert time_interval_ok(start=start, end=end, interval_length=1) is False
    assert time_interval_ok(start=start, end=end, interval_length=10) is True
    assert time_interval_ok(start=start, end=end, interval_length=20) is True


@pytest.mark.parametrize('interval_length', [*range(1, 101)])
def test_get_intervals(interval_length):
    """Test that the [start, end] time interval is split into parts of length interval_length."""
    # arrange
    start = datetime.datetime(2021, 1, 1, 0, 0, 0)
    end = datetime.datetime(2021, 1, 1, 0, 1, 40)
    total_interval_length = (end - start).total_seconds()

    # act
    result = get_intervals(start=start, end=end, interval_length=interval_length)

    # assert
    assert len(result) == ceil(total_interval_length / interval_length)
    assert all(start <= entry[0] <= end for entry in result)
    assert all(start <= entry[1] <= end for entry in result)


def test_get_time_intervals():
    # arrange
    granularity = 86400  # daily
    params_short_interval = {
        "start": datetime.datetime(2021, 1, 1, 0, 0, 0).isoformat(),
        "end": datetime.datetime(2021, 1, 1, 0, 1, 40).isoformat(),
        "granularity": granularity,
    }
    params_multiple_intervals = {
        "start": datetime.datetime(2020, 1, 1, 0, 0, 0).isoformat(),
        "end": datetime.datetime(2021, 1, 1, 0, 0, 0).isoformat(),
        "granularity": granularity,
    }

    # act
    results_short = get_time_intervals(params_short_interval)
    results_multiple = get_time_intervals(params_multiple_intervals)

    # assert
    assert results_short == [(datetime.datetime(2021, 1, 1, 0, 0), datetime.datetime(2021, 1, 1, 0, 1, 40))]
    assert results_multiple == [
        (datetime.datetime(2020, 3, 7, 0, 0), datetime.datetime(2021, 1, 1, 0, 0)),
        (datetime.datetime(2020, 1, 1, 0, 0), datetime.datetime(2020, 3, 7, 0, 0)),
    ]
