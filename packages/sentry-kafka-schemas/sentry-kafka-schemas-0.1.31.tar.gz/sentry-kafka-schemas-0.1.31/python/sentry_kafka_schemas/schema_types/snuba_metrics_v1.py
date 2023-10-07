from typing import Any, Dict, Union, Literal, List, TypedDict
from typing_extensions import Required


CounterMetricValue = Union[int, float]
""" counter_metric_value. """



DistributionMetricValue = List[Union[int, float]]
""" distribution_metric_value. """



class Metric(TypedDict, total=False):
    """ metric. """

    version: Literal[1]
    use_case_id: Required[str]
    """ Required property """

    org_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    metric_id: Required[int]
    """ Required property """

    type: Required[str]
    """ Required property """

    timestamp: Required[int]
    """
    minimum: 0

    Required property
    """

    sentry_received_timestamp: Union[int, float]
    tags: Required["_IntToInt"]
    """ Required property """

    value: Required[Union["CounterMetricValue", "SetMetricValue", "DistributionMetricValue"]]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    mapping_meta: Required["_MappingMeta"]
    """ Required property """



SetMetricValue = List[int]
""" set_metric_value. """



_IntToInt = Dict[str, Any]
"""
patternProperties:
  ^[0-9]$:
    type: integer
"""



_MappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""

