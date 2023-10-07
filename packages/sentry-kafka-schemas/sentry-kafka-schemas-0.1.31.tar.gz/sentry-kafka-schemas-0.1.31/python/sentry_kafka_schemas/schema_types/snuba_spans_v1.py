from typing import Dict, Union, TypedDict
from typing_extensions import Required


class SpanEvent(TypedDict, total=False):
    """ span_event. """

    event_id: "_Uuid"
    organization_id: int
    project_id: Required[int]
    """ Required property """

    trace_id: Required["_Uuid"]
    """ Required property """

    span_id: Required[str]
    """
    The span ID is a unique identifier for a span within a trace. It is an 8 byte hexadecimal string.

    Required property
    """

    parent_span_id: str
    """ The parent span ID is the ID of the span that caused this span. It is an 8 byte hexadecimal string. """

    segment_id: str
    """ The segment ID is a unique identifier for a segment within a trace. It is an 8 byte hexadecimal string. """

    group_raw: str
    """ The raw group ID has from the root transaction. It is an 8 byte hexadecimal string. """

    profile_id: "_Uuid"
    is_segment: Required[bool]
    """
    Whether this span is a segment or not.

    Required property
    """

    start_timestamp_ms: Required[int]
    """
    The start timestamp of the span in milliseconds since epoch.

    Required property
    """

    duration_ms: Required[int]
    """
    The duration of the span in milliseconds.

    Required property
    """

    exclusive_time_ms: Required[int]
    """
    The exclusive time of the span in milliseconds.

    Required property
    """

    retention_days: Required[Union[int, None]]
    """ Required property """

    description: Union[str]
    tags: Union[Dict[str, str], None]
    """  Manual key/value tag pairs. """

    sentry_tags: "_SentryExtractedTags"


_SentryExtractedTags = Union["_SentryExtractedTagsAnyof0"]
""" Tags extracted by sentry. These are kept separate from customer tags """



_SentryExtractedTagsAnyof0 = TypedDict('_SentryExtractedTagsAnyof0', {
    'http.method': str,
    'action': str,
    'domain': str,
    'module': str,
    'group': str,
    'system': str,
    'status': str,
    'status_code': str,
    'transaction': str,
    'transaction.op': str,
    'op': str,
    'transaction.method': str,
}, total=False)


_Uuid = str
"""
minLength: 32
maxLength: 36
"""

