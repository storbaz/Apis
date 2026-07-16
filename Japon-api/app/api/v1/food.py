from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/food", tags=["food-restaurant"])


FOOD_GUIDE = {
    "tokyo": {
        "city": "Tokyo",
        "specialties": [
            {
                "name": "Sushi",
                "description": "El sushi de Tokyo es considerado el mejor del mundo. Prueba el sushi de Tsukiji.",
                "where": ["Tsukiji Outer Market", "Ginza", "Roppongi"],
                "price_range": "$$-$$$$",
                "tip": "Los conveyor belt sushi (kaitenzushi) son baratos y divertidos"
            },
            {
                "name": "Ramen",
                "description": "Cada barrio tiene su estilo de ramen. Shinjuku es famoso por los ramen shops.",
                "where": ["Shinjuku", "Shibuya", "Ikebukuro"],
                "price_range": "$-$$",
                "tip": "Busca los restaurants con cola, son los mas populares"
            },
            {
                "name": "Tempura",
                "description": "Mariscos y verduras rebozadas y fritas. El tempura de Tokyo es ligero y crujiente.",
                "where": ["Ginza", "Asakusa"],
                "price_range": "$$-$$$$",
                "tip": "Los restaurantes de tempura suelen ser counter-style, es una experiencia"
            }
        ]
    },
    "osaka": {
        "city": "Osaka",
        "specialties": [
            {
                "name": "Takoyaki",
                "description": "Bolas de pulpo fritas, el snack mas famoso de Osaka.",
                "where": ["Dotonbori", "Shinsaibashi"],
                "price_range": "$",
                "tip": "Los puestos de Dotonbori son los mas famosos, pero prueba los de los barrios laterales"
            },
            {
                "name": "Okonomiyaki",
                "description": "Tortilla japonesa con repollo, carne, mariscos. Se cocina en la mesa.",
                "where": ["Dotonbori", "Namba"],
                "price_range": "$-$$",
                "tip": "En Osaka es 'osaka-style' (mezclado), en Hiroshima es en capas"
            },
            {
                "name": "Kushikatsu",
                "description": "Brochetas fritas de todo tipo. El mas famoso es en Shinsekai.",
                "where": ["Shinsekai", "Tennoji"],
                "price_range": "$",
                "tip": "NUNCA doblees la salsa! Usa el plato para echar salsa"
            }
        ]
    },
    "kyoto": {
        "city": "Kyoto",
        "specialties": [
            {
                "name": "Kaiseki",
                "description": "Cocina tradicional japonesa en multiples platos pequeños y elegantes.",
                "where": ["Gion", "Pontocho"],
                "price_range": "$$$$",
                "tip": "Es una experiencia gastronomica, no solo una comida"
            },
            {
                "name": "Tofu",
                "description": "Kyoto es famosa por su tofu de calidad. Prueba el yudofu (tofu hervido).",
                "where": ["Nanzenji", "Arashiyama"],
                "price_range": "$$",
                "tip": "El tofu de Kyoto es diferente al que conoces, es suave y delicado"
            },
            {
                "name": "Matcha y Dulces",
                "description": "Kyoto es la capital del matcha. Prueba los wagashi (dulces tradicionales).",
                "where": ["Uji", "Arashiyama"],
                "price_range": "$-$$",
                "tip": "El matcha de Uji es el mejor. Hay cafes dedicados solo a matcha"
            }
        ]
    },
    "hiroshima": {
        "city": "Hiroshima",
        "specialties": [
            {
                "name": "Okonomiyaki Hiroshima-style",
                "description": "En capas (no mezclado como en Osaka). Con fideos, huevo y mucho mas.",
                "where": ["Hondori", "Okonomimura"],
                "price_range": "$$",
                "tip": "Okonomimura tiene 24 floors de restaurantes de okonomiyaki"
            },
            {
                "name": "Oysters",
                "description": "Hiroshima produce el 60% de las ostras de Japon. Frescas y deliciosas.",
                "where": ["Miyajima", "Costa de Hiroshima"],
                "price_range": "$$-$$$$",
                "tip": "Las ostras a la parrilla son imperdibles"
            }
        ]
    },
    "fukuoka": {
        "city": "Fukuoka",
        "specialties": [
            {
                "name": "Ramen Tonkotsu",
                "description": "El ramen de caldo de cerdo mas famoso de Japon. Origen de Fukuoka.",
                "where": ["Yatai (carritos)", "Tenjin", "Nakasu"],
                "price_range": "$",
                "tip": "Los yatai (carritos callejeros) son la mejor forma de probarlo"
            },
            {
                "name": "Mentaiko",
                "description": "Huevas de pescado especiadas. El souvenir mas famoso de Fukuoka.",
                "where": "Cualquier tienda",
                "price_range": "$",
                "tip": "Cómpralo para llevar y comer en el avion"
            }
        ]
    },
    "hokkaido": {
        "city": "Hokkaido",
        "specialties": [
            {
                "name": "Mariscos frescos",
                "description": "Cangrejo, pulpo, salmon, uni (erizo). Los mas frescos de Japon.",
                "where": ["Sapporo", "Otaru", "Hakodate"],
                "price_range": "$$-$$$$",
                "tip": "El mercado de Nijo en Sapporo tiene los mejores precios"
            },
            {
                "name": "Genghis Khan (Jingisukan)",
                "description": "Cordero a la parrilla en forma de domo. Plato tipico de Hokkaido.",
                "where": ["Sapporo", "Odori Park"],
                "price_range": "$$",
                "tip": "Es una experiencia communal, se come en grupo"
            },
            {
                "name": "Ramen Miso",
                "description": "El ramen de miso de Sapporo es el mas famoso de Japon.",
                "where": ["Sapporo", "Ramen Yokocho"],
                "price_range": "$",
                "tip": "Ramen Yokocho tiene docenas de shops en una calle"
            }
        ]
    },
    "okinawa": {
        "city": "Okinawa",
        "specialties": [
            {
                "name": "Rafute",
                "description": "Cerdo estofado en salsa de soja y awamori. Plato tradicional Ryukyu.",
                "where": ["Naha", "Kokusai Dori"],
                "price_range": "$$",
                "tip": "La cocina de Okinawa es muy diferente a la japonesa"
            },
            {
                "name": "Soki Soba",
                "description": "Fideos con costillas de cerdo. El plato mas popular de Okinawa.",
                "where": ["Naha", "Toda"],
                "price_range": "$",
                "tip": "No confundir con el ramen, es un plato distinto"
            },
            {
                "name": "Taco Rice",
                "description": "Arroz con taco de carne molida. Fusion americano-japonesa.",
                "where": ["Chatan", "Araha Beach"],
                "price_range": "$",
                "tip": "Nacido de la influencia militar americana"
            }
        ]
    },
    "nara": {
        "city": "Nara",
        "specialties": [
            {
                "name": "Kakinoha Sushi",
                "description": "Sushi envuelto en hojas de kaki (caqui). Conservacion natural.",
                "where": ["Naramachi", "Estacion de Nara"],
                "price_range": "$$",
                "tip": "Es el souvenir gastronomico mas tipico de Nara"
            },
            {
                "name": "Miwa Somen",
                "description": "Fideos finos de la zona de Miwa. Los mejores de Japon.",
                "where": ["Miwa", "Sakurai"],
                "price_range": "$$",
                "tip": "Se sirven frios en verano, calientes en invierno"
            }
        ]
    },
    "kanazawa": {
        "city": "Kanazawa",
        "specialties": [
            {
                "name": "Kaisen Don",
                "description": "Bol de arroz con mariscos frescos del Mar de Japon.",
                "where": ["Omicho Market", "Korinbo"],
                "price_range": "$$-$$$$",
                "tip": "Omicho Market tiene los mejores precios y frescura"
            },
            {
                "name": "Jibuni",
                "description": "Pato estofado con wasabi y gluten. Plato tipico de Kanazawa.",
                "where": ["Restaurante tradicionales"],
                "price_range": "$$",
                "tip": "Es un plato antiguo que no encontraras en otro sitio"
            },
            {
                "name": "Gold Leaf Ice Cream",
                "description": "Helado cubierto con hoja de oro comestible. Especalidad local.",
                "where": ["Higashi Chaya", "Kenroku-en"],
                "price_range": "$",
                "tip": "Kanazawa produce el 99% del oro leaf de Japon"
            }
        ]
    }
}

