# API Specifications

Operational contract and schema rules for all internal API functions used by the Travel CLI application.

## Overview

This document describes the internal API functions defined in `api.py` that interact with external services to provide geocoding, weather, currency exchange, and points of interest data. All functions are asynchronous and designed for CLI interactive use.

## External Services

| Service | Purpose | Configuration Required |
|---------|---------|------------------------|
| Open-Meteo Geocoding API | City name to coordinates | None |
| Open-Meteo Weather API | Current weather and forecast | None |
| ExchangeRate API (open.er-api.com) | Currency conversion rates | None |
| Geoapify Places API | Points of interest (tourism, leisure) | `GEOAPIFY_API_KEY` |
| OpenTripMap API | Alternative POI source | `OPENTRIPMAP_API_KEY` |

## Functions

### `geocode_city(city: str) -> Optional[Dict[str, Any]]`

Geocodes a city name to latitude, longitude, and metadata using Open-Meteo Geocoding API.

**Parameters**
- `city` (str): City name to search for (spaces are URL-encoded)

**Returns**
- `Dict` with keys: `name`, `country`, `latitude`, `longitude`, `timezone`, `country_code`
- `None` if request fails or no results found

**Example Response**
```json
{
  "name": "Paris",
  "country": "France",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "timezone": "Europe/Paris",
  "country_code": "FR"
}
```

**Errors**
- Network timeout (10s)
- HTTP non-200 status
- Empty results array

---

### `get_weather(city: str) -> Optional[Dict[str, Any]]`

Fetches current weather and 3-day forecast for a city using Open-Meteo Weather API.

**Parameters**
- `city` (str): City name (internally geocoded via `geocode_city`)

**Returns**
- `Dict` with structure:
  - `city` (str): Resolved city name
  - `country` (str): Country name
  - `latitude` (float)
  - `longitude` (float)
  - `current` (Dict): `temp` (°C), `windspeed` (km/h), `condition` (str)
  - `forecast` (List[Dict]): Up to 3 days with `date`, `max_temp`, `min_temp`, `precipitation_prob`, `condition`
- `None` if geocoding fails or weather request fails

**Weather Codes**
Uses internal `WEATHER_CODES` mapping (WMO codes) to human-readable conditions.

**Errors**
- Propagates geocoding errors
- Network timeout (10s)
- HTTP non-200 status

---

### `get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]`

Gets exchange rate from `from_currency` to `to_currency` using free ExchangeRate API.

**Parameters**
- `from_currency` (str): Base currency code (e.g., "USD")
- `to_currency` (str): Target currency code (e.g., "EUR")

**Returns**
- `float` exchange rate (1 unit of `from_currency` = X units of `to_currency`)
- `None` if request fails or currency not found

**Endpoint**
`https://open.er-api.com/v6/latest/{from_currency}`

**Errors**
- Network timeout (10s)
- HTTP non-200 status
- Missing rate in response

---

### `get_places_pois(city: str) -> List[Dict[str, Any]]`

Gets local points of interest (attractions, parks, entertainment) for a city.

**Parameters**
- `city` (str): City name (internally geocoded)

**Returns**
- `List[Dict]` with each item containing:
  - `name` (str)
  - `category` (str): Human-readable category (e.g., "Attraction", "Park")
  - `address` (str): Formatted address or empty string
  - `description` (str): Brief description or placeholder
- Empty list if no API keys configured or all requests fail

**Provider Priority**
1. Geoapify Places API (requires `GEOAPIFY_API_KEY`)
2. OpenTripMap API (requires `OPENTRIPMAP_API_KEY`)
3. Returns empty list if neither key is set

**Geoapify Parameters**
- Categories: `tourism.attraction`, `leisure.park`, `entertainment`
- Radius: 5000m circle around city center
- Limit: 10 results

**OpenTripMap Parameters**
- Kinds: `interesting_places`
- Radius: 5000m
- Limit: 10 results

**Errors**
- Silently catches exceptions per provider
- Falls back to next provider
- Returns empty list on total failure

## Configuration

API keys are loaded from environment variables via `config.py`:

```python
# In config.py
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")
```

Set these in your `.env` file or environment to enable POI lookup.

## Error Handling

All functions:
- Use 10-second timeout via `httpx.AsyncClient`
- Catch all exceptions and return `None` or empty list
- Do not raise exceptions to caller
- Log no errors (silent failure)

## Usage Notes

- All functions are `async` and must be awaited
- Designed for CLI interactive use, not high-throughput
- No rate limiting implemented (respect provider limits)
- Weather data uses metric units (°C, km/h)
- Currency rates are real-time from ExchangeRate API
- Geocoding uses Open-Meteo's free tier (no API key required)