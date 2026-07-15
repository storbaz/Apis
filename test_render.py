import httpx
import json
import sys
import asyncio

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    base = 'https://apis-4g3r.onrender.com'
    async with httpx.AsyncClient(timeout=90.0) as c:
        print('=== SEARCH (dentistas Madrid) ===')
        r = await c.get(base + '/v1/maps/search', params={'query': 'dentistas', 'location': 'Madrid', 'limit': 3})
        print('Status:', r.status_code)
        data = r.json()
        if 'results' in data:
            results = data['results']
            print('Results:', len(results))
            for b in results:
                name = b.get('name', 'N/A')
                cat = b.get('category', 'N/A')
                rating = b.get('rating', 'N/A')
                print('  -', name, '|', cat, '|', rating, 'stars')
        else:
            print(json.dumps(data, indent=2))

asyncio.run(test())
