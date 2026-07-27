#!/usr/bin/env python3
"""
Script para publicar artículos del blog de ViajApp en Dev.to
"""

import os
import sys
import json
import requests

DEVTO_API_KEY = os.environ.get("DEVTO_API_KEY", "")
API_URL = "https://dev.to/api/articles"

# Pool de artículos adaptados para Dev.to (enfocados en tech + viajes)
DEVTO_ARTICLES = [
    {
        "title": "How I Built a Japan Travel App with Next.js and FastAPI",
        "published": True,
        "tags": ["webdev", "javascript", "react", "buildinpublic"],
        "body_markdown": """
# How I Built a Japan Travel App with Next.js and FastAPI

Last year I decided to plan a trip to Japan. I quickly realized that information about Japan travel is scattered across dozens of websites, each with different formats and outdated prices.

So I built **ViajApp** - a complete Japan travel platform with API, web app, and soon mobile.

## The Stack

- **Frontend**: Next.js 16 with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Vercel + Render

## Features I Built

### 1. Restaurant Search with Serper API
Real-time search for restaurants, temples, and attractions using Google Places data.

### 2. Currency Converter
Live exchange rates updated daily. No more mental math at konbini.

### 3. Transport Calculator
Calculate the best route between cities with JR Pass recommendations.

### 4. Blog Auto-Generation
This article you're reading was automatically generated and posted via GitHub Actions. Every week, a new article about Japan travel is created and published to both the website and Dev.to.

### 5. Emergency Info
Real-time weather, emergency numbers, and hospital finder for each region.

## The API

The backend has 40+ endpoints covering:
- Culture guides
- Food recommendations  
- Budget calculator
- Event finder
- Transport info
- Emergency services

## Lessons Learned

1. **Start with the data**: Before writing code, I collected all the Japan travel information I could find
2. **API-first design**: Building the API first made the frontend much easier
3. **Automation is key**: The blog auto-generation saves hours every week
4. **SEO matters**: Each article has metadata, tags, and structured content

## What's Next

- Mobile app (React Native)
- AI-powered itinerary generator
- More countries (Greece, Italy, Spain)

## Try It

🌐 **Web**: [viajapp.app](https://www.viajapp.app)
📡 **API**: [japan-travel-api.onrender.com](https://japan-travel-api.onrender.com)

---

*Built with love for Japan 🇯🇵*
""",
        "canonical_url": "https://www.viajapp.app"
    },
    {
        "title": "10 Things I Learned Building a Travel App (That Nobody Tells You)",
        "published": True,
        "tags": ["productivity", "webdev", "career", "buildinpublic"],
        "body_markdown": """
# 10 Things I Learned Building a Travel App

I spent 6 months building ViajApp, a Japan travel platform. Here's what I wish I knew before starting.

## 1. Data is King, Not Code

The hardest part wasn't coding - it was collecting accurate data about Japan travel. Prices change, restaurants close, trains get rerouted.

**Solution**: I built a data pipeline that updates automatically.

## 2. Users Don't Care About Your Stack

Nobody asks if you use React or Vue. They care if the app works and looks good.

## 3. API Design is Everything

A well-designed API saves you months of refactoring later.

```
GET /v1/food/restaurants?city=tokyo&cuisine=ramen
GET /v1/transport/route?from=tokyo&to=kyoto
GET /v1/currency/convert?from=JPY&to=EUR&amount=1000
```

## 4. Automation Pays for Itself

I automated:
- Blog post generation (1 article/week)
- Currency rate updates (daily)
- Weather data sync (hourly)
- Event calendar updates (weekly)

**Time saved**: ~10 hours/week

## 5. SEO is Not Optional

Each page has:
- Meta titles and descriptions
- Open Graph tags
- Structured data
- XML sitemap
- Robots.txt

## 6. Mobile-First, Always

60% of travel app users are on mobile. If your app doesn't work on phones, you've lost them.

## 7. Error Handling Saves Lives

When someone is in Japan and your app crashes, they're lost. I added:
- Offline mode
- Fallback data
- Error boundaries
- Graceful degradation

## 8. Testing is Cheaper Than Bugs

33 tests covering API endpoints, currency calculations, and data validation.

## 9. Documentation is a Feature

The API has OpenAPI docs at `/docs`. Users love it.

## 10. Ship Fast, Iterate Faster

Version 1 was ugly but functional. Version 2 is beautiful. Users don't wait for perfect.

---

**Built ViajApp**: [viajapp.app](https://www.viajapp.app)
""",
        "canonical_url": "https://www.viajapp.app"
    },
    {
        "title": "Building a Real-Time Currency Converter for Travel Apps",
        "published": True,
        "tags": ["javascript", "webdev", "tutorial"],
        "body_markdown": """
# Building a Real-Time Currency Converter for Travel Apps

Every traveler needs to convert currencies. Here's how I built a real-time converter for ViajApp.

## The Problem

When you're in Japan, you need to quickly convert yen to your home currency. mental math is hard, and most apps require internet.

## The Solution

A currency converter that:
1. Updates rates daily
2. Works offline
3. Shows historical trends
4. Has a clean UI

## Implementation

### Backend (FastAPI)

```python
@router.get("/convert")
async def convert_currency(
    from_currency: str,
    to_currency: str, 
    amount: float
):
    rate = get_exchange_rate(from_currency, to_currency)
    converted = amount * rate
    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": rate,
        "converted": round(converted, 2)
    }
```

### Frontend (Next.js)

```typescript
const convertCurrency = async (amount: number) => {
  const res = await fetch(
    `/api/v1/currency/convert?from=${from}&to=${to}&amount=${amount}`
  );
  const data = await res.json();
  setConverted(data.converted);
};
```

## Features

- **10 currencies**: JPY, EUR, USD, GBP, KRW, etc.
- **Daily updates**: Rates refresh every 24 hours
- **Offline support**: Last known rates cached
- **Quick presets**: "How much is 1000 yen?"

## Lessons

1. **Cache everything**: API calls are slow, cache is fast
2. **Show the rate**: Users want to see the exchange rate, not just the result
3. **Round properly**: Money should always show 2 decimal places

---

**Try it**: [viajapp.app/currency](https://www.viajapp.app/currency)
""",
        "canonical_url": "https://www.viajapp.app/currency"
    },
    {
        "title": "ViajApp: How I Built Interactive Maps and Shared Expenses for a Travel App",
        "published": True,
        "tags": ["webdev", "javascript", "react", "buildinpublic"],
        "body_markdown": """
# ViajApp: Interactive Maps and Shared Expenses

I just shipped three major features for ViajApp, my Japan travel platform. Here's what I built and the technical challenges.

## 1. Interactive Route Map

The trip planner now includes a **Leaflet/OpenStreetMap** component that visualizes your Japan route.

### How it works:
- Cities are stored with coordinates in a `cityCoords` dictionary
- A `FitBounds` component auto-zooms to show all markers
- `L.divIcon` creates custom numbered markers (red for stops, green for final)
- A dashed polyline connects all cities
- Mobile-optimized: `scrollWheelZoom={false}` prevents accidental zoom

### The tricky part:
The `react-leaflet` library requires client-side rendering only. I used Next.js `dynamic()` with `{ ssr: false }` to prevent SSR errors:

```tsx
const RouteMap = dynamic(() => import("./RouteMap"), { ssr: false });
```

## 2. Shared Expenses

Built a complete expense splitting system:
- **Groups**: Create a group, add members
- **Expenses**: Add expenses with amount, currency, description
- **Balances**: Auto-calculate who owes whom
- **Supabase RLS**: Row-level security policies for data isolation

### Backend (FastAPI):
```python
@router.post("/groups")
async def create_group(data: CreateGroup, user = Depends(get_current_user)):
    group = supabase.table("expense_groups").insert({...}).execute()
    return group.data[0]
```

## 3. Community Tips

A Reddit-like system where travelers share tips:
- Categories: budget, transport, food, safety, accommodation
- Like system for voting
- Filter by city or category
- Moderation via `approved` flag

## Results

- 63 pages live
- 35+ API endpoints
- All features working in production

**Try it**: [viajapp.app](https://www.viajapp.app)
""",
        "canonical_url": "https://www.viajapp.app"
    },
    {
        "title": "How to Automate Blog Posts with GitHub Actions and AI",
        "published": True,
        "tags": ["devops", "productivity", "javascript"],
        "body_markdown": """
# How to Automate Blog Posts with GitHub Actions

I auto-generate one blog post per week about Japan travel. Here's the exact setup.

## The System

```
GitHub Actions → API → Generate Article → Post to Dev.to
```

## Step 1: Article Pool

I have 19 pre-written articles about Japan in a JSON pool:

```json
{
  "slug": "curiosidades-japon",
  "title": "15 Curiosidades de Japón",
  "category": "Curiosidades",
  "content": "..."
}
```

## Step 2: GitHub Action

```yaml
name: Auto Blog Post
on:
  schedule:
    - cron: '0 10 * * 1'  # Every Monday at 10am UTC
  workflow_dispatch:

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - name: Generate and Post
        run: |
          # Get next article from pool
          ARTICLE=$(curl -s -X POST $API_URL/v1/blog/generate)
          
          # Extract content
          TITLE=$(echo $ARTICLE | jq -r '.post.title')
          CONTENT=$(echo $ARTICLE | jq -r '.post.content')
          TAGS=$(echo $ARTICLE | jq -r '.post.tags | join(",")')
          
          # Post to Dev.to
          curl -X POST https://dev.to/api/articles \\
            -H "api-key: ${{ secrets.DEVTO_API_KEY }}" \\
            -H "Content-Type: application/json" \\
            -d "{
              \"article\": {
                \"title\": \"$TITLE\",
                \"body_markdown\": \"$CONTENT\",
                \"tags\": [\"webdev\", \"javascript\"],
                \"published\": true
              }
            }"
```

## Step 3: Secrets

Add your Dev.to API key as a GitHub secret:
- Go to repo Settings → Secrets → Actions
- Add `DEVTO_API_KEY`

## Results

- **1 article/week** automatically
- **0 manual work** after setup
- **Cross-posted** to website + Dev.to
- **SEO optimized** with metadata

## Cost

- GitHub Actions: **Free** (2000 minutes/month)
- Dev.to API: **Free**
- Total: **$0/month**

---

**Source code**: [github.com/storbaz/japan-travel-api](https://github.com/storbaz/japan-travel-api)
""",
        "canonical_url": "https://www.viajapp.app"
    }
]

