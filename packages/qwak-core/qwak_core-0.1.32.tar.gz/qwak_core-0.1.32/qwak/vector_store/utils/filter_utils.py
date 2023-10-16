from datetime import datetime, timezone
from typing import Any, Optional

from _qwak_proto.qwak.vectors.v1.filters_pb2 import AtomicLiteral as ProtoAtomicLiteral
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp


def transform(value: Any) -> ProtoAtomicLiteral:
    if isinstance(value, bool):
        return ProtoAtomicLiteral(bool_literal=value)
    elif isinstance(value, str):
        return ProtoAtomicLiteral(string_literal=value)
    elif isinstance(value, int):
        return ProtoAtomicLiteral(int_literal=value)
    elif isinstance(value, float):
        return ProtoAtomicLiteral(double_literal=value)
    elif isinstance(value, datetime):
        # Assuming that timestamp is a datetime
        return ProtoAtomicLiteral(timestamp_literal=_datetime_to_pts(value))
    else:
        raise ValueError(f"Unsupported data type: {type(value)}")


def _datetime_to_pts(dtime: Optional[datetime]) -> Optional[ProtoTimestamp]:
    """
    converts a python datetime to Protobuf Timestamp
    @param dtime: python datetime.datetime
    @return: if the input is None, returns None. else converts to proto timestamp in utc timezone
    """
    if not dtime:
        return None
    res: ProtoTimestamp = ProtoTimestamp()
    res.FromDatetime(dtime.replace(tzinfo=timezone.utc))
    return res
