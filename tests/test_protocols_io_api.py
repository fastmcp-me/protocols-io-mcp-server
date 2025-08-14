import pytest
from protocols_io_mcp.utils import helpers

@pytest.mark.asyncio
async def test_get_profile():
    """
    Test the get profile feature of the protocols.io API.
    """
    profile = await helpers.access_protocols_io_resource("GET", "/v3/session/profile")
    assert isinstance(profile, dict)
    assert "user" in profile
    assert "name" in profile["user"]
    assert "username" in profile["user"]
    assert "affiliation" in profile["user"]