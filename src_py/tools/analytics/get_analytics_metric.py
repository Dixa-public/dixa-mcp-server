"""Get detailed information about a specific analytics metric from Dixa"""
from tools.utils import make_request


def get_analytics_metric(metric_id: str, log=None) -> str:
    """
    Get detailed information about a specific analytics metric from Dixa.
    This endpoint lists all available properties of a metric that can be used for querying its data.
    
    Args:
        metric_id: The ID of the metric to fetch information for (e.g., 'csat')
        log: Optional logger for debugging
    
    Returns:
        JSON string of the metric information
    """
    url = f"https://dev.dixa.io/v1/analytics/metrics/{metric_id}"
    data = make_request("GET", url, log=log)
    return data

