"""List all available tags in Dixa"""
from tools.utils import make_request


def list_tags(include_deactivated: bool = False, log=None) -> str:
    """
    List all available tags in Dixa.
    
    Args:
        include_deactivated: Whether to include deactivated tags (default: False)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the tags data
    """
    params = {
        "includeDeactivated": str(include_deactivated),
    }
    
    url = "https://dev.dixa.io/v1/tags"
    data = make_request("GET", url, params=params, log=log)
    return data

