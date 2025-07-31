import uuid
from typing import Optional, Annotated, Literal
from pydantic import BaseModel, Field
from protocols_io_mcp.server import mcp
import protocols_io_mcp.utils.helpers as helpers

class ProtocolStep(BaseModel):
    guid: Annotated[str, Field(description="Unique identifier for this protocol step. Please use 'generate_guids' to create the new GUIDs.")]
    step: str
    previous_guid: Annotated[Optional[str], Field(description="Only the previous_guid of the first step can be null.")] = None
    section: Optional[str] = None
    section_color: Optional[str] = None
    is_substep: bool

    def dict(self, **kwargs):
        return self.model_dump(exclude_none=True, **kwargs)

@mcp.tool()
async def create_protocol() -> dict:
    """Create a new protocol on protocols.io."""
    data = {
        "type_id": 1,
    }
    response = await helpers.access_protocols_io_resource("POST", f"/v3/protocols/{uuid.uuid4().hex}", data)
    return response

@mcp.tool()
async def get_user_protocol_list() -> dict:
    """Get a list of all protocols on protocols.io."""
    response_profile = await helpers.access_protocols_io_resource("GET", f"/v3/session/profile", {})
    if "user" not in response_profile or "username" not in response_profile["user"]:
        return response_profile
    response = await helpers.access_protocols_io_resource("GET", f"/v3/researchers/{response_profile['user']['username']}/protocols?filter=user_all")
    return response

@mcp.tool()
async def get_public_protocol_list_by_keyword(protocol_filter: Literal["public", "user_public", "user_private", "shared_with_user"], keyword: str, page_size: int = 10, page_id: int = 1) -> dict:
    """Get a list of public protocols on protocols.io by keyword."""
    response = await helpers.access_protocols_io_resource("GET", f"/v3/protocols?filter={protocol_filter}&key={keyword}&page_size={page_size}&page_id={page_id}")
    return response

@mcp.tool()
async def update_protocol(
    protocol_id: int | str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    before_start: Optional[str] = None,
    guidelines: Optional[str] = None,
    warning: Optional[str] = None,
    materials_text: Optional[str] = None,
    protocol_references: Annotated[Optional[str], Field(description="Use `\n` when line breaking")] = None,
) -> dict:
    """Update a protocol on protocols.io."""
    keys = ["title", "description", "before_start", "guidelines", "warning", "materials_text", "protocol_references"]
    data = {key: value for key, value in zip(keys, [title, description, before_start, guidelines, warning, materials_text, protocol_references]) if value is not None}
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