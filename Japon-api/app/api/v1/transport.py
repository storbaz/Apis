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
    },
    {
        "from": "Tokyo",
        "to": "Hokkaido (Sapporo)",
        "train": "Shinkansen + Hokkaido Shinkansen",
        "duration": "4h (Hayabusa + Hokkaido)",
        "price_jpy": 27760,
        "frequency": "Cada hora",
        "tips": "JR Pass cubre esta ruta. Es un viaje largo pero valioso."
    },
    {
        "from": "Osaka",
        "to": "Hokkaido (Sapporo)",
        "train": "Vuelo domestic (Peach/Jetstar)",
        "duration": "2h vuelo",
        "price_jpy": 5000,
        "frequency": "Varios vuelos diarios",
        "tips": "El vuelo es mas rapido y a veces mas barato que el tren."
    },
    {
        "from": "Fukuoka",
        "to": "Hiroshima",
        "train": "Shinkansen (Sakura)",
        "duration": "1h",
        "price_jpy": 8500,
        "frequency": "Cada 30 minutos",
        "tips": "JR Pass cubre esta ruta. Ruta muy turistica."
    },
    {
        "from": "Kyoto",
        "to": "Nara",
        "train": "JR Nara Line o Kintetsu",
        "duration": "45 min (JR) / 35 min (Kintetsu)",
        "price_jpy": 720,
        "frequency": "Cada 30 minutos",
        "tips": "Kintetsu es mas rapido pero no cubierto por JR Pass."
    }
]

AIRPORTS = [
    {
        "name": "Narita International Airport (NRT)",
        "city": "Tokyo",
        "code": "NRT",
        "distance_to_city": "60 km",
        "transport_to_city": [
            {"name": "Narita Express (JR)", "duration": "60 min", "price": 3250, "covered_by_jrpass": True},
            {"name": "Skyliner (Keisei)", "duration": "41 min", "price": 2520, "covered_by_jrpass": False},
            {"name": "Airport Limousine Bus", "duration": "85 min", "price": 3200, "covered_by_jrpass": False}
        ],
        "tips": "El Narita Express es la mejor opcion si tienes JR Pass."
    },
    {
        "name": "Haneda Airport (HND)",
        "city": "Tokyo",
        "code": "HND",
        "distance_to_city": "15 km",
        "transport_to_city": [
            {"name": "Keikyu Line", "duration": "15 min", "price": 300, "covered_by_jrpass": False},
            {"name": "Tokyo Monorail", "duration": "18 min", "price": 500, "covered_by_jrpass": True},
            {"name": "Bus", "duration": "30-60 min", "price": 1000, "covered_by_jrpass": False}
        ],
        "tips": "Haneda esta mucho mas cerca que Narita. Es mejor si vuelas domestico."
    },
    {
        "name": "Kansai International Airport (KIX)",
        "city": "Osaka",
        "code": "KIX",
        "distance_to_city": "50 km",
        "transport_to_city": [
            {"name": "JR Haruka", "duration": "50 min", "price": 3640, "covered_by_jrpass": True},
            {"name": "Nankai Rapi:t", "duration": "38 min", "price": 1450, "covered_by_jrpass": False},
            {"name": "Airport Limousine Bus", "duration": "70 min", "price": 1600, "covered_by_jrpass": False}
        ],
        "tips": "El Nankai Rapi:t es mas barato y rapidísimo. Diseño retro-futurista."
    },
    {
        "name": "New Chitose Airport (CTS)",
        "city": "Hokkaido (Sapporo)",
        "code": "CTS",
        "distance_to_city": "60 km",
        "transport_to_city": [
            {"name": "JR Rapid Airport", "duration": "37 min", "price": 1150, "covered_by_jrpass": True},
            {"name": "Bus", "duration": "80 min", "price": 1100, "covered_by_jrpass": False}
        ],
        "tips": "El aeropuerto tiene un acuario y un parque de nieve en invierno."
    },
    {
        "name": "Naha Airport (OKA)",
        "city": "Okinawa",
        "code": "OKA",
        "distance_to_city": "6 km",
        "transport_to_city": [
            {"name": "Yui Rail (monorail)", "duration": "15 min", "price": 270, "covered_by_jrpass": False},
            {"name": "Bus", "duration": "20-40 min", "price": 300, "covered_by_jrpass": False}
        ],
        "tips": "En Okinawa necesitas alquilar coche. El monorail solo va hasta Naha."
    },
    {
        "name": "Fukuoka Airport (FUK)",
        "city": "Fukuoka",
        "code": "FUK",
        "distance_to_city": "5 km",
        "transport_to_city": [
            {"name": "Subway", "duration": "5 min", "price": 260, "covered_by_jrpass": False},
            {"name": "Bus", "duration": "15 min", "price": 300, "covered_by_jrpass": False}
        ],
        "tips": "El aeropuerto mas cercano al centro de cualquier ciudad japonesa."
    }
]

CAR_RENTAL = {
    "description": "Alquilar coche en Japon es ideal para zonas rurales (Hokkaido, Okinawa, Nara).",
    "requirements": [
        "Permiso de conducir internacional (IDP)",
        "Pasaporte",
        "Tarjeta de credito",
        "Edad minima: 18-21 anos (varia por empresa)"
    ],
    "companies": [
        {"name": "Times Car Rental", "tip": "La mas popular y con mas sucursales"},
        {"name": "Nippon Rent-a-Car", "tip": "Buena calidad y servicio"},
        {"name": "Orix Rent-a-Car", "tip": "Precios competitivos"},
        {"name": "Toyota Rent-a-Car", "tip": "Coches nuevos y fiables"}
    ],
    "driving_tips": [
        "Conducir por la izquierda",
        "Los limites de velocidad son 60-80 km/h en carretera",
        "Las autopistas son caras pero rapidas",
        "El parking en ciudades es caro",
        "Los konbini tienen cajeros para pagar gasolina"
    ],
    "best_regions_for_driving": [
        {"region": "Hokkaido", "reason": "Carreteras vacias y paisajes increibles"},
        {"region": "Okinawa", "reason": "Sin tren, necesitas coche para moverte"},
        {"region": "Nara", "reason": "Para visitar templos remotos"},
        {"region": "Nagano", "reason": "Para acceder a los snow monkeys y templos"}
    ]
}



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


@router.get("/airports")
async def airports(
    city: Optional[str] = Query(None, description="Ciudad de Japon")
):
    if city:
        city_lower = city.lower()
        result = [a for a in AIRPORTS if city_lower in a["city"].lower()]
        return {"city": city, "airports": result}

    return {"total": len(AIRPORTS), "airports": AIRPORTS}


@router.get("/car-rental")
async def car_rental():
    return CAR_RENTAL
