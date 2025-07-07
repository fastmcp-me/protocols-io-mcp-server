import os
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("protocols-io")
PROTOCOLS_IO_CLIENT_ACCESS_TOKEN = os.getenv("PROTOCOLS_IO_CLIENT_ACCESS_TOKEN")
PROTOCOLS_IO_API_URL = os.getenv("PROTOCOLS_IO_API_URL")

async def get_protocols_io_resource(url: str) -> dict[str, Any] | None:
    """Fetch a resource from protocols.io API."""
    headers = {
        "Authorization": f"Bearer {PROTOCOLS_IO_CLIENT_ACCESS_TOKEN}"
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
    url = f"{PROTOCOLS_IO_API_URL}/session/profile"
    data = await get_protocols_io_resource(url)
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    mcp.run(transport='stdio')