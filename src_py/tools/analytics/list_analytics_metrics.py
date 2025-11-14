"""List all available analytics metric IDs from Dixa"""
from typing import Optional
from tools.utils import make_request


def list_analytics_metrics(
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    List all available analytics metric IDs from Dixa that can be used to fetch data in Get Metric Data.
    These metrics represent different types of measurements and analytics that can be queried.
    
    Args:
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the metrics data
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = "https://dev.dixa.io/v1/analytics/metrics"
    data = make_request("GET", url, params=params, log=log)
    return data

