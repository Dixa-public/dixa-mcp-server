"""Get analytics data for a specific metric from Dixa"""
from typing import Optional, List, Dict
from tools.utils import make_request


PERIOD_PRESETS = [
    "PreviousQuarter",
    "ThisWeek",
    "PreviousWeek",
    "Yesterday",
    "Today",
    "ThisMonth",
    "PreviousMonth",
    "ThisQuarter",
    "ThisYear",
]


def get_analytics_metrics_data(
    metric_id: str,
    period_filter: Dict[str, Dict[str, str]],
    aggregations: List[str],
    timezone: str,
    filters: Optional[List[Dict[str, List[str]]]] = None,
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    Call listAnalyticsMetrics before calling this endpoint to get the available metrics.
    Get analytics data for a specific metric with filters, period settings, and aggregations.
    This endpoint allows you to query analytics metrics data with custom filters, period settings,
    aggregations, and timezone.
    
    Args:
        metric_id: The ID of the metric to fetch data for (e.g., 'closed_conversations')
        period_filter: The period filter configuration using preset periods
            (dict with '_type': 'Preset' and 'value': {'_type': preset_name})
        aggregations: Array of aggregations to apply (e.g., ['Count'])
        timezone: The timezone to use for the data (e.g., 'Europe/Copenhagen') (required)
        filters: Array of filters to apply (each filter is a dict with 'attribute' and 'values')
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the analytics data
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = "https://dev.dixa.io/v1/analytics/metrics"
    
    json_data = {
        "id": metric_id,
        "periodFilter": period_filter,
        "aggregations": aggregations,
        "timezone": timezone,
    }
    
    if filters:
        json_data["filters"] = filters
    
    data = make_request("POST", url, params=params, json_data=json_data, log=log)
    return data

