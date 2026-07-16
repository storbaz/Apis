from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/events", tags=["events-festivals"])


FESTIVALS_DATA = [
    {
        "name": "Hanami (Floracion de cerezos)",
        "name_jp": "花見",
        "season": "primavera",
        "months": ["marzo", "abril", "mayo"],
        "description": "Tradicion de contemplar la floracion de los cerezos. Se hacen picnic en parques bajo los arboles.",
        "best_cities": ["Tokyo", "Kyoto", "Osaka", "Hiroshima"],
        "dates_2026": "Marzo-Abril (varia por region)",
        "tips": [
            "Llega temano para conseguir buen lugar en Ueno Park (Tokyo)",
            "Los parques se llenan por la noche, pero la iluminacion es preciosa",
            "Trae mantas y comida para el picnic",
            "El sakura dura solo 1-2 semanas, revisa las previsiones"
        ]
    },
    {
        "name": "Matsuri de Kyoto",
        "name_jp": "祭り",
        "season": "verano",
        "months": ["julio", "agosto"],
        "description": "Festivales tradicionales con trajes yukata, comida callejera y desfiles.",
        "best_cities": ["Kyoto"],
        "dates_2026": "Julio-Agosto",
        "tips": [
            "Gion Matsuri en julio es el mas famoso",
            "Usa yukata (kimono ligero de verano)",
            "Prueba el kakigori (hielo raspa) y los takoyaki",
            "Los templos tienen eventos especiales nocturnos"
        ]
    },
    {
        "name": "Obon",
        "name_jp": "お盆",
        "season": "verano",
        "months": ["agosto"],
        "description": "Festival de los ancestros. Los japoneses regresan a sus ciudades nacionales. Hay danzas (Bon Odori) y lanternas.",
        "best_cities": "Todas",
        "dates_2026": "13-16 Agosto",
        "tips": [
            "Muchas tiendas cierran durante Obon",
            "Los precios de trenes y hoteles suben",
            "Las danzas Bon Odori son abiertas a todos",
            "Es una buena experiencia cultural unica"
        ]
    },
    {
        "name": "Olimpiadas de Tokyo",
        "name_jp": "オリンピック",
        "season": "verano",
        "months": ["julio", "agosto"],
        "description": "Si hay eventos deportivos internacionales, Tokyo se llena de actividades.",
        "best_cities": ["Tokyo"],
        "dates_2026": "Verificar calendario deportivo",
        "tips": [
            "Reserva con mucho antelacion",
            "Los eventos en vivo son increibles",
            "La ciudad se viste con decoraciones especiales"
        ]
    },
    {
        "name": "Festival de los Reyes",
        "name_jp": "節分",
        "season": "invierno",
        "months": ["febrero"],
        "description": "Dia de lanzar frijoles para espantar a los malos espiritus. Se celebra el 3 de febrero.",
        "best_cities": "Todas",
        "dates_2026": "3 Febrero",
        "tips": [
            "Los templos organizan eventos especiales",
            "Se come el ehomaki (sushi roll) entero sin cortar",
            "Los frijoles se compran en cualquier konbini",
            "Es una tradicion divertida y unica"
        ]
    },
    {
        "name": "Sanja Matsuri",
        "name_jp": "三社祭",
        "season": "primavera",
        "months": ["mayo"],
        "description": "Uno de los festivales de santuarios mas grandes de Tokyo. Desfiles con mikoshi (santuarios portatiles).",
        "best_cities": ["Tokyo"],
        "dates_2026": "Tercer fin de semana de Mayo",
        "tips": [
            "Se celebra en Asakusa, cerca del Templo Senso-ji",
            "Hay muchisima gente, ve temprano",
            "Los participants van semi-desnudos (es tradicional)",
            "La comida callejera es excelente"
        ]
    },
    {
        "name": "Kanda Matsuri",
        "name_jp": "神田祭",
        "season": "primavera",
        "months": ["mayo"],
        "description": "Festival historico de Tokyo con desfiles de mikoshi por el centro de la ciudad.",
        "best_cities": ["Tokyo"],
        "dates_2026": "Fines de semana de Mayo (varia)",
        "tips": [
            "Uno de los tres grandes festivales de Tokyo",
            "Los mikoshi pasan por Akihabara y Chiyoda",
            "Es menos turistico que Sanja Matsuri",
            "Buen momento para ver la vida local"
        ]
    },
    {
        "name": "Autumn Leaves (Momijigari)",
        "name_jp": "紅葉狩り",
        "season": "otoño",
        "months": ["octubre", "noviembre", "diciembre"],
        "description": "Tradicion de contemplar los arboles en otoño. Los parques y templos se llenan de rojos y naranjas.",
        "best_cities": ["Kyoto", "Nara", "Nikko", "Hakone"],
        "dates_2026": "Octubre-Diciembre (varia por region)",
        "tips": [
            "Kyoto es espectacular en Noviembre",
            "Los templos iluminados nocturnamente son magicos",
            "Nikko tiene los colores mas temprano (Octubre)",
            "Hakone es perfecto para ver hojas + onsen"
        ]
    }
]

