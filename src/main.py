import os
import json
import uuid
import httpx
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP
from models import ProtocolStep
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP(
    name="protocols-io-mcp-server",
    instructions="""This server provides access to protocols.io API."""
)
PROTOCOLS_IO_CLIENT_ACCESS_TOKEN = os.getenv("PROTOCOLS_IO_CLIENT_ACCESS_TOKEN")
PROTOCOLS_IO_API_URL = os.getenv("PROTOCOLS_IO_API_URL")

async def get_protocols_io_resource(url: str) -> dict[str, Any]:
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
            return {
                "error": True,
                "message": f"Error fetching resourse: {e}",
                "url": url
            }

async def post_protocols_io_resource(url: str, data: dict) -> dict[str, Any]:
    """Post data to protocols.io API."""
    headers = {
        "Authorization": f"Bearer {PROTOCOLS_IO_CLIENT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.TimeoutException, json.JSONDecodeError) as e:
            return {
                "error": True,
                "message": f"Error posting resourse: {e}",
                "url": url
            }

async def put_protocols_io_resource(url: str, data: dict) -> dict[str, Any]:
    """Put data to protocols.io API."""
    headers = {
        "Authorization": f"Bearer {PROTOCOLS_IO_CLIENT_ACCESS_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.TimeoutException, json.JSONDecodeError) as e:
            return {
                "error": True,
                "message": f"Error putting resourse: {e}",
                "url": url
            }

@mcp.tool()
def generate_guids(count: int) -> list:
    """Generate a list of unique GUIDs."""
    guids = [uuid.uuid4().hex for _ in range(count)]
    return guids

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

@mcp.tool()
async def get_protocol_list(username: str) -> dict:
    """Get a list of all protocols on protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v3/researchers/{username}/protocols?filter=user_all"
    response = await get_protocols_io_resource(url)
    return response

@mcp.tool()
async def update_protocol(protocol_id: int | str, title: Optional[str] = None, description: Optional[str] = None, before_start: Optional[str] = None, guidelines: Optional[str] = None) -> dict:
    """Update a protocol on protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v4/protocols/{protocol_id}"
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if before_start:
        data["before_start"] = before_start
    if guidelines:
        data["guidelines"] = guidelines
    response = await put_protocols_io_resource(url, data)
    return response

@mcp.tool()
async def get_protocol_steps(protocol_id: int | str) -> dict:
    """Get a list of steps for a protocol on protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v4/protocols/{protocol_id}/steps"
    response = await get_protocols_io_resource(url)
    return response

@mcp.tool()
async def create_or_update_protocol_step(protocol_id: int | str, steps: list[ProtocolStep]) -> dict:
    """Create or update the steps of a protocol on protocols.io."""
    url = f"{PROTOCOLS_IO_API_URL}/v4/protocols/{protocol_id}/steps"
    serialized_steps = []
    for step in steps:
        step_data = step.model_dump(exclude_none=True)
        serialized_steps.append(step_data)
    data = {
        "steps": serialized_steps
    }
    response = await post_protocols_io_resource(url, data)
    return response

if __name__ == "__main__":
    mcp.run(transport='stdio')