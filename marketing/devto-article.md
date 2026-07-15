# How to Generate B2B Leads from Google Maps in 2 Minutes (Free API)

**Stop manually copying business data. Automate your lead generation with this free API.**

---

Generating B2B leads is tedious. You search Google Maps, copy the business name, find their website, check if the email exists... repeat 500 times.

What if you could do all of that with a single API call?

That's exactly what the **Google Maps Business Scraper API** does. Let me show you.

## What It Does

- **Search** any business type in any location (dentists in Madrid, restaurants in NYC, lawyers in London)
- **Get** business name, address, website, phone, rating, and coordinates
- **Enrich** with verified emails (SMTP verification) and social profiles (LinkedIn, Instagram, Facebook)
- **All** returned as clean JSON in milliseconds

## Quick Start

### Step 1: Get Your Free API Key

Go to [Google Maps Business Scraper on RapidAPI](https://rapidapi.com/storbaz/api/google-maps-business-scraper5) and sign up. The **free tier gives you 100 requests/month** with no credit card required.

### Step 2: Search for Businesses

**Python:**

```python
import requests

url = "https://google-maps-business-scraper5.p.rapidapi.com/v1/maps/search"

querystring = {
    "query": "dentistas",
    "location": "Madrid",
    "limit": "10"
}

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "google-maps-business-scraper5.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

for business in data["results"]:
    print(f"{business['name']} - {business['address']}")
```

**JavaScript:**

```javascript
const options = {
    method: 'GET',
    headers: {
        'X-RapidAPI-Key': 'YOUR_API_KEY',
        'X-RapidAPI-Host': 'google-maps-business-scraper5.p.rapidapi.com'
    }
};

const url = new URL('https://google-maps-business-scraper5.p.rapidapi.com/v1/maps/search');
url.searchParams.append('query', 'dentistas');
url.searchParams.append('location', 'Madrid');
url.searchParams.append('limit', '10');

fetch(url, options)
    .then(res => res.json())
    .then(data => {
        data.results.forEach(biz => {
            console.log(`${biz.name} - ${biz.address}`);
        });
    });
```

### Step 3: Enrich with Emails

Add `enrich=true` to get verified emails and social profiles:

```python
querystring = {
    "query": "dentistas",
    "location": "Madrid",
    "limit": "10",
    "enrich": "true"
}
```

The response now includes:

```json
{
    "name": "Clínica Dental Madrid",
    "address": "Calle Gran Vía 42, Madrid",
    "website": "https://clinicadental.com",
    "email": "info@clinicadental.com",
    "email_verified": true,
    "social": {
        "linkedin": "https://linkedin.com/company/clinicadental",
        "instagram": "https://instagram.com/clinicadental"
    }
}
```

## Use Cases

| Use Case | How It Helps |
|----------|--------------|
| **Lead Generation** | Build prospect lists for cold outreach |
| **Sales Prospecting** | Find potential clients by industry and location |
| **Market Research** | Analyze business density in different areas |
| **Email Campaigns** | Get verified emails for cold email sequences |
| **Freelancing** | Find local businesses that need your services |

## Real Example: Finding Dentists in Madrid

```python
import requests

# Search 50 dentists in Madrid
response = requests.get(
    "https://google-maps-business-scraper5.p.rapidapi.com/v1/maps/search",
    headers={
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "google-maps-business-scraper5.p.rapidapi.com"
    },
    params={
        "query": "dentistas",
        "location": "Madrid, Spain",
        "limit": "50",
        "enrich": "true"
    }
)

leads = response.json()["results"]
print(f"Found {len(leads)} leads")

for lead in leads:
    email = lead.get("email", "No email")
    print(f"{lead['name']} | {email} | ⭐ {lead.get('rating', 'N/A')}")
```

Output:
```
Found 50 leads
Clínica Dental Madrid | info@clinicadental.com | ⭐ 4.7
Dental Studio Madrid | hello@dentalstudio.es | ⭐ 4.5
...
```

## Pricing

| Plan | Requests/Month | Price |
|------|---------------|-------|
| **Free** | 100 | $0 |
| **Basic** | 5,000 | $9/mo |
| **Pro** | 20,000 | $29/mo |
| **Business** | 75,000 | $79/mo |

The free tier is enough to test and validate your use case.

## Try It Now

1. Go to [Google Maps Business Scraper API](https://rapidapi.com/storbaz/api/google-maps-business-scraper5)
2. Subscribe to the free plan
3. Run your first search

No credit card. No setup fees. Just search and get data.

---

*Have questions? Drop a comment below or reach out on [Twitter/X](https://x.com/storbaz).*