SEASONS_DATA = {
    "primavera": {
        "name": "Primavera (Haru)",
        "months": ["marzo", "abril", "mayo"],
        "weather": "Suave, 10-20°C. Algo de lluvia en abril.",
        "highlights": ["Floracion de cerezos (Sakura)", "Hanami", "Temperaturas perfectas"],
        "what_to_wear": ["Ropa ligera", "Chaqueta fina", "Paraguas compacto"],
        "crowd_level": "Muy alto (temporada alta)",
        "prices": "Altas (especialmente hoteles en zona sakura)"
    },
    "verano": {
        "name": "Verano (Natsu)",
        "months": ["junio", "julio", "agosto"],
        "weather": "Caluroso y humedo, 25-35°C. Temporada de lluvias (junio) y tifones (agosto-septiembre).",
        "highlights": ["Festivales de verano (matsuri)", "Fuegos artificiales", "Playas de Okinawa"],
        "what_to_wear": ["Ropa muy ligera", "Protector solar", "Sombrero", "Toalla"],
        "crowd_level": "Medio (agosto es vacaciones nacionales)",
        "prices": "Medias-altas (Obon sube precios)"
    },
    "otono": {
        "name": "Otoño (Aki)",
        "months": ["septiembre", "octubre", "noviembre"],
        "weather": "Agradable, 15-25°C. Colores espectaculares en los arboles.",
        "highlights": ["Hoja roja (Momijigari)", "Cerveza de otoño", "Comida de temporada"],
        "what_to_wear": ["Capas", "Chaqueta ligera", "Bufanda fina"],
        "crowd_level": "Alto (especialmente Noviembre en Kyoto)",
        "prices": "Altas (especialmente Noviembre)"
    },
    "invierno": {
        "name": "Invierno (Fuyu)",
        "months": ["diciembre", "enero", "febrero"],
        "weather": "Frio, 0-10°C. Nieve en el norte (Hokkaido, Nagano).",
        "highlights": ["Iluminaciones navideñas", "Onsen (baños termales)", "Esqui en Niseko"],
        "what_to_wear": ["Ropa de abrigo", "Chaqueta gruesa", "Guantes", "Bufanda"],
        "crowd_level": "Bajo (excepto Año Nuevo)",
        "prices": "Bajas (excepto Navidad/Año Nuevo)"
    }
}


@router.get("/festivals")
async def festivals(
    season: Optional[str] = Query(None, description="primavera, verano, otoño, invierno"),
    city: Optional[str] = Query(None, description="Ciudad de Japon")
):
    result = FESTIVALS_DATA

    if season:
        result = [f for f in result if f["season"] == season.lower()]

    if city:
        result = [f for f in result if city.lower() in str(f["best_cities"]).lower()]

    return {
        "total": len(result),
        "festivals": result
    }


@router.get("/seasons")
async def seasons():
    return {
        "total": len(SEASONS_DATA),
        "seasons": list(SEASONS_DATA.values())
    }


@router.get("/seasons/{season}")
async def season_detail(season: str):
    season_lower = season.lower()
    if season_lower not in SEASONS_DATA:
        return {"error": f"Temporada '{season}' no encontrada. Usa: primavera, verano, otoño, invierno"}
    return SEASONS_DATA[season_lower]


@router.get("/city/{city}")
async def city_events(city: str):
    city_lower = city.lower()
    city_events = [f for f in FESTIVALS_DATA if city_lower in str(f["best_cities"]).lower()]

    return {
        "city": city,
        "total_events": len(city_events),
        "events": city_events
    }
