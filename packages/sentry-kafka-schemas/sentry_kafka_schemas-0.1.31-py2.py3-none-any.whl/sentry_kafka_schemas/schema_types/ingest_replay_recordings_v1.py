from typing import Union, Literal, Any, TypedDict
from typing_extensions import Required


class ReplayRecording(TypedDict, total=False):
    """
    replay_recording.

    A replay recording, or a chunk thereof
    """

    type: Required[Literal["replay_recording_not_chunked"]]
    """ Required property """

    replay_id: Required[str]
    """ Required property """

    key_id: Union[None, int]
    org_id: Required[int]
    """
    minimum: 0

    Required property
    """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    received: Required[int]
    """
    minimum: 0

    Required property
    """

    retention_days: Required[int]
    """ Required property """

    payload: Required[Any]
    """
    msgpack bytes

    WARNING: we get an schema without any type

    Required property
    """

    version: int
    """ default: 0 """



_REPLAY_RECORDING_VERSION_DEFAULT = 0
""" Default value of the field path 'replay_recording version' """

