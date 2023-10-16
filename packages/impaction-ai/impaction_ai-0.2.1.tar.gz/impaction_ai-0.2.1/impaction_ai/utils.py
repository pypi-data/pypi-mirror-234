from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp


def datetime_to_timestamp(dt: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
