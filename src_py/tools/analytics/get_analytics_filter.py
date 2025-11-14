"""Get possible values to be used with a given analytics filter attribute from Dixa"""
from typing import Optional
from tools.utils import make_request


def get_analytics_filter(
    filter_attribute: str,
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    Get possible values to be used with a given analytics filter attribute from Dixa.
    Filter attributes are not metric or record specific, so one filter attribute can be used
    with multiple metrics/records. When a filter value is not relevant for a specific metric/record,
    it is simply ignored.
    
    Args:
        filter_attribute: The filter attribute to get values for (e.g., 'agent_id', 'queue_id', 'channel')
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the filter values
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = f"https://dev.dixa.io/v1/analytics/filter/{filter_attribute}"
    data = make_request("GET", url, params=params, log=log)
    return data

