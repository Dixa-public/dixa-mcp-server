"""
Utility functions for Dixa API calls
"""
import os
import json
import requests
from typing import Dict, Any, Optional


def get_api_key() -> str:
    """Get the Dixa API key from environment variable."""
    api_key = os.getenv("DIXA_API_KEY")
    if not api_key:
        raise ValueError("DIXA_API_KEY environment variable is not set")
    return api_key


def make_request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    log=None,
) -> Dict[str, Any]:
    """
    Make an HTTP request to the Dixa API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Full URL to request
        params: Query parameters (for GET requests)
        json_data: JSON body (for POST/PUT requests)
        log: Optional logger for debugging
    
    Returns:
        Formatted JSON string
    """
    api_key = get_api_key()
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    
    if log:
        log.debug(f"Request {method} {url}")
        if json_data:
            log.debug(f"Request body: {json.dumps(json_data, indent=2)}")
    
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers=headers,
            timeout=30,
        )
        
        response_text = response.text
        
        if not response.ok:
            error_msg = (
                f"Failed to fetch data: {response.status_code} {response.reason}\n"
                f"Response: {response_text}"
            )
            raise Exception(error_msg)
        
        # Handle 204 No Content responses
        if response.status_code == 204:
            return json.dumps({"success": True, "message": "Operation completed successfully"}, indent=2)
        
        # Parse JSON response
        try:
            data = response.json()
            # Return as formatted JSON string for MCP
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from server: {response_text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

