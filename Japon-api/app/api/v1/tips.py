from fastapi import APIRouter

router = APIRouter(prefix="/tips", tags=["tips-savings"])

SAVING_TIPS = [
    {
        "id": "transport-1",
        "category": "transporte",
        "title": "JR Pass: ¿Te conviene?",
        "description": "El JR Pass de 7 días cuesta ~50,000¥. Solo conviene si vas a hacer al menos 2 viajes largos (Tokio-Kyoto ida y vuelta = ~26,000¥ cada uno). Para solo Tokio, usa Suica/Pasmo.",
        "savings": "Hasta 20,000¥ si lo usas bien",
        "icon": "🚄"
    },
    {
        "id": "transport-2",
        "category": "transporte",
        "title": "Usa buses nocturnos",
        "description": "Los buses nocturnos de Willer Express cuestan desde 2,000¥ por trayectos que en tren cuestan 10,000¥+. Ahorras hotel y transporte a la vez.",
        "savings": "8,000-15,000¥ por trayecto",
        "icon": "🚌"
    },
    {
        "id": "transport-3",
        "category": "transporte",
        "title": "Camina en las estaciones",
        "description": "Las estaciones de Tokyo son enormes. Moverse de una línea a otra puede costarte 500¥ extra. Planifica para bajar en la estación correcta.",
        "savings": "500-1000¥ por día",
        "icon": "🚶"
    },
    {
        "id": "comida-1",
        "category": "comida",
        "title": "Almuerzo del día (ランチ)",
        "description": "Muchos restaurantes ofrecen lunch sets por 800-1200¥ que en la noche cuestan 2000-3000¥. Misma calidad, mitad de precio.",
        "savings": "1000-2000¥ por comida",
        "icon": "🍱"
    },
    {
        "id": "comida-2",
        "category": "comida",
        "title": "Konbini: tu mejor amigo",
        "description": "7-Eleven, FamilyMart y Lawson tienen comidas calientes de calidad por 300-700¥. Onigiri (120¥), bento (500¥), ramen (500¥).",
        "savings": "1000-2000¥ por día",
        "icon": "🏪"
    },
    {
        "id": "comida-3",
        "category": "comida",
        "title": "Agua del grifo es segura",
        "description": "El agua de Japón es perfectly potable. Lleva una botella reutilizable y ahorra 150¥ por botella que tomes.",
        "savings": "500-1000¥ por día",
        "icon": "💧"
    },
    {
        "id": "comida-4",
        "category": "comida",
        "title": "Supermercado con descuento nocturno",
        "description": "Después de las 7-8pm, los supermercados ponen stickers de descuento (20-50% off) en bentos, sushi y comida preparada.",
        "savings": "500-1500¥ por cena",
        "icon": "🏷️"
    },
    {
        "id": "comida-5",
        "category": "comida",
        "title": "Cadena de fideos baratos",
        "description": "Ichiran, Ippudo y otros chains tienen ramen desde 800¥. Los independentes suelen estar en 1000-1500¥.",
        "savings": "200-700¥ por comida",
        "icon": "🍜"
    },
    {
        "id": "alojamiento-1",
        "category": "alojamiento",
        "title": "Hostels y cápsulas",
        "description": "Los hostels cuestan 2500-4000¥/noche. Las cápsulas 3000-5000¥. Un hotel normal: 8000-15000¥.",
        "savings": "4000-10000¥ por noche",
        "icon": "🛏️"
    },
    {
        "id": "alojamiento-2",
        "category": "alojamiento",
        "title": "Airbnb fuera del centro",
        "description": "Un Airbnb a 15 min del centro puede costar la mitad que uno en Shinjuku o Shibuya. Japón tiene excelente transporte.",
        "savings": "3000-8000¥ por noche",
        "icon": "🏠"
    },
    {
        "id": "alojamiento-3",
        "category": "alojamiento",
        "title": "Manga cafes para emergencias",
        "description": "Los manga cafes (jugem-teru) ofrecen cabinas privadas con sofá, ducha y bebidas ilimitadas por 2000-3000¥ toda la noche.",
        "savings": "5000-8000¥ por noche",
        "icon": "📚"
    },
    {
        "id": "compras-1",
        "category": "compras",
        "title": "Tax-free para extranjeros",
        "description": "Si gastas más de 5000¥ en una tienda, puedes pedir tax-free (10% de descuento). Lleva tu pasaporte.",
        "savings": "10% de tus compras",
        "icon": "🛂"
    },
    {
        "id": "compras-2",
        "category": "compras",
        "title": "100-yen shops (Daiso, Can Do)",
        "description": "Todo a 100¥ (100-yen shops). Souvenirs, útiles, snacks, accesorios de viaje. Perfecto para no gastar de más.",
        "savings": "Cientos de yen por compra",
        "icon": "🏪"
    },
    {
        "id": "compras-3",
        "category": "compras",
        "title": "Don Quijote para souvenirs",
        "description": "Don Quijote tiene los mejores precios en snacks, cosmetics y souvenirs. Pide su cupón de descuento de 5% para turistas.",
        "savings": "5% extra de descuento",
        "icon": "🐧"
    },
    {
        "id": "general-1",
        "category": "general",
        "title": " ATM de 7-Eleven",
        "description": "Los cajeros de 7-Eleven aceptan tarjetas internacionales. Evita los cajeros de bancos normales que pueden cobrar comisión.",
        "savings": "Evitas comisiones de 200-500¥",
        "icon": "🏧"
    },
    {
        "id": "general-2",
        "category": "general",
        "title": "e-SIM en vez de roaming",
        "description": "Un e-SIM de Ubigi o Airalo para Japón cuesta ~2000¥ por 10GB. El roaming puede costar 30€/día.",
        "savings": "20,000+¥ en un viaje de 10 días",
        "icon": "📱"
    },
    {
        "id": "general-3",
        "category": "general",
        "title": "Free WiFi en estaciones",
        "description": "Las principales estaciones tienen WiFi gratuito. También en convenience stores y algunos cafes. Úsalo para ahorrar datos.",
        "savings": "Ahorras datos del e-SIM",
        "icon": "📶"
    },
    {
        "id": "actividades-1",
        "category": "actividades",
        "title": "Templos gratis",
        "description": "Muchos templos y santuarios son gratuitos. Meiji Shrine, Sensoji (exterior), Fushimi Inari... No necesitas pagar para disfrutar.",
        "savings": "500-2000¥ por templo",
        "icon": "⛩️"
    },
    {
        "id": "actividades-2",
        "category": "actividades",
        "title": "Parques y jardines",
        "description": "Shinjuku Gyoen (500¥), Ueno Park (gratis), Yoyogi Park (gratis), Kenrokuen. Los parques son la mejor actividad barata.",
        "savings": "0-500¥ por día",
        "icon": "🌸"
    },
    {
        "id": "actividades-3",
        "category": "actividades",
        "title": "Observa gratis desde Tokyo Skytree",
        "description": "En vez de subir a Tokyo Skytree (3000¥+), ve a la base gratis o visita el Tokyo Metropolitan Government Building (gratis, vista panorámica).",
        "savings": "3000¥+",
        "icon": "🏙️"
    },
]


@router.get("/savings")
async def get_saving_tips(category: str = None):
    """Tips de ahorro para viajar a Japón"""
    if category:
        tips = [t for t in SAVING_TIPS if t["category"] == category.lower()]
        return {"category": category, "tips": tips, "total_savings": f"Ahorra hasta {sum(int(t['savings'].replace(',','').split('-')[0].replace('¥','').replace('+','').replace('%','') or '0') for t in tips)}¥"}
    categories = list(set(t["category"] for t in SAVING_TIPS))
    return {"tips": SAVING_TIPS, "categories": categories, "total": len(SAVING_TIPS)}


@router.get("/categories")
async def get_tip_categories():
    """Categorías de tips disponibles"""
    categories = list(set(t["category"] for t in SAVING_TIPS))
    return {"categories": categories}
