import asyncio
from typing import List
from session import TripContext
from agent import TravelAgent
from ui.theme import console
import api
from rich.table import Table
from rich.panel import Panel

async def handle_weather(args: List[str], context: TripContext, agent: TravelAgent):
    if not args:
        if context.destination:
            city = context.destination
        else:
            console.print("[travel.error]Usage: /weather <city>[/]")
            return
    else:
        city = " ".join(args)

    with console.status(f"[travel.teal]Fetching weather for {city.title()}...[/]"):
        weather_data = await api.get_weather(city)

    if not weather_data:
        if agent.is_initialized and agent.client:
            with console.status("[travel.teal]Checking for spelling correction...[/]"):
                try:
                    prompt = (
                        f"The user searched for the weather of '{city}'. We couldn't find a direct geocoding result. "
                        "If this is a typo of a valid city, return only the corrected city name. "
                        "If this is a region, state, or country, return the name of its capital or most popular major city (e.g., return 'Jaipur' for 'Rajasthan', or 'Paris' for 'France'). "
                        "If it is completely unrecognized, return 'None'. Do not write any other text, just the corrected city name or 'None'."
                    )
                    response = agent.client.models.generate_content(
                        model=agent.model_name,
                        contents=prompt
                    )
                    corrected_city = response.text.strip().replace("'", "").replace('"', "")
                    if corrected_city and corrected_city.lower() != "none" and corrected_city.lower() != city.lower():
                        console.print(f"[travel.info]Location not found. Retrying with corrected spelling: [travel.gold]{corrected_city}[/]...[/]")
                        with console.status(f"[travel.teal]Fetching weather for {corrected_city}...[/]"):
                            weather_data = await api.get_weather(corrected_city)
                except Exception:
                    pass

    if not weather_data:
        console.print(f"[travel.error]Could not fetch weather data for {city.title()}.[/]")
        return

    current = weather_data["current"]
    console.print(Panel(
        f"[travel.teal]City:[/] [travel.gold]{weather_data['city']}, {weather_data['country']}[/]\n"
        f"[travel.teal]Current Temp:[/] {current['temp']}°C\n"
        f"[travel.teal]Condition:[/] {current['condition']}\n"
        f"[travel.teal]Wind Speed:[/] {current['windspeed']} km/h",
        title="[travel.teal]Current Weather[/]",
        border_style="travel.teal"
    ))

    table = Table(title="[travel.teal]3-Day Weather Forecast[/]", border_style="travel.sand")
    table.add_column("Date", style="travel.text")
    table.add_column("Max Temp", style="travel.gold")
    table.add_column("Min Temp", style="travel.info")
    table.add_column("Rain %", style="travel.teal")
    table.add_column("Condition", style="travel.text")

    for f in weather_data["forecast"]:
        table.add_row(
            f["date"],
            f"{f['max_temp']}°C",
            f"{f['min_temp']}°C",
            f"{f['precipitation_prob']}%",
            f["condition"]
        )

    console.print(table)
