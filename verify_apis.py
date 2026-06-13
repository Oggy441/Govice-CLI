import sys
import asyncio
import api
from ui.theme import console

# Force stdout/stderr to use UTF-8 encoding, preventing charmap errors on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

async def test_apis():
    console.print("[travel.teal]=== Starting API Verification ===[/]")
    
    # 1. Test Weather API
    console.print("\n[travel.teal]1. Testing Weather API for London...[/]")
    try:
        weather = await api.get_weather("London")
        if weather:
            console.print(f"[travel.success]✓ Success![/] Weather in {weather['city']}, {weather['country']}:")
            console.print(f"  Current Temp: {weather['current']['temp']}°C, Condition: {weather['current']['condition']}")
            console.print(f"  Forecast days fetched: {len(weather['forecast'])}")
        else:
            console.print("[travel.error]✗ Failed:[/] Weather data returned None.")
    except Exception as e:
        console.print(f"[travel.error]✗ Error:[/] {e}")
        
    # 2. Test Exchange Rate API
    console.print("\n[travel.teal]2. Testing Exchange Rate API (USD to INR)...[/]")
    try:
        rate = await api.get_exchange_rate("USD", "INR")
        if rate:
            console.print(f"[travel.success]✓ Success![/] 1 USD = {rate} INR")
        else:
            console.print("[travel.error]✗ Failed:[/] Rate returned None.")
    except Exception as e:
        console.print(f"[travel.error]✗ Error:[/] {e}")
        
    # 3. Test Places/POIs API
    console.print("\n[travel.teal]3. Testing Places API for Tokyo (fallback mode check)...[/]")
    try:
        places = await api.get_places_pois("Tokyo")
        console.print(f"[travel.success]✓ Success![/] Fetched {len(places)} places.")
    except Exception as e:
        console.print(f"[travel.error]✗ Error:[/] {e}")

if __name__ == "__main__":
    asyncio.run(test_apis())
