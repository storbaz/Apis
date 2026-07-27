import json
import os
import httpx
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/stats", tags=["stats"])

STATS_CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "japan_stats.json")
CACHE_TTL = timedelta(hours=24)

_cache = {"data": None, "updated_at": None}


def _load_stats():
    if _cache["data"] and _cache["updated_at"]:
        if datetime.now() - _cache["updated_at"] < CACHE_TTL:
            return _cache["data"]

    try:
        with open(STATS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _cache["data"] = data
        _cache["updated_at"] = datetime.now()
        return data
    except FileNotFoundError:
        return _get_default_stats()


def _get_default_stats():
    return {
        "source": "JNTO / Japan Government",
        "last_updated": "2025-01-01",
        "visitors": {
            "total_2024": 36870000,
            "total_2023": 25066000,
            "growth_yoy": "47%",
            "record_year": 2024,
            "note": "Récord histórico superando los 31.9M de pre-pandemia (2019)",
        },
        "spending": {
            "avg_daily_per_tourist": 148,
            "avg_daily_food": 46,
            "avg_daily_accommodation": 55,
            "avg_daily_transport": 20,
            "avg_daily_shopping": 27,
            "currency": "EUR",
            "note": "Basado en encuesta JNTO 2024 a turistas internacionales",
        },
        "duration": {
            "avg_nights": 7.2,
            "most_popular": "7-8 noches",
            "note": "Turistas internacionales excluyendo China",
        },
        "popular_destinations": [
            {"name": "Tokio", "share": "48%"},
            {"name": "Osaka", "share": "32%"},
            {"name": "Kioto", "share": "28%"},
            {"name": "Hiroshima", "share": "15%"},
            {"name": "Nara", "share": "12%"},
            {"name": "Fukuoka", "share": "10%"},
            {"name": "Kanazawa", "share": "8%"},
        ],
        "seasonality": {
            "peak": "Marzo-Abril (sakura) y Octubre-Noviembre (koyo)",
            "chill": "Enero-Febrero (menos turistas, más barato)",
            "hot": "Julio-Agosto (caluroso, festivales de verano)",
            "note": "Golden Week (28 abril-6 mayo) es la semana más cara",
        },
        "jr_pass": {
            "price_7d": 50000,
            "price_14d": 80000,
            "price_21d": 100000,
            "currency": "JPY",
            "note": "Precios desde octubre 2023 (incremento del 69%)",
        },
        "exchange_rate": {
            "jpy_to_eur": None,
            "last_fetched": None,
            "note": "Se actualiza en tiempo real desde ExchangeRate API",
        },
    }


async def _fetch_exchange_rate():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("https://open.er-api.com/v6/latest/EUR")
            if resp.status_code == 200:
                data = resp.json()
                jpy = data.get("rates", {}).get("JPY")
                if jpy:
                    return {"jpy_to_eur": round(1 / jpy, 6), "last_fetched": datetime.now().isoformat()}
    except Exception:
        pass
    return None


@router.get("")
async def get_stats():
    stats = _load_stats()
    rate = await _fetch_exchange_rate()
    if rate:
        stats["exchange_rate"] = rate
    return stats


@router.get("/refresh")
async def refresh_stats():
    _cache["data"] = None
    _cache["updated_at"] = None
    stats = _load_stats()
    rate = await _fetch_exchange_rate()
    if rate:
        stats["exchange_rate"] = rate
    return {"status": "refreshed", "data": stats}
