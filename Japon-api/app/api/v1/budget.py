from fastapi import APIRouter, Query
from typing import Optional
from pydantic import BaseModel


router = APIRouter(prefix="/budget", tags=["budget-expenses"])


class CityBudget(BaseModel):
    city: str
    daily_budget_low: int
    daily_budget_medium: int
    daily_budget_high: int
    currency: str = "JPY"
    tips: list[str]


CITIES_BUDGET = {
    "tokyo": {
        "city": "Tokyo",
        "daily_budget_low": 8000,
        "daily_budget_medium": 15000,
        "daily_budget_high": 30000,
        "currency": "JPY",
        "tips": [
            "Los konbini (7-Eleven, FamilyMart) tienen comida barata y de calidad",
            "Almuerza en centros comerciales (los lunch sets son mas baratos)",
            "Usa pasajos de 24h/72h en metro",
            "El arroz con curry de CoCo Ichibanya es barato y filling"
        ]
    },
    "osaka": {
        "city": "Osaka",
        "daily_budget_low": 7000,
        "daily_budget_medium": 13000,
        "daily_budget_high": 25000,
        "currency": "JPY",
        "tips": [
            "Osaka es la ciudad de la comida callejera mas barata de Japon",
            "Dotonbori tiene opciones economicas todo el dia",
            "El Osaka Amazing Pass incluye transporte + atracciones",
            "Los takoyaki y okonomiyaki son baratos y deliciosos"
        ]
    },
    "kyoto": {
        "city": "Kyoto",
        "daily_budget_low": 7500,
        "daily_budget_medium": 14000,
        "daily_budget_high": 28000,
        "currency": "JPY",
        "tips": [
            "Muchos templos son gratis o muy baratos",
            "El bus de 1 dia es la mejor forma de moverse",
            "Evita restaurantes en Gion (caros para turistas)",
            "El matcha y los dulces tradicionales son economicos"
        ]
    },
    "hiroshima": {
        "city": "Hiroshima",
        "daily_budget_low": 6500,
        "daily_budget_medium": 12000,
        "daily_budget_high": 22000,
        "currency": "JPY",
        "tips": [
            "El Peace Memorial es gratis",
            "Los okonomiyaki estilo Hiroshima son baratos",
            "El tramway es barato y pratico",
            "Miyajima se puede visitar economicamente"
        ]
    },
    "fukuoka": {
        "city": "Fukuoka",
        "daily_budget_low": 6000,
        "daily_budget_medium": 11000,
        "daily_budget_high": 20000,
        "currency": "JPY",
        "tips": [
            "Los puestos de yatai (carritos) son la mejor opcion barata",
            "El ramen de Fukuoka es famoso y economico",
            "El subway tiene passes de 1 dia baratos",
            "Los mercados locales tienen comida fresca barata"
        ]
    }
}

TAXFREE_INFO = {
    "general": {
        "minimum_purchase": 5000,
        "currency": "JPY",
        "description": "Para obtener tax-free, debes gastar minimo 5000 yen (sin impuestos) en una misma tienda el mismo dia",
        "required_documents": ["Pasaporte original", "Tarjeta de embarque (vuelo de regreso)"],
        "stores": [
            "Grandes tiendas (Don Quijote, Bic Camera, Yodobashi)",
            "Farmacias (Matsumoto Kiyoshi, Welcia)",
            "Tiendas de souvenirs en aeropuertos",
            "Algunos konbini"
        ],
        "how_to": [
            "Busca el sticker 'Tax-Free' o 'Duty-Free' en la tienda",
            "Presenta tu pasaporte en caja",
            "El descuento se aplica automaticamente",
            "Guarda los recibos (pueden pedirlos en el aeropuerto)"
        ]
    },
    "electronics": {
        "stores": ["Bic Camera", "Yodobashi Camera", "Yamada Denki", "Don Quijote"],
        "tip": "Estas tiendas aceptan tarjeta y tienen personal que habla ingles"
    },
    "pharmacy": {
        "stores": ["Matsumoto Kiyoshi", "Welcia", "Sundrug"],
        "tip": "Los medicamentos japoneses son excelentes. Busca los que tienen estrella roja (tax-free)"
    },
    "souvenirs": {
        "stores": ["Don Quijote", "Loft", "Tokyu Hands", "Tiendas en estaciones"],
        "tip": "Los omiyage (souvenirs de comida) son perfectos para regalar"
    }
}


@router.get("/cities")
async def cities_budget():
    return {
        "total": len(CITIES_BUDGET),
        "cities": list(CITIES_BUDGET.values())
    }


@router.get("/cities/{city}")
async def city_budget(city: str):
    city_lower = city.lower()
    if city_lower not in CITIES_BUDGET:
        return {"error": f"Ciudad '{city}' no encontrada. Ciudades disponibles: {list(CITIES_BUDGET.keys())}"}
    return CITIES_BUDGET[city_lower]


@router.get("/taxfree")
async def taxfree_info():
    return TAXFREE_INFO


@router.get("/estimate")
async def estimate_daily(
    city: str = Query(..., description="Ciudad de Japon"),
    style: str = Query("medium", description="low, medium, high"),
    days: int = Query(7, description="Numero de dias")
):
    city_lower = city.lower()
    if city_lower not in CITIES_BUDGET:
        return {"error": f"Ciudad '{city}' no encontrada"}

    city_data = CITIES_BUDGET[city_lower]
    style_key = f"daily_budget_{style}"

    if style_key not in city_data:
        return {"error": "Estilo no valido. Usa: low, medium, high"}

    daily = city_data[style_key]
    total = daily * days

    return {
        "city": city_data["city"],
        "style": style,
        "daily_budget_jpy": daily,
        "total_budget_jpy": total,
        "days": days,
        "estimated_eur": round(total * 0.0062, 2),
        "estimated_usd": round(total * 0.0067, 2),
        "tips": city_data["tips"]
    }
