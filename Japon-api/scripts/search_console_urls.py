#!/usr/bin/env python3
"""
Genera la lista de URLs para enviar a Google Search Console.
Ejecutar: python scripts/search_console_urls.py
Copia las URLs y envialas manualmente desde:
https://search.google.com/search-console
"""

BASE = "https://www.viajapp.app"

# URLs que necesitan indexacion (prioridad alta)
PRIORITY_URLS = [
    # Paginas de ciudades (SEO alto)
    f"{BASE}/tokyo",
    f"{BASE}/kyoto",
    f"{BASE}/osaka",
    f"{BASE}/hiroshima",
    f"{BASE}/nara",
    f"{BASE}/fukuoka",
    f"{BASE}/hakone",
    f"{BASE}/kanazawa",
    # Herramientas
    f"{BASE}/tools",
    f"{BASE}/jr-pass",
    f"{BASE}/trip-planner",
    f"{BASE}/translator",
    f"{BASE}/favorites",
    f"{BASE}/wallet",
    f"{BASE}/today",
    f"{BASE}/free-tours",
    f"{BASE}/authentic",
    # Lugares estructurados
    f"{BASE}/place/senso-ji-temple",
    f"{BASE}/place/fushimi-inari-taisha",
    f"{BASE}/place/shibuya-crossing",
    f"{BASE}/place/arashiyama-bamboo",
    f"{BASE}/place/dotonbori",
    # Social
    f"{BASE}/shared-expenses",
    f"{BASE}/community",
    # Blog
    f"{BASE}/blog",
    f"{BASE}/blog/nuevas-herramientas-viajapp-2026",
    # Otros
    f"{BASE}/forgot-to-buy",
    f"{BASE}/about",
    f"{BASE}/contact",
    f"{BASE}/food",
    f"{BASE}/transport",
    f"{BASE}/weather",
    f"{BASE}/budget",
    f"{BASE}/events",
    f"{BASE}/culture",
    f"{BASE}/history",
    f"{BASE}/nature",
    f"{BASE}/sports",
    f"{BASE}/shopping",
    f"{BASE}/reservations",
    f"{BASE}/seasons",
    f"{BASE}/freaky",
    f"{BASE}/currency",
    f"{BASE}/map",
    f"{BASE}/restaurants",
    f"{BASE}/visa",
    f"{BASE}/packing",
]

print("=" * 60)
print("URLS PARA GOOGLE SEARCH CONSOLE")
print("=" * 60)
print(f"\nTotal: {len(PRIORITY_URLS)} URLs\n")
print("Enviar via: https://search.google.com/search-console")
print("Herramienta: Inspeccionar URL -> Solicitar indexacion\n")
print("-" * 60)

for i, url in enumerate(PRIORITY_URLS, 1):
    print(f"{i:2d}. {url}")

print("-" * 60)
print("\nNota: Google solo permite ~10-12 solicitudes/dia.")
print("Empieza con las paginas de ciudades (mas importantes para SEO).")
