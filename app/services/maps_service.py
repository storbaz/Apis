import httpx
from cachetools import TTLCache
from app.config import settings
from app.schemas.maps import (
    BusinessResult, Coordinates, Pagination, SearchResponse, Review
)

SERPER_BASE_URL = "https://google.serper.dev"
http_client = httpx.AsyncClient(timeout=10)
cache = TTLCache(maxsize=200, ttl=600)


def _build_maps_url(item: dict) -> str:
    cid = item.get("cid", "")
    if cid:
        return f"https://www.google.com/maps/cid/{cid}"
    place_id = item.get("placeId", "")
    if place_id:
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    return ""


def _parse_hours(item: dict) -> dict | None:
    hours_data = item.get("hours")
    if not hours_data or not isinstance(hours_data, dict):
        return None
    return hours_data


def _build_business_result(item: dict) -> BusinessResult:
    coordinates = None
    lat = item.get("latitude")
    lng = item.get("longitude")
    if lat is not None and lng is not None:
        coordinates = Coordinates(lat=lat, lng=lng)

    hours = _parse_hours(item)

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
        hours=hours,
        is_claimed=item.get("claimStatus") == "CLAIMED",
        service_options=item.get("serviceOptions"),
        price_level=item.get("price"),
        thumbnail_url=item.get("thumbnailUrl"),
        google_maps_url=_build_maps_url(item),
    )


async def search_google_maps(
    query: str,
    location: str = "",
    limit: int = 20,
    page: int = 1,
) -> SearchResponse:
    cache_key = f"search_{query}_{location}_{limit}_{page}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    search_query = f"{query} {location}".strip()

    payload = {
        "q": search_query,
        "hl": "es",
        "gl": "es",
    }
    if page > 1:
        payload["page"] = page

    response = await http_client.post(
        f"{SERPER_BASE_URL}/places",
        json=payload,
        headers=headers
    )
    response.raise_for_status()
    data = response.json()

    places = data.get("places", [])
    results = [_build_business_result(item) for item in places[:limit]]

    total = len(places)
    search_response = SearchResponse(
        results=results,
        pagination=Pagination(
            current_page=page,
            total_results=data.get("searchInformation", {}).get("totalResults", total),
            has_next=total >= limit,
        )
    )
    cache[cache_key] = search_response
    return search_response


async def search_nearby(
    lat: float,
    lng: float,
    query: str = "",
    radius: int = 5000,
    limit: int = 20,
) -> SearchResponse:
    cache_key = f"nearby_{lat}_{lng}_{query}_{radius}_{limit}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    search_query = query if query else "businesses"

    payload = {
        "q": search_query,
        "hl": "es",
        "gl": "es",
        "location": f"{lat},{lng}",
        "radius": radius,
    }

    response = await http_client.post(
        f"{SERPER_BASE_URL}/places",
        json=payload,
        headers=headers
    )
    response.raise_for_status()
    data = response.json()

    places = data.get("places", [])
    results = [_build_business_result(item) for item in places[:limit]]

    search_response = SearchResponse(
        results=results,
        pagination=Pagination(
            current_page=1,
            total_results=len(places),
            has_next=len(places) >= limit,
        )
    )
    cache[cache_key] = search_response
    return search_response


async def search_place_by_name(name: str) -> BusinessResult | None:
    cache_key = f"place_{name}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": name,
        "hl": "es",
        "gl": "es"
    }

    response = await http_client.post(
        f"{SERPER_BASE_URL}/places",
        json=payload,
        headers=headers
    )
    response.raise_for_status()
    data = response.json()

    places = data.get("places", [])
    if not places:
        return None

    result = _build_business_result(places[0])
    cache[cache_key] = result
    return result


async def get_place_reviews(
    place_id: str,
    hl: str = "es",
) -> list[Review]:
    cache_key = f"reviews_{place_id}_{hl}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "cid": place_id,
        "hl": hl,
    }

    response = await http_client.post(
        f"{SERPER_BASE_URL}/places/details",
        json=payload,
        headers=headers
    )
    response.raise_for_status()
    data = response.json()

    reviews_data = data.get("reviews", [])
    reviews = []
    for r in reviews_data:
        reviews.append(Review(
            author=r.get("authorName", ""),
            rating=r.get("rating"),
            text=r.get("text", ""),
            time=r.get("time", ""),
            profile_image=r.get("authorImage"),
        ))

    cache[cache_key] = reviews
    return reviews
