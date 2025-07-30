import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from protocols_io_mcp.server import mcp
import protocols_io_mcp.utils.helpers as helpers

class ProtocolStep(BaseModel):
    guid: Annotated[str, Field(description="Unique identifier for this protocol step. Please use 'generate_guids' to create the new GUIDs.")]
    step: str
    previous_guid: Annotated[Optional[str], Field(description="Only the previous_guid of the first step can be null.")] = None
    section: Optional[str] = None
    section_color: Optional[str] = None
    is_substep: bool = False

    def dict(self, **kwargs):
        return self.model_dump(exclude_none=True, **kwargs)

@mcp.tool()
def generate_guids(count: int) -> list:
    """Generate a list of unique GUIDs."""
    guids = [uuid.uuid4().hex for _ in range(count)]
    return guids

@mcp.tool()
async def create_protocol() -> dict:
    """Create a new protocol on protocols.io."""
    data = {
        "type_id": 1,
    }
    response = await helpers.access_protocols_io_resource("POST", f"/v3/protocols/{uuid.uuid4().hex}", data)
    return response

@mcp.tool()
async def get_protocol_list(username: str) -> dict:
    """Get a list of all protocols on protocols.io."""
    response = await helpers.access_protocols_io_resource("GET", f"/v3/researchers/{username}/protocols?filter=user_all")
    return response

@mcp.tool()
async def update_protocol(protocol_id: int | str, title: Optional[str] = None, description: Optional[str] = None, before_start: Optional[str] = None, guidelines: Optional[str] = None) -> dict:
    """Update a protocol on protocols.io."""
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if before_start:
        data["before_start"] = before_start
    if guidelines:
        data["guidelines"] = guidelines
    response = await helpers.access_protocols_io_resource("PUT", f"/v4/protocols/{protocol_id}", data)
    return response

@mcp.tool()
async def get_protocol_steps(protocol_id: int | str) -> dict:
    """Get a list of steps for a protocol on protocols.io."""
    response = await helpers.access_protocols_io_resource("GET", f"/v4/protocols/{protocol_id}/steps")
    return response

@mcp.tool()
async def create_or_update_protocol_step(protocol_id: int | str, steps: list[ProtocolStep]) -> dict:
    """Create or update the steps of a protocol on protocols.io."""
    serialized_steps = []
    for step in steps:
        step_data = step.model_dump(exclude_none=True)
        serialized_steps.append(step_data)
    data = {
        "steps": serialized_steps
    }
    response = await helpers.access_protocols_io_resource("POST", f"/v4/protocols/{protocol_id}/steps", data)
    return response

@mcp.tool()
async def delete_protocol_step(protocol_id: int | str, step_guids: list[str]) -> dict:
    """Delete steps from a protocol on protocols.io."""
    data = {
        "steps": step_guids
    }
    response = await helpers.access_protocols_io_resource("DELETE", f"/v4/protocols/{protocol_id}/steps", data)
    return response