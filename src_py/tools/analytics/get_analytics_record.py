"""Get detailed information about a specific analytics record from Dixa"""
from tools.utils import make_request


def get_analytics_record(record_id: str, log=None) -> str:
    """
    Get detailed information about a specific analytics record from Dixa.
    This endpoint lists all available properties of a record that can be used for querying its data.
    
    Args:
        record_id: The ID of the record to fetch information for (e.g., 'conversation')
        log: Optional logger for debugging
    
    Returns:
        JSON string of the record information
    """
    url = f"https://dev.dixa.io/v1/analytics/records/{record_id}"
    data = make_request("GET", url, log=log)
    return data

