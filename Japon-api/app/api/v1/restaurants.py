from fastapi import APIRouter

router = APIRouter(prefix="/restaurants", tags=["restaurants-guides"])

RESTAURANTS = {
    "tokyo": [
        {"name": "Ichiran Ramen", "type": "ramen", "area": "Shibuya", "price": "bajo", "avg_price_jpy": 1000, "rating": 4.5, "description": "Ramen tonkotsu personal en cabinas individuales. Experiencia única.", "must_try": "Ramen original", "hours": "24h", "tip": "Usa la máquina expendedora para pedir"},
        {"name": "Fuunji", "type": "ramen", "area": "Shinjuku", "price": "bajo", "avg_price_jpy": 900, "rating": 4.6, "description": "Tsukemen (noodles con caldo aparte) legendary. Cola larga pero vale la pena.", "must_try": "Tsukemen", "hours": "11:00-15:00, 17:00-21:00", "tip": "Ve antes de abrir para evitar la cola"},
        {"name": "Gonpachi", "type": "izakaya", "area": "Nishi-Azabu", "price": "medio", "avg_price_jpy": 3500, "rating": 4.3, "description": "Izakaya que inspiró la escena de Kill Bill. Ambiente espectacular.", "must_try": "Soba hand-made", "hours": "11:30-03:00", "tip": "Reserva para cenar"},
        {"name": "Sushi Dai", "type": "sushi", "area": "Toyosu", "price": "medio", "avg_price_jpy": 4000, "rating": 4.7, "description": "Uno de los mejores sushi de Tokyo. Cola de 1-2 horas.", "must_try": "Omakase (menú del chef)", "hours": "05:00-14:00", "tip": "Llega a las 5am para evitar la cola"},
        {"name": "Afuri Ramen", "type": "ramen", "area": "Ebisu", "price": "bajo", "avg_price_jpy": 1100, "rating": 4.4, "description": "Ramen yuzu shio, ligero y cítrico. Perfecto para el calor.", "must_try": "Yuzu Shio Ramen", "hours": "11:00-23:00", "tip": "Prueba el huevo ajitsuke"},
        {"name": "Uobei Shibuya", "type": "sushi", "area": "Shibuya", "price": "bajo", "avg_price_jpy": 1500, "rating": 4.2, "description": "Sushi por conveyor belt a 100¥/plato. Pedido por pantalla táctil.", "must_try": "Salmón, atún, camarón", "hours": "11:00-23:00", "tip": "Perfecto para niños y presupuestos ajustados"},
        {"name": "Tsunahachi", "type": "tempura", "area": "Shinjuku", "price": "medio", "avg_price_jpy": 2500, "rating": 4.3, "description": "Tempura desde 1923. Camarones gigantes y verduras crujientes.", "must_try": "Tempura omakase", "hours": "11:30-14:30, 17:00-21:00", "tip": "Pide asientos en la barra para ver la preparación"},
        {"name": "Nakajima", "type": "kaiseki", "area": "Yotsuya", "price": "alto", "avg_price_jpy": 8000, "rating": 4.8, "description": "Kaiseki (cena tradicional) de nivel Michelin a precio accesible.", "must_try": "Lunch kaiseki", "hours": "11:30-14:00, 17:00-21:00", "tip": "El lunch es mucho más barato que la cena"},
        {"name": "CoCo Ichibanya", "type": "curry", "area": "varias", "price": "bajo", "avg_price_jpy": 800, "rating": 4.1, "description": "Curry japonés personalizable. Elige tu picante del 1 al 10.", "must_try": "Curry con chorizo y arroz", "hours": "11:00-23:00", "tip": "Nivel 3-4 de picante es perfecto para empezar"},
        {"name": "Gyukatsu Motomura", "type": "gyukatsu", "area": "Shinjuku", "price": "medio", "avg_price_jpy": 1700, "rating": 4.6, "description": "Gyukatsu (filete de ternera empanizado) que tú mismo sellas en piedra caliente.", "must_try": "Gyukatsu set completo", "hours": "11:30-15:00, 17:00-21:30", "tip": "El primer bocado, cómetelo sin cocinar para probar el sabor original"},
    ],
    "osaka": [
        {"name": "Takoyaki Wanaka", "type": "street-food", "area": "Dotonbori", "price": "bajo", "avg_price_jpy": 500, "rating": 4.5, "description": "Los mejores takoyaki de Osaka. Crujientes por fuera, cremosos por dentro.", "must_try": "Takoyaki con bonito", "hours": "11:00-22:00", "tip": "Cuidado, están muy calientes"},
        {"name": "Kushikatsu Daruma", "type": "kushikatsu", "area": "Shinsaibashi", "price": "bajo", "avg_price_jpy": 1500, "rating": 4.4, "description": "Kushikatsu (brochetas fritas) con la regla de oro: ¡NO doble dipping!", "must_try": "Set de kushikatsu variados", "hours": "11:00-23:00", "tip": "Usa la cebolla del barro para re-sazonar"},
        {"name": "Mizuno", "type": "okonomiyaki", "area": "Dotonbori", "price": "medio", "avg_price_jpy": 1500, "rating": 4.6, "description": "Okonomiyaki desde 1945. Ambos estilos: Osaka y Hiroshima.", "must_try": "Okonomiyaki de mariscos", "hours": "11:30-22:00", "tip": "Ve temprano o reserva online"},
        {"name": "Harukoma Sushi", "type": "sushi", "area": "Tenma", "price": "medio", "avg_price_jpy": 2500, "rating": 4.7, "description": "Sushi de conveyor belt de alta calidad. Los locales lo adoran.", "must_try": "Atún otoro", "hours": "11:00-22:00", "tip": "No tiene reserva, llega temprano"},
        {"name": "Kani Doraku", "type": "cangrejo", "area": "Dotonbori", "price": "alto", "avg_price_jpy": 5000, "rating": 4.3, "description": "El icónico restaurante del cangrejo gigante. Comida de cangrejo premium.", "must_try": "Kani course", "hours": "11:30-22:00", "tip": "El exterior es gratis para fotos"},
    ],
    "kyoto": [
        {"name": "Nishiki Market", "type": "street-food", "area": "Nishiki", "price": "bajo", "avg_price_jpy": 1000, "rating": 4.5, "description": "El mercado de 400 años. Street food, pickles, dulces, y más.", "must_try": "Yuba (tofu skin), tsukemono", "hours": "09:00-17:00", "tip": "Ve con hambre y prueba todo"},
        {"name": "Omen", "type": "udon", "area": "Ginkakuji", "price": "medio", "avg_price_jpy": 1800, "rating": 4.4, "description": "Udon artesanal con vegetales de temporada en caldo dashi.", "must_try": "Omen udon con tempura", "hours": "11:00-14:30, 17:00-20:30", "tip": "Cerca del Silver Pavilion, combina las dos visitas"},
        {"name": "Kichi Kichi Omurice", "type": "omurice", "area": "Gion", "price": "medio", "avg_price_jpy": 4000, "rating": 4.7, "description": "El famoso omurice de YouTube. Show en vivo del chef cortando el huevo.", "must_try": "Omurice premium", "hours": "11:30-14:00, 17:00-20:00", "tip": "Reserva con semanas de antelación"},
        {"name": "Gogyo Ramen", "type": "ramen", "area": "Nishikiyamachi", "price": "bajo", "avg_price_jpy": 1000, "rating": 4.3, "description": "Ramen kogashi (quemado) con caldo de miso carbonizado. Sabor único.", "must_try": "Kogashi miso ramen", "hours": "11:30-14:30, 17:00-23:00", "tip": "El caldo se prepara a la orden, ten paciencia"},
    ],
    "hakone": [
        {"name": "Hakone Bakery", "type": "panaderia", "area": "Hakone-Yumoto", "price": "bajo", "avg_price_jpy": 500, "rating": 4.3, "description": "Pan artesanal recién horneado. Perfecto para un desayuno rápido.", "must_try": "Pan de matcha", "hours": "08:00-15:00", "tip": "Llega temprano, se agota rápido"},
    ],
    "nara": [
        {"name": "Kakinoha Sushi", "type": "sushi", "area": "Naramachi", "price": "medio", "avg_price_jpy": 2000, "rating": 4.4, "description": "Sushi envuelto en hojas de caqui, tradición local de 700 años.", "must_try": "Kakinoha sushi set", "hours": "10:00-17:00", "tip": "Perfecto para llevar de recuerdo"},
    ],
    "hiroshima": [
        {"name": "Nagata-ya", "type": "okonomiyaki", "area": "Hondori", "price": "bajo", "avg_price_jpy": 1200, "rating": 4.7, "description": "Okonomiyaki estilo Hiroshima (capas, no mezclado). El mejor de la ciudad.", "must_try": "Okonomiyaki con fideos", "hours": "11:00-00:00", "tip": "El chef es rápido, respeta su proceso"},
    ],
    "fukuoka": [
        {"name": "Yatai (puestos de calle)", "type": "street-food", "area": "Nakasu", "price": "bajo", "avg_price_jpy": 1000, "rating": 4.6, "description": "Puestos de ramen y street food a orillas del río Nakasu. Experiencia nocturna única.", "must_try": "Hakata ramen", "hours": "18:00-02:00", "tip": "Los yatai solo aceptan efectivo"},
        {"name": "Shin Shin", "type": "ramen", "area": "Tenjin", "price": "bajo", "avg_price_jpy": 800, "rating": 4.5, "description": "Ramen tonkotsu cremoso. Popular entre locales.", "must_try": "Hakata ramen con kaedama (extra noodles)", "hours": "11:00-02:00", "tip": "Puedes pedir la dureza de los noodles"},
    ],
}


