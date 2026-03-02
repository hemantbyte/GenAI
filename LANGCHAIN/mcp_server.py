from dotenv import load_dotenv
import os
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get

# load environment variables
load_dotenv()

# create the MCP server instance with a name
mcp = FastMCP(name="MCP Server")

# create Tavily web search client
ClientTavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 🛠️ Tool: web_search
@mcp.tool()
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for the given query and return the results."""
    return ClientTavily.search(query=query, num_results=5)

# 📂 Resource: GitHub repo files
@mcp.resource("urn:github_repo_files")
def github_repo_files() -> Dict[str, Any]:
    """Provide access to the files in the langchain-ai repository."""
    url = "https://raw.githubusercontent.com/hemantbyte/GenAI/main/LANGCHAIN/README.md"
    try:
        response = get(url)
        return response.text
    except Exception as e:
        return {"error": f"Error fetching repo files: {str(e)}"}

# 📝 Prompt template
@mcp.prompt()
def prompt():
    return """
You are a helpful assistant about LangChain, LangGraph and LangSmith.

Use:
- web_search for general web queries.
- github_repo_files to read the GitHub README.

Answer questions clearly.
"""

# 🏁 Run the server with stdio transport
# if __name__ == "__main__":
#     print("Starting LangChain MCP server (stdio)…")
#     mcp.run(transport="stdio")

# 🏁 Run the server with streamable HTTP transport
if __name__ == "__main__":
    print("Starting MCP server (streamable HTTP)…")
    mcp.run(
        transport="http",     # streamable HTTP
        host="0.0.0.0",        # network bind
        port=8000              # chosen port
    )