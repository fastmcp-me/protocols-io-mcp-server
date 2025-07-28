from protocols_io_mcp.server import mcp
import protocols_io_mcp.utils.helpers as helpers

@mcp.tool()
async def get_profile() -> dict:
    """Get user profile information from protocols.io."""
    response = await helpers.access_protocols_io_resource("GET", "/v3/session/profile")
    return response