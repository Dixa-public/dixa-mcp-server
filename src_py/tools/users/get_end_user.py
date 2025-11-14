"""Get information about a specific end user from Dixa"""
from tools.utils import make_request


def get_end_user(user_id: str, log=None) -> str:
    """
    Get information about a specific end user from Dixa.
    
    Args:
        user_id: The ID of the end user to fetch information for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the user data
    """
    url = f"https://dev.dixa.io/v1/endusers/{user_id}"
    data = make_request("GET", url, log=log)
    return data

