from typing import TypedDict, List, Any, Dict
from typing_extensions import Required


class _Root(TypedDict, total=False):
    functions: Required[List[Dict[str, Any]]]
    """ Required property """

    environment: str
    profile_id: Required[str]
    """ Required property """

    platform: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    received: Required[int]
    """ Required property """

    release: str
    dist: str
    retention_days: Required[int]
    """ Required property """

    timestamp: Required[int]
    """ Required property """

    transaction_name: Required[str]
    """ Required property """

    transaction_op: Required[str]
    """ Required property """

    transaction_status: Required[str]
    """ Required property """

    http_method: str
    browser_name: str
    device_class: int
