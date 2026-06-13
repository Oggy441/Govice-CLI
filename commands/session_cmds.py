from typing import List
import shlex
from session import TripContext
from agent import TravelAgent
from ui.theme import console
from ui.components import print_status_bar

async def handle_save(args: List[str], context: TripContext, agent: TravelAgent):
    if not args:
        console.print("[travel.error]Usage: /save <session_name>[/]")
        return
        
    name = args[0]
    try:
        path = context.save(name)
        console.print(f"[travel.success]Successfully saved trip session to {path}[/]")
    except Exception as e:
        console.print(f"[travel.error]Failed to save session: {e}[/]")

async def handle_load(args: List[str], context: TripContext, agent: TravelAgent):
    if not args:
        saved = TripContext.list_saved_sessions()
        if not saved:
            console.print("[travel.info]No saved sessions found.[/]")
        else:
            console.print("[travel.info]Saved sessions:[/]")
            for s in saved:
                console.print(f"  - {s}")
        console.print("[travel.error]Usage: /load <session_name>[/]")
        return
        
    name = args[0]
    loaded = TripContext.load(name)
    if not loaded:
        console.print(f"[travel.error]Session '{name}' not found.[/]")
        return
        
    context.destination = loaded.destination
    context.days = loaded.days
    context.budget = loaded.budget
    context.currency = loaded.currency
    context.saved_itinerary = loaded.saved_itinerary
    context.chat_history = loaded.chat_history
    
    if agent.is_initialized:
        agent.load_history(context.chat_history)
            
    console.print(f"[travel.success]Successfully loaded session '{name}'![/]")
    print_status_bar(context)


async def handle_clear(args: List[str], context: TripContext, agent: TravelAgent):
    context.destination = None
    context.days = None
    context.budget = None
    context.currency = "INR"
    context.saved_itinerary = None
    context.chat_history = []
    
    if agent.is_initialized:
        agent.load_history([])
        
    console.print("[travel.success]Session context and chat history cleared.[/]")
    print_status_bar(context)
