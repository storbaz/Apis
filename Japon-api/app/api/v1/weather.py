from fastapi import APIRouter
import httpx
from app.config import settings

router = APIRouter(prefix="/weather", tags=["weather"])

CITIES = {
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "name": "Tokyo"},
    "osaka": {"lat": 34.6937, "lon": 135.5023, "name": "Osaka"},
    "kyoto": {"lat": 35.0116, "lon": 135.7681, "name": "Kyoto"},
    "hiroshima": {"lat": 34.3853, "lon": 132.4553, "name": "Hiroshima"},
    "sapporo": {"lat": 43.0621, "lon": 141.3544, "name": "Sapporo"},
    "fukuoka": {"lat": 33.5902, "lon": 130.4017, "name": "Fukuoka"},
    "nagoya": {"lat": 35.1815, "lon": 136.9066, "name": "Nagoya"},
    "okinawa": {"lat": 26.3344, "lon": 127.8056, "name": "Okinawa"},
    "nara": {"lat": 34.6851, "lon": 135.8048, "name": "Nara"},
}

WEATHER_ICONS = {
    "01d": "☀️", "01n": "🌙",
    "02d": "⛅", "02n": "☁️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️",
}


@router.get("/{city}")
async def get_weather(city: str):
    city_data = CITIES.get(city.lower())
    if not city_data:
        return {"error": f"Ciudad '{city}' no encontrada. Disponibles: {', '.join(CITIES.keys())}"}

    if not settings.OPENWEATHER_API_KEY:
        return _generate_mock_weather(city_data)

    try:
        async with httpx.AsyncClient() as client:
            current = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": city_data["lat"],
                    "lon": city_data["lon"],
                    "appid": settings.OPENWEATHER_API_KEY,
                    "units": "metric",
                    "lang": "es",
                },
                timeout=10.0,
            )

            if current.status_code != 200:
                return _generate_mock_weather(city_data)

            data = current.json()
            forecast_resp = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "lat": city_data["lat"],
                    "lon": city_data["lon"],
                    "appid": settings.OPENWEATHER_API_KEY,
                    "units": "metric",
                    "lang": "es",
                },
                timeout=10.0,
            )

            forecast = []
            if forecast_resp.status_code == 200:
                fdata = forecast_resp.json()
                seen = set()
                for item in fdata.get("list", []):
                    date = item["dt_txt"].split(" ")[0]
                    if date not in seen and len(forecast) < 7:
                        seen.add(date)
                        forecast.append({
                            "date": date,
                            "temp_min": item["main"]["temp_min"],
                            "temp_max": item["main"]["temp_max"],
                            "description": item["weather"][0]["description"],
                            "icon": WEATHER_ICONS.get(item["weather"][0]["icon"], "☀️"),
                        })

            return {
                "city": city_data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": WEATHER_ICONS.get(data["weather"][0]["icon"], "☀️"),
                "wind": data["wind"]["speed"],
                "forecast": forecast,
            }

    except Exception:
        return _generate_mock_weather(city_data)


def _generate_mock_weather(city_data: dict):
    import random
    from datetime import datetime, timedelta

    base_temp = {"tokyo": 22, "osaka": 23, "kyoto": 21, "hiroshima": 22, "sapporo": 15, "fukuoka": 23, "nagoya": 22, "okinawa": 27, "nara": 21}
    temp = base_temp.get(city_data["name"].lower(), 22) + random.uniform(-3, 3)
    icons = ["☀️", "⛅", "☁️", "🌦️"]
    descs = ["cielo despejado", "parcialmente nublado", "nublado", "lluvia ligera"]

    forecast = []
    for i in range(7):
        d = datetime.now() + timedelta(days=i + 1)
        t_min = temp + random.uniform(-5, -1)
        t_max = temp + random.uniform(1, 5)
        forecast.append({
            "date": d.strftime("%Y-%m-%d"),
            "temp_min": round(t_min, 1),
            "temp_max": round(t_max, 1),
            "description": random.choice(descs),
            "icon": random.choice(icons),
        })

    return {
        "city": city_data["name"],
        "temp": round(temp, 1),
        "feels_like": round(temp - 1, 1),
        "humidity": random.randint(40, 80),
        "description": random.choice(descs),
        "icon": random.choice(icons),
        "wind": round(random.uniform(1, 8), 1),
        "forecast": forecast,
        "mock": True,
    }
