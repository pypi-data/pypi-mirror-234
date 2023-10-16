import datetime
from typing import Optional
from typing import Tuple
from typing import Union

import pendulum
import pytimeparse
from google.protobuf import duration_pb2

from tecton_core.errors import TectonValidationError
from tecton_proto.data.feature_store_pb2 import FeatureStoreFormatVersion


def timedelta_to_duration(td: datetime.timedelta) -> pendulum.Duration:
    return pendulum.duration(days=td.days, seconds=td.seconds, microseconds=td.microseconds)


def proto_to_duration(proto_duration) -> pendulum.Duration:
    return timedelta_to_duration(proto_duration.ToTimedelta())


def assert_is_round_seconds(d: pendulum.Duration):
    if d % pendulum.Duration(seconds=1):
        raise ValueError(f"{d.in_words()} is not a round number of seconds")
    return d


def strict_pytimeparse(time_str: str) -> Union[int, float]:
    parsed = pytimeparse.parse(time_str)
    if parsed is None:
        raise TectonValidationError(f'Could not parse time string "{time_str}"')
    else:
        return parsed


def nanos_to_seconds(nanos: int) -> float:
    """
    :param nanos: Nanoseconds
    :return: Converts nanoseconds to seconds
    """
    return nanos / float(1e9)


def seconds_to_nanos(seconds: int) -> int:
    """
    :param seconds: Seconds
    :return: Converts seconds to nanoseconds
    """
    return int(seconds) * int(1e9)


def convert_timedelta_for_version(duration: datetime.timedelta, version: int) -> int:
    """
    Convert pendulum duration according to version
    VO -> Return Seconds
    V1 -> Return Nanoseconds
    :param duration: Pendulum Duration
    :param version: Feature Store Format Version
    :return:
    """
    assert duration.microseconds == 0
    interval = duration.total_seconds()
    if version == FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
        return int(interval)
    else:
        return int(seconds_to_nanos(interval))


def convert_proto_duration_for_version(duration: duration_pb2.Duration, version: int) -> int:
    return convert_timedelta_for_version(duration.ToTimedelta(), version)


def align_time_downwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    return datetime.datetime.utcfromtimestamp(time.timestamp() - excess_seconds)


def align_epoch_downwards(int_timestamp_col: int, window_size: int) -> int:
    return int_timestamp_col - (int_timestamp_col % window_size)


def align_time_upwards(time: datetime.datetime, alignment: datetime.timedelta) -> datetime.datetime:
    excess_seconds = time.timestamp() % alignment.total_seconds()
    offset = 0 if excess_seconds == 0 else alignment.total_seconds() - excess_seconds
    return datetime.datetime.utcfromtimestamp(time.timestamp() + offset)


def get_timezone_aware_datetime(time: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    """
    Check and get timezone aware datetime
    :param time: Time to convert to timezone aware
    """
    if time is None:
        return None
    if time.tzinfo is None:
        return time.replace(tzinfo=pendulum.timezone("UTC"))
    else:
        return time


def backfill_jobs_periods(
    start_time: datetime.datetime, end_time: datetime.datetime, interval: datetime.timedelta
) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Return a list of start/end tuples of size batch_schedule.
    For use of breaking up a large backfill window into incremental sizes.
    """
    jobs = []
    while start_time < end_time:
        jobs.append((start_time, start_time + interval))
        start_time = start_time + interval
    assert start_time == end_time, "Start and end times were not aligned to `interval`"
    return jobs
