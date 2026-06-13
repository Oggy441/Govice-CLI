from typing import List
from session import TripContext
from agent import TravelAgent, ask_agent_interactive
from ui.theme import console

async def handle_budget(args: List[str], context: TripContext, agent: TravelAgent):
    if len(args) < 2:
        if context.destination and context.days:
            destination = context.destination
            days = context.days
        else:
            console.print("[travel.error]Usage: /budget <destination> <days>[/]")
            return
    else:
        destination = args[0]
        try:
            days = int(args[1])
        except ValueError:
            console.print("[travel.error]Duration (days) must be an integer.[/]")
            return
            
    # Update context
    context.destination = destination
    context.days = days
    
    prompt = f"Provide a detailed travel budget estimate for visiting {destination} for {days} days. Break down expenses into categories: Accommodation, Food, Transport, Activities, and Miscellaneous. Provide estimated costs in {context.currency}."
    console.print(f"[travel.teal]Estimating budget breakdown for [travel.gold]{destination.title()}[/] ({days} Days)...[/]")
    
    ask_agent_interactive(agent, prompt, context)