KONBINI_GUIDE = {
    "description": "Los konbini (tiendas de conveniencia) son una experiencia gastronomica en si mismos. Tienen comida de calidad a precios bajos.",
    "chains": [
        {
            "name": "7-Eleven",
            "specialties": ["Onigiri", "Sandwiches de huevo", "Oden", "Cafe"],
            "tip": "Los onigiri son los mejores de todos los konbini"
        },
        {
            "name": "FamilyMart",
            "specialties": ["Famichiki (pollo frito)", "Melon pan", "Takoyaki"],
            "tip": "El Famichiki es el pollo frito mas famoso de Japon"
        },
        {
            "name": "Lawson",
            "specialties": ["Uchi cafe (dulces)", "Edamame", "Oyakodon"],
            "tip": "Los postres Uchi Cafe son sorprendentemente buenos"
        },
        {
            "name": "Mini Stop",
            "specialties": ["Soft serve", "Bento economicos", "Cafe"],
            "tip": "El soft serve es famoso por su calidad"
        }
    ],
    "best_items": [
        {"name": "Onigiri", "price": "120-180 yen", "description": "Bolas de arroz con relleno. El snack perfecto."},
        {"name": "Bento", "price": "400-800 yen", "description": "Cajas de comida completas. Mejor opcion barata."},
        {"name": "Oden", "price": "100-200 yen", "description": "Caldo caliente con verduras y carne. Perfecto en invierno."},
        {"name": "Egg sandwich", "price": "200-300 yen", "description": "El sandwich de huevo de konbini es leggendario."},
        {"name": "Famichiki", "price": "200-300 yen", "description": "Pollo frito crujiente. El mejor snack de convenience store."},
        {"name": "Strong Zero", "price": "150-200 yen", "description": "Chu-hai (bebida alcoholica) fuerte y barata. Cuidado!"}
    ]
}

