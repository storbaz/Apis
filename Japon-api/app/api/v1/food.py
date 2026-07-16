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
