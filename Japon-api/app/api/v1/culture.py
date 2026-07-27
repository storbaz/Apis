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


ALLERGENS = {
    "cacahuetes": {"jp": "ピーナッツ", "romaji": "piinattsu"},
    "mariscos": {"jp": "甲殻類", "romaji": "koukakurui"},
    "camarones": {"jp": "エビ", "romaji": "ebi"},
    "pescado": {"jp": "魚", "romaji": "sakana"},
    "huevos": {"jp": "卵", "romaji": "tamago"},
    "lacteos": {"jp": "乳製品", "romaji": "nyuuseihin"},
    "gluten": {"jp": "グルテン", "romaji": "guruten"},
    "soja": {"jp": "大豆", "romaji": "daizu"},
    "frutos_secos": {"jp": "ナッツ類", "romaji": "nattsurui"},
    "almendras": {"jp": "アーモンド", "romaji": "aamondo"},
    "sesamo": {"jp": "ごま", "romaji": "goma"},
    "frutas_citricas": {"jp": "柑橘類", "romaji": "kankitsurui"},
    "carne_vaca": {"jp": "牛肉", "romaji": "gyuuniku"},
    "cerdo": {"jp": "豚肉", "romaji": "butaniku"},
    "pollo": {"jp": "鶏肉", "romaji": "toriniku"},
}

ALLERGY_PHRASES = [
    {
        "japanese": "アレルギーがあります",
        "romaji": "Arerugii ga arimasu",
        "translation": "Tengo una alergia",
        "context": "Frase general para avisar"
    },
    {
        "japanese": "{allergen}にアレルギーがあります",
        "romaji": "{allergen_romaji} ni arerugii ga arimasu",
        "translation": "Soy alergico/a a {allergen}",
        "context": "Especificar alergeno",
        "template": True
    },
    {
        "japanese": "{allergen}が食べられません",
        "romaji": "{allergen_romaji} ga taberaremasen",
        "translation": "No puedo comer {allergen}",
        "context": "Cuando no puedes comer algo",
        "template": True
    },
    {
        "japanese": "{allergen}が入っていますか？",
        "romaji": "{allergen_romaji} ga haitte imasu ka?",
        "translation": "¿Contiene {allergen}?",
        "context": "Preguntar si un plato tiene el alergeno",
        "template": True
    },
    {
        "japanese": "出汁（だし）はありますか？",
        "romaji": "Dashi wa arimasu ka?",
        "translation": "¿Tiene dashi (caldo de pescado)?",
        "context": "El dashi esta en casi todo, incluso en platos que parecen vegetarianos"
    },
    {
        "japanese": "肉と魚を食べません",
        "romaji": "Niku to sakana wo tabemasen",
        "translation": "No como carne ni pescado",
        "context": "Para vegetarianos/veganos"
    },
    {
        "japanese": "これ安全ですか？",
        "romaji": "Kore anzen desu ka?",
        "translation": "¿Esto es seguro para mi?",
        "context": "Cuando no estas seguro de los ingredientes"
    },
    {
        "japanese": " ingredienten を教えてください",
        "romaji": "Seizai wo oshiete kudasai",
        "translation": "Por favor, digame los ingredientes",
        "context": "Pedir informacion de ingredientes"
    },
]


@router.get("/allergies")
async def allergy_info():
    return {
        "allergens": [
            {"id": key, "japanese": val["jp"], "romaji": val["romaji"]}
            for key, val in ALLERGENS.items()
        ],
        "phrases": ALLERGY_PHRASES
    }
