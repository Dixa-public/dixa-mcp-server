"""List all available analytics record IDs from Dixa"""
from typing import Optional
from tools.utils import make_request


def list_analytics_records(
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    List all available analytics record IDs from Dixa that can be used to fetch data in Get Metric Records Data.
    These records represent different types of data that can be queried.
    
    Args:
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the records data
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = "https://dev.dixa.io/v1/analytics/records"
    data = make_request("GET", url, params=params, log=log)
    return data

