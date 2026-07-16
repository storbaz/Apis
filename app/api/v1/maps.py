from fastapi import APIRouter, Query, HTTPException
from app.services.maps_service import search_google_maps, search_place_by_name
from app.services.enrich_service import enrich_business
from app.schemas.maps import SearchResponse, BusinessResult
from app.config import settings

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/search", response_model=SearchResponse)
async def search_businesses(
    query: str = Query(..., description="Business type or keyword (e.g. 'dentistas')"),
    location: str = Query("", description="Location (e.g. 'Madrid, Spain')"),
    limit: int = Query(20, ge=1, le=100, description="Max results")
):
    if not settings.SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="SERPER_API_KEY not configured")

    try:
        result = await search_google_maps(query=query, location=location, limit=limit)
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
            results.append(SearchResponse(results=[], pagination={"current_page": 1, "total_results": 0, "has_next": False}))
    return results


@router.get("/place", response_model=BusinessResult)
async def get_place(
    place_id: str = Query(..., description="Google Maps Place ID"),
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