@router.get("/guide")
async def get_restaurants(city: str = None):
    """Guía de restaurantes recomendados por ciudad"""
    if city:
        city_lower = city.lower()
        if city_lower in RESTAURANTS:
            return {"city": city_lower, "restaurants": RESTAURANTS[city_lower]}
        return {"available_cities": list(RESTAURANTS.keys()), "message": f"Ciudad '{city}' no encontrada"}

    all_restaurants = []
    for c, restaurants in RESTAURANTS.items():
        for r in restaurants:
            all_restaurants.append({**r, "city": c})
    return {"restaurants": all_restaurants, "cities": list(RESTAURANTS.keys()), "total": len(all_restaurants)}


@router.get("/guide/{city}")
async def get_restaurants_by_city(city: str):
    """Restaurantes de una ciudad específica"""
    city_lower = city.lower()
    if city_lower in RESTAURANTS:
        return {"city": city_lower, "restaurants": RESTAURANTS[city_lower]}
    return {"available_cities": list(RESTAURANTS.keys()), "message": f"Ciudad '{city}' no encontrada"}


@router.get("/types")
async def get_restaurant_types():
    """Tipos de restaurante disponibles"""
    types = set()
    for restaurants in RESTAURANTS.values():
        for r in restaurants:
            types.add(r["type"])
    return {"types": sorted(list(types))}
