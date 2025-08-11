from protocols_io_mcp.server import mcp

def main():
    """Run the protocols.io MCP server."""
    print("Starting protocols.io MCP server...")
    mcp.run()

if __name__ == "__main__":
    main()