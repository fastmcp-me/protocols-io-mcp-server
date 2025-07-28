import importlib
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="protocols-io-mcp-server",
    instructions="""This server provides access to protocols.io API."""
)
importlib.import_module('protocols_io_mcp.tools')