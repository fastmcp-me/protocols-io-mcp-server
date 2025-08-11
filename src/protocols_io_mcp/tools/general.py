from protocols_io_mcp.server import mcp
import uuid

@mcp.tool()
def generate_ids(count: int) -> list:
    """Generate a list of unique IDs."""
    ids = [uuid.uuid4().hex for _ in range(count)]
    return ids