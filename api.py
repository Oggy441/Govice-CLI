import httpx
from typing import Dict, Any, Optional, List
import config

# Weather code translation dictionary
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

async def geocode_city(city: str) -> Optional[Dict[str, Any]]:
    """Geocodes a city name to latitude, longitude, and country using Open-Meteo."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.replace(' ', '+')}&count=1&language=en&format=json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results")
                if results:
                    return {
                        "name": results[0].get("name"),
                        "country": results[0].get("country"),
                        "latitude": results[0].get("latitude"),
                        "longitude": results[0].get("longitude"),
                        "timezone": results[0].get("timezone"),
                        "country_code": results[0].get("country_code")
                    }
    except Exception:
        pass
    return None

async def get_weather(city: str) -> Optional[Dict[str, Any]]:
    """Fetches live weather and 3-day forecast for a city."""
    geo = await geocode_city(city)
    if not geo:
        return None
        
    lat = geo["latitude"]
    lon = geo["longitude"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&timezone=auto"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_weather", {})
                daily = data.get("daily", {})
                
                weather_desc = WEATHER_CODES.get(current.get("weathercode"), "Unknown")
                
                forecast = []
                if daily:
                    times = daily.get("time", [])
                    max_temps = daily.get("temperature_2m_max", [])
                    min_temps = daily.get("temperature_2m_min", [])
                    precip = daily.get("precipitation_probability_max", [])
                    wcodes = daily.get("weathercode", [])
                    
                    for i in range(min(3, len(times))):
                        forecast.append({
                            "date": times[i],
                            "max_temp": max_temps[i],
                            "min_temp": min_temps[i],
                            "precipitation_prob": precip[i] if i < len(precip) else 0,
                            "condition": WEATHER_CODES.get(wcodes[i], "Unknown") if i < len(wcodes) else "Unknown"
                        })
                        
                return {
                    "city": geo["name"],
                    "country": geo["country"],
                    "latitude": lat,
                    "longitude": lon,
                    "current": {
                        "temp": current.get("temperature"),
                        "windspeed": current.get("windspeed"),
                        "condition": weather_desc
                    },
                    "forecast": forecast
                }
    except Exception:
        pass
    return None

async def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """Gets exchange rate from from_currency to to_currency using free ExchangeRate API."""
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                return rates.get(to_currency.upper())
    except Exception:
        pass
    return None

async def get_places_pois(city: str) -> List[Dict[str, Any]]:
    """Gets local places/POIs. Falls back to empty list if no keys are configured."""
    geo = await geocode_city(city)
    if not geo:
        return []
        
    lat = geo["latitude"]
    lon = geo["longitude"]
    
    # Try Geoapify
    if config.GEOAPIFY_API_KEY:
        url = f"https://api.geoapify.com/v2/places?categories=tourism.attraction,leisure.park,entertainment&filter=circle:{lon},{lat},5000&limit=10&apiKey={config.GEOAPIFY_API_KEY}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", [])
                    results = []
                    for f in features:
                        props = f.get("properties", {})
                        name = props.get("name") or props.get("formatted")
                        if name:
                            results.append({
                                "name": name,
                                "category": props.get("categories", ["attraction"])[0].split(".")[-1].replace("_", " ").title(),
                                "address": props.get("formatted") or "",
                                "description": props.get("description") or "Local attraction"
                            })
                    return results
        except Exception:
            pass
            
    # Try OpenTripMap
    elif config.OPENTRIPMAP_API_KEY:
        url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={lon}&lat={lat}&kinds=interesting_places&limit=10&apikey={config.OPENTRIPMAP_API_KEY}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    features = response.json().get("features", [])
                    results = []
                    for f in features:
                        props = f.get("properties", {})
                        name = props.get("name")
                        if name:
                            results.append({
                                "name": name,
                                "category": props.get("kinds", "attraction").split(",")[0].replace("_", " ").title(),
                                "address": "",
                                "description": f"POI ID: {props.get('xid')}"
                            })
                    return results[:10]
        except Exception:
            pass
            
    return []
