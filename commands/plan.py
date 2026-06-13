from typing import List
from session import TripContext
from agent import TravelAgent, ask_agent_interactive
from ui.theme import console
from ui.components import print_status_bar

async def handle_plan(args: List[str], context: TripContext, agent: TravelAgent):
    if len(args) < 2:
        console.print("[travel.error]Usage: /plan <destination> <days>[/]")
        return

    destination = args[0]
    try:
        days = int(args[1])
    except ValueError:
        console.print("[travel.error]Duration (days) must be an integer.[/]")
        return

    # Update context
    context.destination = destination
    context.days = days
    
    prompt = f"Create a detailed day-by-day travel itinerary for {destination} for {days} days. Include recommended daily activities, dining choices, and transit tips."
    
    console.print(f"[travel.teal]Planning trip to [travel.gold]{destination.title()}[/] for {days} days...[/]")
    print_status_bar(context)
    
    ask_agent_interactive(agent, prompt, context)
