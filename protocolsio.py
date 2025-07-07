import os
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("protocolsio")
PROTOCOLSIO_CLIENT_ACCESS_TOKEN = os.getenv("PROTOCOLSIO_CLIENT_ACCESS_TOKEN")
PROTOCOLSIO_API_URL = os.getenv("PROTOCOLSIO_API_URL")

async def get_protocolsio_resource(url: str) -> dict[str, Any] | None:
    """Fetch a resource from protocols.io API."""
    headers = {
        "Authorization": f"Bearer {PROTOCOLSIO_CLIENT_ACCESS_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.TimeoutException, json.JSONDecodeError) as e:
            print(f"Error fetching resource from {url}: {e}")
            return None

@mcp.tool()
async def get_profile() -> str:
    """Get user profile information from protocols.io."""
    url = f"{PROTOCOLSIO_API_URL}/session/profile"
    data = await get_protocolsio_resource(url)
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    mcp.run(transport='stdio')