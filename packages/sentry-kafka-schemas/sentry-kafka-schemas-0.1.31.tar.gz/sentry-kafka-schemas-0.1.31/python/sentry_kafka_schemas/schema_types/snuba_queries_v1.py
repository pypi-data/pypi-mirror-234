from typing import Dict, Any, TypedDict, List, Union
from typing_extensions import Required


class ClickhouseQueryProfile(TypedDict, total=False):
    """ clickhouse_query_profile. """

    time_range: Required[Union[int, None]]
    """ Required property """

    table: str
    all_columns: List[str]
    multi_level_condition: Required[bool]
    """ Required property """

    where_profile: Required["ClickhouseQueryProfileWhereProfile"]
    """ Required property """

    groupby_cols: Required[List[str]]
    """ Required property """

    array_join_cols: Required[List[str]]
    """ Required property """



class ClickhouseQueryProfileWhereProfile(TypedDict, total=False):
    """ clickhouse_query_profile_where_profile. """

    columns: Required[List[str]]
    """ Required property """

    mapping_cols: Required[List[str]]
    """ Required property """



class QueryMetadata(TypedDict, total=False):
    """ query_metadata. """

    sql: Required[str]
    """ Required property """

    sql_anonymized: Required[str]
    """ Required property """

    start_timestamp: Required[Union[int, None]]
    """ Required property """

    end_timestamp: Required[Union[int, None]]
    """ Required property """

    stats: Required["_QueryMetadataStats"]
    """ Required property """

    status: Required[str]
    """ Required property """

    trace_id: Required[Union[str, None]]
    """ Required property """

    profile: Required["ClickhouseQueryProfile"]
    """ Required property """

    result_profile: Required[Union[Dict[str, Any], None]]
    """ Required property """

    request_status: Required[str]
    """ Required property """

    slo: Required[str]
    """ Required property """



class Querylog(TypedDict, total=False):
    """
    querylog.

    Querylog schema
    """

    request: Required["_QuerylogRequest"]
    """ Required property """

    dataset: Required[str]
    """ Required property """

    entity: Required[str]
    """ Required property """

    start_timestamp: Required[Union[int, None]]
    """ Required property """

    end_timestamp: Required[Union[int, None]]
    """ Required property """

    status: Required[str]
    """ Required property """

    request_status: Required[str]
    """ Required property """

    slo: Required[str]
    """ Required property """

    projects: Required[List[int]]
    """ Required property """

    query_list: Required[List["QueryMetadata"]]
    """ Required property """

    timing: Required["TimerData"]
    """ Required property """

    snql_anonymized: str
    organization: Union[int, None]


class TimerData(TypedDict, total=False):
    """ timer_data. """

    timestamp: Required[int]
    """ Required property """

    duration_ms: Required[int]
    """ Required property """

    marks_ms: Dict[str, int]
    tags: Dict[str, str]


class _QueryMetadataStats(TypedDict, total=False):
    final: bool
    cache_hit: int
    sample: Union[Union[int, float], None]
    max_threads: int
    clickhouse_table: str
    query_id: str
    is_duplicate: int
    consistent: bool


class _QuerylogRequest(TypedDict, total=False):
    id: Required[str]
    """
    pattern: [0-9a-fA-F]{32}

    Required property
    """

    body: Dict[str, Any]
    referrer: str
    app_id: str
    team: Union[str, None]
    feature: Union[str, None]
