from typing import TypedDict, List, Any, Literal, Union, Dict
from typing_extensions import Required


CounterMetricValue = Union[int, float]
""" counter_metric_value. """



DistributionMetricValue = List[Union[int, float]]
""" distribution_metric_value. """



class GenericMetric(TypedDict, total=False):
    """ generic_metric. """

    version: Literal[2]
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
    tags: Required[Dict[str, str]]
    """ Required property """

    value: Required[Union["CounterMetricValue", "SetMetricValue", "DistributionMetricValue"]]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    mapping_meta: Required["_MappingMeta"]
    """ Required property """

    aggregation_option: str


SetMetricValue = List[int]
""" set_metric_value. """



_MappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""

