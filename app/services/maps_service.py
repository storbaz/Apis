import httpx
from app.config import settings
from app.schemas.maps import (
    BusinessResult, Coordinates, Pagination, SearchResponse
)


SERPER_BASE_URL = "https://google.serper.dev"


async def search_google_maps(query: str, location: str = "", limit: int = 20) -> SearchResponse:
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    search_query = f"{query} {location}".strip()

    payload = {
        "q": search_query,
        "hl": "es",
        "gl": "es"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{SERPER_BASE_URL}/places",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()

    results = []
    for item in data.get("places", [])[:limit]:
        coordinates = None
        if "latitude" in item and "longitude" in item:
            coordinates = Coordinates(
                lat=item.get("latitude", 0),
                lng=item.get("longitude", 0)
            )

        result = BusinessResult(
            place_id=str(item.get("cid", "")),
            name=item.get("title", ""),
            category=item.get("category"),
            address=item.get("address"),
            phone=item.get("phone"),
            website=item.get("website"),
            rating=item.get("rating"),
            reviews_count=item.get("ratingCount"),
            coordinates=coordinates,
            hours=None,
            is_claimed=None
        )
        results.append(result)

    total = len(data.get("places", []))

    return SearchResponse(
        results=results,
        pagination=Pagination(
            current_page=1,
            total_results=total,
            has_next=total > limit
        )
    )


async def search_place_by_name(name: str) -> BusinessResult | None:
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": name,
        "hl": "es",
        "gl": "es"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{SERPER_BASE_URL}/places",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()

    places = data.get("places", [])
    if not places:
        return None

    item = places[0]

    coordinates = None
    if "latitude" in item and "longitude" in item:
        coordinates = Coordinates(
            lat=item.get("latitude", 0),
            lng=item.get("longitude", 0)
        )

    return BusinessResult(
        place_id=str(item.get("cid", "")),
        name=item.get("title", ""),
        category=item.get("category"),
        address=item.get("address"),
        phone=item.get("phone"),
        website=item.get("website"),
        rating=item.get("rating"),
        reviews_count=item.get("ratingCount"),
        coordinates=coordinates,
        hours=None,
        is_claimed=None
    )
