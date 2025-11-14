"""Get analytics data for a specific record from Dixa"""
from typing import Optional, Dict, List
from tools.utils import make_request


def get_analytics_records_data(
    record_id: str,
    period_filter: Dict[str, str],
    timezone: str,
    filters: Optional[Dict[str, List[str]]] = None,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
    log=None,
) -> str:
    """
    Get analytics data for a specific record from Dixa.
    
    Args:
        record_id: The ID of the record to fetch data for
        period_filter: Time period to fetch data for (dict with 'from' and 'to' ISO format dates)
        timezone: Timezone to use for the data (e.g., 'Europe/Copenhagen')
        filters: Optional filters to apply to the data (dict mapping attribute names to lists of values)
        page_key: Optional pagination key for fetching next page of results
        page_limit: Optional limit for number of results per page
        log: Optional logger for debugging
    
    Returns:
        JSON string of the analytics data
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = f"https://dev.dixa.io/v1/analytics/records/{record_id}/data"
    
    json_data = {
        "periodFilter": period_filter,
        "timezone": timezone,
    }
    
    if filters:
        json_data["filters"] = filters
    
    data = make_request("POST", url, params=params, json_data=json_data, log=log)
    return data

