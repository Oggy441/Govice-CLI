import asyncio
from typing import List
from session import TripContext
from agent import TravelAgent, ask_agent_interactive
from ui.theme import console
import api
from rich.table import Table

async def handle_hotels(args: List[str], context: TripContext, agent: TravelAgent):
    if not args:
        if context.destination:
            city = context.destination
        else:
            console.print("[travel.error]Usage: /hotels <city>[/]")
            return
    else:
        city = " ".join(args)
        
    console.print(f"[travel.teal]Searching for points of interest and hotel recommendations in [travel.gold]{city.title()}[/]...[/]")
    
    with console.status("[travel.teal]Fetching local attractions...[/]"):
        places = await api.get_places_pois(city)
        
    if places:
        table = Table(title=f"[travel.teal]Local Attractions in {city.title()}[/]", border_style="travel.sand")
        table.add_column("Name", style="travel.gold")
        table.add_column("Category", style="travel.teal")
        table.add_column("Description", style="travel.text")
        
        for p in places:
            table.add_row(p["name"], p["category"], p["description"])
        console.print(table)
        console.print()
        
    prompt = f"Recommend accommodation areas and hotels (budget, mid-range, luxury) in {city}. Provide approximate cost ranges."
    ask_agent_interactive(agent, prompt, context)