DIETARY_OPTIONS = {
    "vegan": {
        "description": "Japon no es facil para veganos, pero hay opciones",
        "options": [
            {"name": "Shojin Ryori", "description": "Cocina budista, 100% vegetal. Templos en Kyoto."},
            {"name": "Tofu dishes", "description": "Kyoto es el mejor lugar para tofu vegano."},
            {"name": "Vegetable tempura", "description": "Verduras fritas. Pide que no usen dashi."},
            {"name": "Ramen vegano", "description": "Algunos shops tienen opciones de caldo de vegetales."},
            {"name": "Konbini options", "description": "Busca 'yasai' (verduras) en los konbini."}
        ],
        "tips": [
            "Aprende a decir 'bejitarian desu' (soy vegetariano)",
            "El dashi (caldo base) usualmente tiene pescado",
            "En Kyoto hay mas opciones veganas que en cualquier otra ciudad",
            "Descarga HappyCow para encontrar restaurants veganos"
        ]
    },
    "gluten_free": {
        "description": "Japon usa mucho gluten, pero hay opciones naturales",
        "options": [
            {"name": "Sushi", "description": "Naturalmente sin gluten (cuidado con la soja)."},
            {"name": "Yakitori", "description": "Pollo a la parrilla. Pide sin salsa tare."},
            {"name": "Grilled fish", "description": "Pescado a la parrilla. Naturalmente seguro."},
            {"name": "Rice dishes", "description": "Arroz, onigiri, sushi. Base segura."},
            {"name": "Tamagoyaki", "description": "Tortilla japonesa. Generalmente segura."}
        ],
        "tips": [
            "Aprende 'mu-tan' (sin trigo) y 'guten furi' (sin gluten)",
            "El shoyu (soja) contiene trigo, busca 'tamari' (sin trigo)",
            "Los fideos de arroz son seguros",
            "Muchos restaurants modernos tienen opciones sin gluten"
        ]
    }
}



ETIQUETTA_RESTAURANTES = [
    {
        "title": "Entrar al restaurante",
        "description": "En la entrada suele haber un mostrador o maquina de tickets. Espera a que te lleven a tu mesa.",
        "importance": "alta"
    },
    {
        "title": "Usar la maquina de tickets (tiket shop)",
        "description": "Muchos ramen shops y fukado tienen maquinas. Selecciona tu plato, paga, y entrega el ticket al cocinero.",
        "importance": "alta"
    },
    {
        "title": "No pedir agua",
        "description": "En Japon te traen automaticamente agua o te (usually gratis). No necesitas pedirla.",
        "importance": "media"
    },
    {
        "title": "Comer ramen con ruido",
        "description": "Hacer ruido al comer ramen es normal y se considera un halago al cocinero.",
        "importance": "media"
    },
    {
        "title": "Terminar TODO",
        "description": "Dejar la comida sin terminar es de mala educacion. Si no puedes, pide disculpas.",
        "importance": "alta"
    },
    {
        "title": "No pedir caja para llevar",
        "description": "La mayoria de restaurants japoneses no ofrecen caja para llevar. Come todo en el local.",
        "importance": "media"
    },
    {
        "title": "Saber decir que no",
        "description": "Si no te gusta algo, puedes decir 'kekkou desu' (estoy bien, gracias) sin ser grosero.",
        "importance": "baja"
    }
]


@router.get("/guide")
async def food_guide(
    city: Optional[str] = Query(None, description="Ciudad de Japon")
):
    if city:
        city_lower = city.lower()
        if city_lower in FOOD_GUIDE:
            return FOOD_GUIDE[city_lower]
        return {"error": f"Ciudad '{city}' no encontrada en la guia gastronomica"}

    return {
        "total_cities": len(FOOD_GUIDE),
        "cities": list(FOOD_GUIDE.keys()),
        "guide": FOOD_GUIDE
    }


@router.get("/guide/{city}")
async def city_food_guide(city: str):
    city_lower = city.lower()
    if city_lower not in FOOD_GUIDE:
        return {"error": f"Ciudad '{city}' no encontrada. Ciudades disponibles: {list(FOOD_GUIDE.keys())}"}
    return FOOD_GUIDE[city_lower]


@router.get("/etiquette")
async def food_etiquette():
    return {
        "total": len(ETIQUETTA_RESTAURANTES),
        "rules": ETIQUETTA_RESTAURANTES
    }


@router.get("/dishes")
async def all_dishes():
    all_dishes_list = []
    for city_data in FOOD_GUIDE.values():
        for dish in city_data["specialties"]:
            dish_with_city = dish.copy()
            dish_with_city["city"] = city_data["city"]
            all_dishes_list.append(dish_with_city)

    return {
        "total": len(all_dishes_list),
        "dishes": all_dishes_list
    }


@router.get("/konbini")
async def konbini_guide():
    return KONBINI_GUIDE


@router.get("/dietary")
async def dietary_options():
    return DIETARY_OPTIONS
