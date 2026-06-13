from typing import List
from session import TripContext
from agent import TravelAgent, ask_agent_interactive
from ui.theme import console

async def handle_flights(args: List[str], context: TripContext, agent: TravelAgent):
    if len(args) < 3:
        console.print("[travel.error]Usage: /flights <from> <to> <date>[/]")
        return
        
    origin = args[0]
    destination = args[1]
    date = args[2]
    
    prompt = f"Estimate flight routes, airlines, flight times, and cost ranges from {origin} to {destination} around {date}."
    console.print(f"[travel.teal]Searching flight estimates from [travel.gold]{origin.upper()}[/] to [travel.gold]{destination.upper()}[/] on {date}...[/]")
    
    ask_agent_interactive(agent, prompt, context)
