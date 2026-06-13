from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from ui.theme import console
from session import TripContext

def print_banner():
    """Prints a beautiful sand-to-teal gradient ASCII banner."""
    banner_text = """
██████╗  ██████╗ ██╗    ██╗██╗ ██████╗███████╗
██╔════╝ ██╔═══██╗██║   ██║██║██╔════╝██╔════╝
██║  ███╗██║   ██║██║   ██║██║██║     █████╗  
██║   ██║██║   ██║╚██╗ ██╔╝██║██║     ██╔══╝  
╚██████╔╝╚██████╔╝ ╚████╔╝ ██║╚██████╗███████╗
 ╚═════╝  ╚═════╝   ╚═══╝  ╚═╝ ╚═════╝╚══════╝
                                                      
    ~ Your AI Terminal Travel Companion ~
    """
    
    text = Text(banner_text)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i < 7:
            if i < 4:
                line.stylize("travel.teal")
            else:
                line.stylize("travel.sand")
        else:
            line.stylize("travel.gold")
            
    styled_text = Text("\n").join(lines)
    
    panel = Panel(
        Align.center(styled_text),
        border_style="travel.teal",
        title="[travel.gold]v1.0.0[/]",
        subtitle="[travel.sand]Powered by Gemma 4[/]"
    )
    console.print(panel)

def print_status_bar(context: TripContext):
    """Renders a compact panel showing active travel state."""
    if not context.destination:
        status_text = Text.assemble(
            ("! ", "travel.gold"),
            ("No active trip context. Set one using ", "travel.info"),
            ("/plan <destination> <days>", "travel.command"),
            (" or start chatting!", "travel.info")
        )
    else:
        dest = context.destination.title()
        days = f"{context.days} Days" if context.days else "Flexible Duration"
        budget = f"{context.currency} {context.budget:,.2f}" if context.budget else "Flexible Budget"
        
        status_text = Text.assemble(
            ("📍 Destination: ", "travel.teal"), (dest, "travel.gold"),
            ("  |  ", "travel.info"),
            ("📅 Duration: ", "travel.teal"), (days, "travel.text"),
            ("  |  ", "travel.info"),
            ("💰 Budget: ", "travel.teal"), (budget, "travel.text")
        )
        
    console.print(Panel(status_text, border_style="travel.sand", title="[travel.teal]Active Trip Context[/]"))

def print_help():
    """Renders a structured table detailing all slash commands."""
    table = Table(title="[travel.teal]Available Travel CLI Commands[/]", border_style="travel.teal")
    table.add_column("Command", style="travel.command", width=35)
    table.add_column("Description", style="travel.text")
    table.add_column("Example", style="travel.info")
    
    table.add_row("/plan <destination> <days>", "Generate a day-by-day travel itinerary", "/plan Tokyo 5")
    table.add_row("/weather <city>", "Fetch live weather details and forecast", "/weather Paris")
    table.add_row("/flights <from> <to> <date>", "Estimate flight routes and cost ranges", "/flights NYC Tokyo 2026-09-01")
    table.add_row("/hotels <city>", "Get points of interest and hotel details", "/hotels Rome")
    table.add_row("/budget <destination> <days>", "Generate estimated expense breakdown", "/budget Iceland 7")
    table.add_row("/save <name>", "Save active session context to disk", "/save my_japan_trip")
    table.add_row("/load <name>", "Load a previously saved trip session", "/load my_japan_trip")
    table.add_row("/clear", "Reset active trip context and chat history", "/clear")
    table.add_row("/exit", "Exit the travel assistant", "/exit")
    
    console.print(table)
