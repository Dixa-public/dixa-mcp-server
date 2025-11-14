"""Get information about a specific agent from Dixa"""
from tools.utils import make_request


def get_agent(agent_id: str, log=None) -> str:
    """
    Get information about a specific agent from Dixa.
    
    Args:
        agent_id: The ID of the agent to fetch information for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the agent data
    """
    url = f"https://dev.dixa.io/v1/agents/{agent_id}"
    data = make_request("GET", url, log=log)
    return data

