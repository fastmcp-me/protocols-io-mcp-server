from protocols_io_mcp.server import mcp
import uuid

@mcp.tool()
def generate_guids(count: int) -> list:
    """Generate a list of unique GUIDs."""
    guids = [uuid.uuid4().hex for _ in range(count)]
    return guids