from fastapi import APIRouter, Query
from app.services.culture_service import (
    get_phrases,
    get_etiquette,
    get_do_and_dont,
    get_scenario,
    get_all_scenarios
)

router = APIRouter(prefix="/culture", tags=["culture-guide"])


@router.get("/phrases")
async def phrases(
    category: str = Query(None, description="basico, restaurante, compras, transporte, hotel, emergencia"),
    language: str = Query("es", description="Idioma: es, en, fr, pt")
):
    result = get_phrases(category, language)
    return {
        "total": len(result),
        "category": category or "todos",
        "phrases": result
    }


@router.get("/etiquette")
async def etiquette(
    category: str = Query(None, description="zapatos, comida, transporte, baño, social, templo, onzen, basura")
):
    result = get_etiquette(category)
    return {
        "total": len(result),
        "category": category or "todos",
        "rules": result
    }


@router.get("/do-and-dont")
async def do_and_dont(
    category: str = Query(None, description="comida, social, transporte")
):
    result = get_do_and_dont(category)
    return {
        "total": len(result),
        "category": category or "todos",
        "rules": result
    }


@router.get("/scenarios")
async def scenarios():
    result = get_all_scenarios()
    return {
        "total": len(result),
        "scenarios": result
    }


@router.get("/scenarios/{scenario_id}")
async def scenario_detail(scenario_id: str):
    result = get_scenario(scenario_id)
    if not result:
        return {"error": "Escenario no encontrado"}
    return result
