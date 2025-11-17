# Dixa MCP Server - Python Implementation

This is the Python implementation of the Dixa MCP Server, designed to be deployed on FastMCP Cloud.

## Structure

```
src_py/
├── main.py                 # Main FastMCP server entry point
├── requirements.txt        # Python dependencies
├── tools/
│   ├── __init__.py
│   ├── utils.py           # Shared utility functions for API calls
│   ├── conversations/     # Conversation management tools
│   ├── tags/              # Tag management tools
│   ├── users/             # End user management tools
│   ├── agents/            # Agent management tools
│   ├── analytics/         # Analytics tools
│   └── info/              # Information and diagnostic tools
└── README.md
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variable:
```bash
export DIXA_API_KEY=your_api_key_here
```

## Running Locally

```bash
python main.py
```

## Deployment to FastMCP Cloud

1. Push your code to a GitHub repository
2. Sign in to [FastMCP Cloud](https://gofastmcp.com/deployment/fastmcp-cloud) with your GitHub account
3. Create a new project and link it to your repository
4. Set the entry point to `main.py` (or `src_py/main.py` if your repo root is different)
5. Set the `DIXA_API_KEY` environment variable in the FastMCP Cloud dashboard
6. Deploy!

## Tools

All tools from the TypeScript version are implemented:

### Conversation Management
- `searchConversations`: Search conversations in Dixa with pagination support
- `getConversation`: Get a single conversation by ID
- `getConversationMessages`: Get all messages for a specific conversation
- `getConversationTags`: Get all tags associated with a conversation
- `getConversationNotes`: Get all internal notes for a conversation
- `getConversationRatings`: Get all ratings for a conversation

### Tag Management
- `listTags`: List all available tags in Dixa
- `tagConversation`: Add a tag to a specific conversation
- `removeConversationTag`: Remove a tag from a specific conversation

### End User Management
- `getEndUser`: Get information about a specific end user
- `getEndUserConversations`: Get all conversations for a specific end user

### Agent Management
- `getAgent`: Get information about a specific agent
- `listAgents`: List all agents with optional filtering

### Analytics
- `getAnalyticsMetric`: Get detailed information about a specific analytics metric
- `getAnalyticsRecord`: Get detailed information about a specific analytics record
- `listAnalyticsRecords`: List all available analytics record IDs
- `listAnalyticsMetrics`: List all available analytics metric IDs
- `getAnalyticsFilter`: Get possible values for a given analytics filter attribute
- `getAnalyticsRecordsData`: Get analytics data for a specific record with filters and period settings
- `getAnalyticsMetricsData`: Get analytics data for a specific metric with filters, period settings, and aggregations

### Information & Diagnostics
- `getApiInfo`: Preview the configured DIXA_API_KEY (masked) and get information about the associated organization

