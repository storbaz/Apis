"""Google Maps Business Scraper MCP Server — HTTP transport for public access."""

from __future__ import annotations
import os
from typing import Annotated

import httpx
from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP(
    name="gmaps-scraper",
    instructions="Google Maps business scraper. Use search_businesses to find places, "
                 "get_business_details for full info including email and social profiles.",
    version="1.0.0",
)

SCRAPER_BASE = os.environ.get("SCRAPER_BASE_URL", "https://apis-4g3r.onrender.com")


@mcp.tool(
    tags={"maps", "search", "leads"},
    annotations={"readOnlyHint": True, "openWorldHint": True},
)
async def search_businesses(
    query: Annotated[str, Field(description="Business type or name (e.g., 'dentists', 'restaurants', 'plumbers')")],
    location: Annotated[str, Field(description="Location (e.g., 'Madrid', 'New York', 'London')")],
    limit: Annotated[int, Field(description="Max results (1-50)", ge=1, le=50)] = 10,
) -> dict:
    """Search Google Maps for businesses by type near a location.

    Returns businesses with name, category, address, website, rating, and coordinates.
    Use this to find leads for outreach or market research.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{SCRAPER_BASE}/v1/maps/search",
            params={"query": query, "location": location, "limit": limit},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool(
    tags={"maps", "details", "email"},
    annotations={"readOnlyHint": True, "openWorldHint": True},
)
async def get_business_details(
    place_id: Annotated[str, Field(description="Place ID from search results")],
    enrich: Annotated[bool, Field(description="Enable email verification and social profile detection")] = False,
) -> dict:
    """Get full details for a specific business including email and social profiles.

    Set enrich=true to get verified emails and social media links (LinkedIn, Instagram, Facebook, Twitter).
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{SCRAPER_BASE}/v1/maps/place/{place_id}",
            params={"enrich": enrich},
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8002)
