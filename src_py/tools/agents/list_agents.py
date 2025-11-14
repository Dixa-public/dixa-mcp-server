"""List all agents from Dixa with optional filtering and pagination support"""
from typing import Optional
from tools.utils import make_request


def list_agents(page_limit: int = 50, log=None) -> str:
    """
    List all agents from Dixa to find the agent ID with optional filtering by email and phone, and pagination support.
    
    Args:
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the agents data
    """
    params = {}
    
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = "https://dev.dixa.io/v1/agents"
    data = make_request("GET", url, params=params, log=log)
    return data

