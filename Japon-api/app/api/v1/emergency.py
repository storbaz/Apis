from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/emergency", tags=["emergency-info"])


EMERGENCY_CONTACTS = {
    "general": {
        "police": {"number": "110", "description": "Policia"},
        "fire_ambulance": {"number": "119", "description": "Bomberos y Ambulancia"},
        "coast_guard": {"number": "118", "description": "Guardia Costera"},
        "general_emergency": {"number": "#7119", "description": "Emergencias generales (ingles disponible)"}
    },
    "tourist_help": {
        "jnto_hotline": {
            "number": "050-3816-2787",
            "description": "Japan National Tourism Organization - Atencion en ingles 24/7"
        },
        "helpline_japan": {
            "number": "03-5777-8989",
            "description": "Help Line for Foreign Visitors - Asistencia en multiples idiomas"
        },
        "tell_lifeline": {
            "number": "03-5774-0992",
            "description": "TELL Lifeline - Apoyo emocional en ingles"
        }
    },
    "embassies": {
        "spain": {
            "name": "Embajada de Espana en Japon",
            "phone": "+81-3-5798-6001",
            "address": "1-5-5 Mita, Minato-ku, Tokyo 108-8160",
            "website": "https://www.exteriores.gob.es/embajadas/tokio"
        },
        "mexico": {
            "name": "Embajada de Mexico en Japon",
            "phone": "+81-3-5411-0650",
            "address": "3-5-4 Mita, Minato-ku, Tokyo 108-0073",
            "website": "https://embamex.sre.gob.mx/japon"
        },
        "argentina": {
            "name": "Embajada de Argentina en Japon",
            "phone": "+81-3-5411-0650",
            "address": "3-5-4 Mita, Minato-ku, Tokyo 108-0073",
            "website": "https://www.argentina.gob.ar/japon"
        },
        "colombia": {
            "name": "Embajada de Colombia en Japon",
            "phone": "+81-3-5411-0650",
            "address": "3-5-4 Mita, Minato-ku, Tokyo 108-0073",
            "website": "https://www.cancilleria.gov.co"
        },
        "usa": {
            "name": "US Embassy in Japan",
            "phone": "+81-3-3224-5000",
            "address": "1-10-5 Akasaka, Minato-ku, Tokyo 107-8420",
            "website": "https://jp.usembassy.gov"
        },
        "uk": {
            "name": "British Embassy Tokyo",
            "phone": "+81-3-5211-1100",
            "address": "1-2 Ichiban-cho, Chiyoda-ku, Tokyo 102-8381",
            "website": "https://www.gov.uk/world/organisations/british-embassy-tokyo"
        }
    }
}

EMERGENCY_PHRASES = [
    {
        "japanese": "助けてください！",
        "romaji": "Tasukete kudasai!",
        "translation": "Ayuda, por favor!",
        "context": "Emergencia general"
    },
    {
        "japanese": "警察を呼んでください",
        "romaji": "Keisatsu wo yonde kudasai",
        "translation": "Llame a la policia",
        "context": "Crimen o accidente"
    },
    {
        "japanese": "病院に行きたいです",
        "romaji": "Byouin ni ikitai desu",
        "translation": "Quiero ir al hospital",
        "context": "Emergencia medica"
    },
    {
        "japanese": "水をください",
        "romaji": "Mizu wo kudasai",
        "translation": "Agua, por favor",
        "context": "Necesitas agua urgente"
    },
    {
        "japanese": "英語を話せる人はいますか？",
        "romaji": "Eigo wo hanaseru hito wa imasu ka?",
        "translation": "Hay alguien que hable ingles?",
        "context": "Necesitas comunicarte en ingles"
    },
    {
        "japanese": "パスポートをなくしました",
        "romaji": "Pasupooto wo nakushimashita",
        "translation": "Perdi mi pasaporte",
        "context": "Pasaporte perdido o robado"
    },
    {
        "japanese": "薬が必要です",
        "romaji": "Kusuri ga hitsuyou desu",
        "translation": "Necesito medicinas",
        "context": "Necesitas medicacion"
    },
    {
        "japanese": "火事です！",
        "romaji": "Kaji desu!",
        "translation": "Fuego!",
        "context": "Incendio"
    },
    {
        "japanese": "地震が怖いです",
        "romaji": "Jishin ga kowai desu",
        "translation": "Tengo miedo del terremoto",
        "context": "Durante un terremoto"
    },
    {
        "japanese": "どこに避難すればいいですか？",
        "romaji": "Doko ni hinan sureba ii desu ka?",
        "translation": "Donde debo refugiarme?",
        "context": "Buscando lugar seguro"
    }
]