def post_to_devto(article):
    """Publica un artículo en Dev.to"""
    headers = {
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {"article": article}
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"Articulo publicado: {data.get('url', 'Sin URL')}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

def main():
    if not DEVTO_API_KEY:
        print("DEVTO_API_KEY no esta configurada")
        sys.exit(1)
    
    print("Publicando en Dev.to...")
    
    # Rotate through articles using a state file
    state_file = os.path.join(os.path.dirname(__file__), ".last_posted_index")
    last_index = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                last_index = int(f.read().strip())
        except (ValueError, IOError):
            last_index = 0
    
    if DEVTO_ARTICLES:
        article_index = last_index % len(DEVTO_ARTICLES)
        article = DEVTO_ARTICLES[article_index]
        print(f"Articulo #{article_index + 1}/{len(DEVTO_ARTICLES)}")
        print(f"Titulo: {article['title']}")
        print(f"Tags: {', '.join(article['tags'])}")
        
        success = post_to_devto(article)
        
        if success:
            # Save next index
            with open(state_file, "w") as f:
                f.write(str((article_index + 1) % len(DEVTO_ARTICLES)))
            print("\nArticulo publicado exitosamente!")
        else:
            print("\nError al publicar")
            sys.exit(1)
    else:
        print("No hay articulos en el pool")
        sys.exit(1)

if __name__ == "__main__":
    main()
