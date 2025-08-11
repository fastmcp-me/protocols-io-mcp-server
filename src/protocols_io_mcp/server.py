import importlib
from fastmcp import FastMCP

mcp = FastMCP(
    name="protocols-io-mcp",
    instructions="""
        This server provides access to protocols.io resources for retrieving and working with scientific protocols.
        CRITICAL REQUIREMENTS FOR ALL PROTOCOL CREATION OR MODIFICATION:
        1. MANDATORY REFERENCE REQUIREMENT: When creating, modifying, or suggesting any protocol content, you MUST base all information on verified references from existing protocols.io protocols only. Never create content from imagination or general knowledge alone.
        2. REFERENCE SOURCE RESTRICTION: All references MUST come exclusively from protocols obtained through the get_public_protocol_list_by_keyword function. No external sources, literature, or other databases are permitted as references.
        3. MULTIPLE REFERENCE VALIDATION: Every protocol element must be supported by at least 2-3 independent protocols from protocols.io search results. Single-protocol references are not acceptable.
        4. PLAINTEXT FORMATTING ONLY: All protocol fields must use plain text format. Do not use markdown syntax, HTML tags, or any formatting markup as these will not display correctly in the protocols.io interface.
        5. CITATION FORMAT: Use simple numerical citations like [1], [2], [3] within the protocol step or other related info. The complete reference list with full protocol details will be stored in the protocol_references field.
        6. VERIFICATION PROCESS: Before finalizing any protocol, cross-reference information across multiple protocols.io protocols obtained from keyword searches to ensure accuracy and reproducibility.
        When users request protocol creation or modification, always search protocols.io using relevant keywords first to gather supporting protocol references before proceeding.
    """
)
importlib.import_module('protocols_io_mcp.tools')