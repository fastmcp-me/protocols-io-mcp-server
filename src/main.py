import os
import json
import uuid
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP(
    name="protocols-io-mcp-server",
    instructions="""This server provides access to protocols.io API."""
)
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

async def post_protocols_io_resource(url: str, data: dict) -> dict[str, Any] | None:
    """Post data to protocols.io API."""
    headers = {
        "Authorization": f"Bearer {PROTOCOLS_IO_CLIENT_ACCESS_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.TimeoutException, json.JSONDecodeError) as e:
            print(f"Error posting resource from {url}: {e}")
            return None

@mcp.tool()
async def get_profile() -> dict:
    """Get user profile information from protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v3/session/profile"
    response = await get_protocols_io_resource(url)
    return response

@mcp.tool()
async def create_protocol() -> dict:
    """Create a new protocol on protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v3/protocols/{uuid.uuid4().hex}"
    data = {
        "type_id": 1,
    }
    response = await post_protocols_io_resource(url, data)
    return response

if __name__ == "__main__":
    mcp.run(transport='stdio')