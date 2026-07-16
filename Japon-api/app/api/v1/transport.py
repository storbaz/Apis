from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/transport", tags=["transport-trains"])


JR_PASS_INFO = {
    "name": "Japan Rail Pass (JR Pass)",
    "description": "Pasaje ilimitado en trenes JR (Japan Railways) por un periodo de tiempo.",
    "types": [
        {
            "name": "JR Pass Normal",
            "duration": "7, 14 o 21 dias",
            "prices": {
                "7_dias": 50000,
                "14_dias": 80000,
                "21_dias": 100000
            },
            "currency": "JPY",
            "includes": [
                "Todos los trenes JR (excepto Nozomi y Mizuho)",
                "JR buses urbanos",
                "Ferry a Miyajima (Hiroshima)"
            ]
        },
        {
            "name": "JR Pass Green (Primera Clase)",
            "duration": "7, 14 o 21 dias",
            "prices": {
                "7_dias": 70000,
                "14_dias": 110000,
                "21_dias": 140000
            },
            "currency": "JPY",
            "includes": [
                "Todo lo del JR Pass normal",
                "Asientos premium en trenes",
                "Mas espacio y comodidad"
            ]
        }
    ],
    "where_to_buy": [
        "Online antes del viaje (recomendado - a veces hay descuentos)",
        "Estaciones JR principales (Tokyo, Shin-Osaka, etc.)",
        "Aeropuerto de Narita/Haneda"
    ],
    "tips": [
        "Si vas a hacer Tokyo-Kyoto-Osaka, el JR Pass te ahorra dinero",
        "No cubre el Nozomi (el tren mas rapido), usa el Hikari en su lugar",
        "Activalo en la estacion con tu pasaporte",
        "Los asientos de reservados se pueden usar gratis con el JR Pass"
    ]
}

CITY_CONNECTIONS = [
    {
        "from": "Tokyo",
        "to": "Kyoto",
        "train": "Shinkansen (Hikari)",
        "duration": "2h 40min",
        "price_jpy": 13320,
        "frequency": "Cada 15-30 minutos",
        "tips": "Sentado en el lado derecho (asiento D o E) puedes ver el Monte Fuji"
    },
    {
        "from": "Tokyo",
        "to": "Osaka",
        "train": "Shinkansen (Hikari)",
        "duration": "2h 55min",
        "price_jpy": 14400,
        "frequency": "Cada 15-30 minutos",
        "tips": "Si tienes JR Pass, es gratis. Sin el, considera vuelo low-cost."
    },
    {
        "from": "Kyoto",
        "to": "Osaka",
        "train": "JR Special Rapid",
        "duration": "30 minutos",
        "price_jpy": 580,
        "frequency": "Cada 15 minutos",
        "tips": "El JR Pass cubre esta ruta. Es la forma mas rapida."
    },
    {
        "from": "Osaka",
        "to": "Hiroshima",
        "train": "Shinkansen (Sakura)",
        "duration": "1h 30min",
        "price_jpy": 10200,
        "frequency": "Cada 30 minutos",
        "tips": "El JR Pass cubre esta ruta. Hiroshima vale la pena por el Peace Memorial."
    },
    {
        "from": "Tokyo",
        "to": "Hakone",
        "train": "Romancecar (Odakyu)",
        "duration": "1h 30min",
        "price_jpy": 2330,
        "frequency": "Cada 30 minutos",
        "tips": "No cubierto por JR Pass. Compra el Hakone Free Pass por 6100 yen (2 dias de transporte ilimitado)."
    },
    {
        "from": "Tokyo",
        "to": "Nikko",
        "train": "JR + Tobu Railway",
        "duration": "2h",
        "price_jpy": 5500,
        "frequency": "Cada hora",
        "tips": "El JR Pass cubre la parte JR. El tren Tobu es aparte."
    },
    {
        "from": "Osaka",
        "to": "Nara",
        "train": "JR Nara Line",
        "duration": "45 minutos",
        "price_jpy": 820,
        "frequency": "Cada 30 minutos",
        "tips": "JR Pass cubre esta ruta. Nara es perfecta para ver los ciervos."
    }
]

TRANSPORT_TIPS = [
    {
        "title": "Suica o Pasmo",
        "description": "Tarjetas recargables para metro y trenes locales. Funcionan en casi todos los transportes de Japon.",
        "where_to_buy": "Maquinas en cualquier estacion de metro/tren",
        "tip": "Recarga con efectivo. Algunos konbini tambien las aceptan."
    },
    {
        "title": "Trenes nocturnos",
        "description": "Hay trenes nocturnos que te ahorran una noche de hotel. Son comodos y economicos.",
        "routes": "Tokyo-Kyoto, Tokyo-Osaka",
        "tip": "Reserva con antelacion, especialmente en vacaciones."
    },
    {
        "title": "Autobuses de largo recorrido",
        "description": "Willer Express y otros operadores ofrecen buses economicos entre ciudades.",
        "prices": "Desde 2000 yen",
        "tip": "Son comodos y tienen enchufes. Buenos para presupuestos ajustados."
    },
    {
        "title": "Metro de Tokyo",
        "description": "El metro de Tokyo tiene 13 lineas. Usa Google Maps o la app Japan Travel para navegar.",
        "price": "170-320 yen por viaje",
        "tip": "Los passes de 24h/72h son economicos si vas a usar el metro mucho."
    },
    {
        "title": "Taxi en Japon",
        "description": "Caros pero utiles de noche o con maletas. La puerta se abre automaticamente.",
        "price": "Desde 500 yen + 100 yen por 300m",
        "tip": "No des propina. El conductor te abrira la puerta automaticamente."
    }
]


@router.get("/jrpass")
async def jrpass_info():
    return JR_PASS_INFO


@router.get("/connections")
async def connections(
    from_city: Optional[str] = Query(None, description="Ciudad de origen"),
    to_city: Optional[str] = Query(None, description="Ciudad de destino")
):
    result = CITY_CONNECTIONS

    if from_city:
        result = [c for c in result if from_city.lower() in c["from"].lower()]

    if to_city:
        result = [c for c in result if to_city.lower() in c["to"].lower()]

    return {
        "total": len(result),
        "connections": result
    }


@router.get("/connections/{from_city}/{to_city}")
async def connection_detail(from_city: str, to_city: str):
    connection = None
    for c in CITY_CONNECTIONS:
        if from_city.lower() in c["from"].lower() and to_city.lower() in c["to"].lower():
            connection = c
            break

    if not connection:
        return {"error": f"Conexion no encontrada entre {from_city} y {to_city}"}

    return connection


@router.get("/tips")
async def transport_tips():
    return {
        "total": len(TRANSPORT_TIPS),
        "tips": TRANSPORT_TIPS
    }