HOSPITALS_INFO = {
    "tokyo": [
        {
            "name": "Tokyo Adventist Hospital",
            "address": "2-22-1 Mejiro, Toshima-ku, Tokyo",
            "phone": "+81-3-3941-1111",
            "english_available": True,
            "specialties": ["General", "Emergency"]
        },
        {
            "name": "St. Luke's International Hospital",
            "address": "9-1 Akashi-cho, Chuo-ku, Tokyo",
            "phone": "+81-3-3541-5151",
            "english_available": True,
            "specialties": ["General", "International Patients"]
        }
    ],
    "osaka": [
        {
            "name": "Osaka University Hospital",
            "address": "2-15 Yamadaoka, Suita, Osaka",
            "phone": "+81-6-6879-5111",
            "english_available": True,
            "specialties": ["General", "Emergency"]
        }
    ],
    "kyoto": [
        {
            "name": "Kyoto University Hospital",
            "address": "54 Kawahara-cho, Shogoin, Sakyo-ku, Kyoto",
            "phone": "+81-75-751-3111",
            "english_available": True,
            "specialties": ["General", "Emergency"]
        }
    ]
}

HEALTH_TIPS = [
    {
        "title": "Seguro de viaje",
        "description": "Es OBLIGATORIO tener seguro de viaje. Los hospitals japoneses son caros sin seguro.",
        "importance": "critica"
    },
    {
        "title": "Mapa con el hospital",
        "description": "Guarda la direccion del hospital mas cercano a tu hotel en tu telefono.",
        "importance": "alta"
    },
    {
        "title": "Botiquin basico",
        "description": "Lleva medicinas basicas: analgesicos, antidiarreicos, antihistaminicos, vendas.",
        "importance": "media"
    },
    {
        "title": "Agua del grifo",
        "description": "El agua del grifo en Japon es potable y segura de beber.",
        "importance": "baja"
    },
    {
        "title": "Alergias alimentarias",
        "description": "Si tienes alergias, lleva una tarjeta traducida al japonero.",
        "importance": "alta"
    }
]


@router.get("/contacts")
async def emergency_contacts():
    return EMERGENCY_CONTACTS


@router.get("/phrases")
async def emergency_phrases():
    return {
        "total": len(EMERGENCY_PHRASES),
        "phrases": EMERGENCY_PHRASES
    }


@router.get("/hospitals")
async def hospitals(
    city: Optional[str] = Query(None, description="Ciudad de Japon")
):
    if city:
        city_lower = city.lower()
        if city_lower in HOSPITALS_INFO:
            return {
                "city": city,
                "hospitals": HOSPITALS_INFO[city_lower]
            }
        return {"error": f"Ciudad '{city}' no encontrada en la base de datos de hospitales"}

    return {
        "total_cities": len(HOSPITALS_INFO),
        "hospitals": HOSPITALS_INFO
    }


@router.get("/tips")
async def health_tips():
    return {
        "total": len(HEALTH_TIPS),
        "tips": HEALTH_TIPS
    }


@router.get("/embassies/{country}")
async def embassy_info(country: str):
    country_lower = country.lower()
    if country_lower in EMERGENCY_CONTACTS["embassies"]:
        return EMERGENCY_CONTACTS["embassies"][country_lower]
    return {"error": f"Embajada de '{country}' no encontrada. Paises disponibles: {list(EMERGENCY_CONTACTS['embassies'].keys())}"}
