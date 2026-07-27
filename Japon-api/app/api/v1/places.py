from fastapi import APIRouter, Query, HTTPException
from app.config import settings
from cachetools import TTLCache
import httpx

router = APIRouter(prefix="/places", tags=["places-search"])

SERPER_BASE_URL = "https://google.serper.dev"
cache = TTLCache(maxsize=200, ttl=3600)
http_client = httpx.AsyncClient(timeout=15)


def _parse_place(item: dict) -> dict:
    coordinates = None
    lat = item.get("latitude")
    lng = item.get("longitude")
    if lat is not None and lng is not None:
        coordinates = {"lat": lat, "lng": lng}

    return {
        "place_id": str(item.get("cid", "")),
        "name": item.get("title", ""),
        "category": item.get("category"),
        "address": item.get("address"),
        "phone": item.get("phone"),
        "website": item.get("website"),
        "rating": item.get("rating"),
        "reviews_count": item.get("ratingCount"),
        "coordinates": coordinates,
        "hours": item.get("hours"),
        "price_level": item.get("price"),
        "thumbnail_url": item.get("thumbnailUrl"),
        "google_maps_url": _build_maps_url(item),
    }


def _build_maps_url(item: dict) -> str:
    lat = item.get("latitude")
    lng = item.get("longitude")
    title = item.get("title", "").replace(" ", "+")
    if lat and lng:
        return f"https://www.google.com/maps?q={lat},{lng}+{title}"
    place_id = item.get("placeId", "")
    if place_id:
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    return ""


JAPAN_CITIES = {
    "tokyo": "Tokyo, Japan",
    "osaka": "Osaka, Japan",
    "kyoto": "Kyoto, Japan",
    "hiroshima": "Hiroshima, Japan",
    "nara": "Nara, Japan",
    "fukuoka": "Fukuoka, Japan",
    "nagoya": "Nagoya, Japan",
    "sapporo": "Sapporo, Japan",
    "kobe": "Kobe, Japan",
    "yokohama": "Yokohama, Japan",
    "hakone": "Hakone, Japan",
    "kanazawa": "Kanazawa, Japan",
    "takayama": "Takayama, Japan",
    "nikko": "Nikko, Japan",
    "okinawa": "Okinawa, Japan",
}


@router.get("/search")
async def search_places(
    q: str = Query(..., description="Búsqueda (ej: 'ramen', 'hotel', 'sushi')"),
    city: str = Query("tokyo", description="Ciudad de Japón"),
    limit: int = Query(20, ge=1, le=50),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    city_query = JAPAN_CITIES.get(city.lower(), city)
    full_query = f"{q} {city_query}"

    cache_key = f"search_{full_query}_{limit}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"q": full_query, "hl": "en", "gl": "jp"}

    try:
        response = await http_client.post(f"{SERPER_BASE_URL}/places", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Serper API error: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to Serper: {str(e)}")

    places = data.get("places", [])
    results = [_parse_place(item) for item in places[:limit]]

    result = {
        "query": q,
        "city": city.lower(),
        "results": results,
        "total": len(results),
    }
    cache[cache_key] = result
    return result


@router.get("/nearby")
async def search_nearby_places(
    lat: float = Query(..., description="Latitud"),
    lng: float = Query(..., description="Longitud"),
    query: str = Query("restaurants", description="Tipo de negocio"),
    radius: int = Query(3000, ge=100, le=20000, description="Radio en metros"),
    limit: int = Query(20, ge=1, le=50),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    cache_key = f"nearby_{lat}_{lng}_{query}_{radius}_{limit}"
    if cache_key in cache:
        return cache[cache_key]

    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "q": query,
        "hl": "en",
        "gl": "jp",
        "location": f"{lat},{lng}",
        "radius": radius,
    }

    try:
        response = await http_client.post(f"{SERPER_BASE_URL}/places", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error: {str(e)}")

    places = data.get("places", [])
    results = [_parse_place(item) for item in places[:limit]]

    result = {
        "query": query,
        "results": results,
        "total": len(results),
    }
    cache[cache_key] = result
    return result


@router.get("/reviews")
async def get_place_reviews(
    place_id: str = Query(..., description="Place CID de Google Maps"),
    name: str = Query("", description="Nombre del lugar"),
    lat: float = Query(0, description="Latitud"),
    lng: float = Query(0, description="Longitud"),
):
    if lat and lng:
        maps_url = f"https://www.google.com/maps?q={lat},{lng}+{name.replace(' ', '+')}"
    else:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}"

    return {
        "place_id": place_id,
        "message": "Las reseñas están disponibles directamente en Google Maps",
        "google_maps_url": maps_url,
    }


@router.get("/cities")
async def get_japan_cities():
    return {
        "cities": [
            {"id": k, "name": v.split(",")[0]} for k, v in JAPAN_CITIES.items()
        ]
    }
