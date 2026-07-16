from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response
from app.services.maps_service import (
    search_google_maps, search_place_by_name,
    search_nearby, get_place_reviews,
)
from app.services.enrich_service import enrich_business
from app.schemas.maps import SearchResponse, BusinessResult, ReviewsResponse, Pagination
from app.config import settings

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/search", response_model=SearchResponse)
async def search_businesses(
    query: str = Query(..., description="Business type or keyword (e.g. 'dentistas')"),
    location: str = Query("", description="Location (e.g. 'Madrid, Spain')"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
    page: int = Query(1, ge=1, le=10, description="Page number for pagination"),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        result = await search_google_maps(query=query, location=location, limit=limit, page=page)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data: {str(e)}")


@router.get("/bulk", response_model=list[SearchResponse])
async def search_businesses_bulk(
    queries: str = Query(..., description="Comma-separated search queries"),
    location: str = Query("", description="Location for all searches"),
    limit: int = Query(10, ge=1, le=50, description="Max results per query")
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    query_list = [q.strip() for q in queries.split(",") if q.strip()]
    if not query_list:
        raise HTTPException(status_code=400, detail="At least one query required")
    if len(query_list) > 5:
        raise HTTPException(status_code=400, detail="Max 5 queries per bulk request")

    results = []
    for q in query_list:
        try:
            result = await search_google_maps(query=q, location=location, limit=limit)
            results.append(result)
        except Exception:
            results.append(SearchResponse(results=[], pagination=Pagination(current_page=1, total_results=0, has_next=False)))
    return results


@router.get("/nearby", response_model=SearchResponse)
async def search_nearby_businesses(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    query: str = Query("", description="Business type filter (e.g. 'restaurants')"),
    radius: int = Query(5000, ge=100, le=50000, description="Search radius in meters"),
    limit: int = Query(20, ge=1, le=50, description="Max results"),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        result = await search_nearby(lat=lat, lng=lng, query=query, radius=radius, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching nearby data: {str(e)}")


@router.get("/place", response_model=BusinessResult)
async def get_place(
    place_id: str = Query(..., description="Google Maps Place ID or CID"),
    enrich: bool = Query(False, description="Enrich with email and social data")
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        result = await search_place_by_name(name=place_id)
        if not result:
            raise HTTPException(status_code=404, detail="Place not found")

        if enrich and result.website:
            enrichment = await enrich_business(result.website)
            result.enrichment = enrichment

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching place: {str(e)}")


@router.get("/reviews", response_model=ReviewsResponse)
async def get_reviews(
    place_id: str = Query(..., description="Google Maps Place CID"),
    hl: str = Query("en", description="Language code (e.g. 'en', 'es')"),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        reviews = await get_place_reviews(place_id=place_id, hl=hl)
        return ReviewsResponse(
            place_id=place_id,
            reviews=reviews,
            total=len(reviews),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching reviews: {str(e)}")


@router.get("/niche/{niche}")
async def search_niche(
    niche: str,
    location: str = Query("", description="City or region"),
    limit: int = Query(20, ge=1, le=100),
    enrich: bool = Query(False, description="Enrich with emails"),
):
    NICHE_MAP = {
        "dentistas": "dentist",
        "restaurantes": "restaurant",
        "farmacias": "pharmacy",
        "gimnasios": "gym",
        "hoteles": "hotel",
        "abogados": "lawyer",
        "inmobiliarias": "real estate agency",
        "clinicas": "medical clinic",
        "veterinarias": "veterinary",
        "talleres": "auto repair",
        "panaderias": "bakery",
        "cafeterias": "coffee shop",
        "supermercados": "supermarket",
        "librerias": "bookstore",
        "floristerias": "florist",
        "peluquerias": "hair salon",
        "dentists": "dentist",
        "restaurants": "restaurant",
        "pharmacies": "pharmacy",
        "gyms": "gym",
        "hotels": "hotel",
        "lawyers": "lawyer",
        "clinics": "medical clinic",
        "vet": "veterinary",
        "mechanics": "auto repair",
        "bakeries": "bakery",
        "cafes": "coffee shop",
        "markets": "supermarket",
        "bookstores": "bookstore",
        "florists": "florist",
        "salons": "hair salon",
    }
    query = NICHE_MAP.get(niche.lower(), niche)

    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        result = await search_google_maps(query=query, location=location, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error: {str(e)}")

    if enrich:
        enriched = []
        for biz in result.results:
            if biz.website:
                try:
                    enrichment = await enrich_business(biz.website)
                    biz.enrichment = enrichment
                except Exception:
                    pass
            enriched.append(biz)
        result.results = enriched

    return result


@router.get("/niche/{niche}/export")
async def export_niche_csv(
    niche: str,
    location: str = Query("", description="City or region"),
    limit: int = Query(50, ge=1, le=200),
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    NICHE_MAP = {
        "dentistas": "dentist", "restaurantes": "restaurant", "farmacias": "pharmacy",
        "gimnasios": "gym", "hoteles": "hotel", "abogados": "lawyer",
        "clinicas": "medical clinic", "veterinarias": "veterinary", "talleres": "auto repair",
        "dentists": "dentist", "restaurants": "restaurant", "pharmacies": "pharmacy",
        "gyms": "gym", "hotels": "hotel", "lawyers": "lawyer",
    }
    query = NICHE_MAP.get(niche.lower(), niche)

    try:
        result = await search_google_maps(query=query, location=location, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error: {str(e)}")

    lines = ["Name,Category,Address,Phone,Website,Rating,Reviews,Google Maps URL"]
    for biz in result.results:
        name = (biz.name or "").replace(",", ";")
        cat = (biz.category or "").replace(",", ";")
        addr = (biz.address or "").replace(",", ";")
        phone = biz.phone or ""
        web = biz.website or ""
        rating = biz.rating or ""
        reviews = biz.reviews_count or ""
        gurl = biz.google_maps_url or ""
        lines.append(f'"{name}","{cat}","{addr}","{phone}","{web}","{rating}","{reviews}","{gurl}"')

    csv_content = "\n".join(lines)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{niche}_leads.csv"'},
    )


@router.get("/niches")
async def list_niches():
    return {
        "niches": [
            {"id": "dentistas", "name": "Dentistas", "icon": "dentist"},
            {"id": "restaurantes", "name": "Restaurantes", "icon": "restaurant"},
            {"id": "farmacias", "name": "Farmacias", "icon": "pharmacy"},
            {"id": "gimnasios", "name": "Gimnasios", "icon": "gym"},
            {"id": "hoteles", "name": "Hoteles", "icon": "hotel"},
            {"id": "abogados", "name": "Abogados", "icon": "lawyer"},
            {"id": "clinicas", "name": "Clínicas", "icon": "clinic"},
            {"id": "veterinarias", "name": "Veterinarias", "icon": "vet"},
            {"id": "talleres", "name": "Talleres", "icon": "mechanic"},
            {"id": "panaderias", "name": "Panaderías", "icon": "bakery"},
            {"id": "cafeterias", "name": "Cafeterías", "icon": "coffee"},
            {"id": "supermercados", "name": "Supermercados", "icon": "market"},
            {"id": "peluquerias", "name": "Peluquerías", "icon": "salon"},
            {"id": "floristerias", "name": "Floristerías", "icon": "florist"},
            {"id": "librerias", "name": "Librerías", "icon": "bookstore"},
        ],
        "usage": "/v1/maps/niche/dentistas?location=Madrid&enrich=true",
        "export": "/v1/maps/niche/dentistas/export?location=Madrid&limit=50",
    }
