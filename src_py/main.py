"""
Dixa MCP Server - Python implementation for FastMCP Cloud
"""
import os
from fastmcp import FastMCP

# Import all tools
from tools.conversations import (
    search_conversations,
    get_conversation,
    get_conversation_messages,
    get_conversation_notes,
    get_conversation_ratings,
)
from tools.tags import (
    list_tags,
    tag_conversation,
    remove_conversation_tag,
    get_conversation_tags,
)
from tools.users import (
    get_end_user,
    get_end_user_conversations,
)
from tools.agents import (
    get_agent,
    list_agents,
)
from tools.analytics import (
    get_analytics_metric,
    get_analytics_record,
    list_analytics_records,
    list_analytics_metrics,
    get_analytics_filter,
    get_analytics_records_data,
    get_analytics_metrics_data,
)
from tools.info import (
    get_api_info,
)

# Create the FastMCP server
mcp = FastMCP("Dixa MCP Server")

# Register conversation tools
mcp.tool()(search_conversations)
mcp.tool()(get_conversation)
mcp.tool()(get_conversation_messages)
mcp.tool()(get_conversation_notes)
mcp.tool()(get_conversation_ratings)

# Register tag tools
mcp.tool()(list_tags)
mcp.tool()(tag_conversation)
mcp.tool()(remove_conversation_tag)
mcp.tool()(get_conversation_tags)

# Register user tools
mcp.tool()(get_end_user)
mcp.tool()(get_end_user_conversations)

# Register agent tools
mcp.tool()(get_agent)
mcp.tool()(list_agents)

# Register analytics tools
mcp.tool()(get_analytics_metric)
mcp.tool()(get_analytics_record)
mcp.tool()(list_analytics_records)
mcp.tool()(list_analytics_metrics)
mcp.tool()(get_analytics_filter)
mcp.tool()(get_analytics_records_data)
mcp.tool()(get_analytics_metrics_data)

# Register info tools
mcp.tool()(get_api_info)

if __name__ == "__main__":
    mcp.run()

