import os
import sys
import asyncio
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.panel import Panel

# Force stdout/stderr to use UTF-8 encoding, preventing charmap errors on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import config
from session import TripContext
from agent import TravelAgent, ask_agent_interactive
from ui.theme import console
from ui.components import print_banner, print_status_bar, print_help

# Import command handlers
from commands.plan import handle_plan
from commands.weather import handle_weather
from commands.flights import handle_flights
from commands.hotels import handle_hotels
from commands.budget import handle_budget
from commands.session_cmds import handle_save, handle_load, handle_clear

# Map of commands to their async handler functions
COMMAND_MAP = {
    "/plan": handle_plan,
    "/weather": handle_weather,
    "/flights": handle_flights,
    "/hotels": handle_hotels,
    "/budget": handle_budget,
    "/save": handle_save,
    "/load": handle_load,
    "/clear": handle_clear,
}

# Style for the prompt
prompt_style = Style.from_dict({
    'prompt': '#006d77 bold',
    'arrow': '#e29578 bold',
})

async def check_or_prompt_api_key() -> bool:
    """Ensure Gemini API key is configured. If not, prompt the user for one."""
    if config.has_gemini_key():
        return True
        
    console.print(Panel(
        "[travel.error]Google Gemini API key was not found in your environment or .env file.[/]\n\n"
        "[travel.info]Please get a free API key from Google AI Studio:[/]\n"
        "https://aistudio.google.com/",
        title="[travel.error]API Key Required[/]",
        border_style="travel.error"
    ))
    
    try:
        # Prompt for key
        key = input("Enter your GEMINI_API_KEY: ").strip()
        if not key:
            console.print("[travel.error]No API key provided. Chat agent will not be functional.[/]")
            return False
            
        save = input("Would you like to save this key to a .env file? (y/n): ").strip().lower()
        save_to_env = save in ("y", "yes")
        
        config.set_gemini_key(key, save_to_env=save_to_env)
        if save_to_env:
            console.print("[travel.success]Saved API key to .env file.[/]")
        return True
    except (KeyboardInterrupt, EOFError):
        console.print("\n[travel.error]Cancelled API key prompt.[/]")
        return False

async def main():
    # Print welcome banner
    print_banner()
    
    # Check Gemini API Key
    await check_or_prompt_api_key()
    
    # Initialize travel agent
    agent = TravelAgent()
    if config.has_gemini_key():
        with console.status("[travel.teal]Initializing AI Travel Agent...[/]"):
            initialized = agent.initialize()
            if initialized:
                console.print("[travel.success]AI Travel Agent ready.[/]")
            else:
                console.print("[travel.error]Could not initialize AI Agent. Chat fallback will be active.[/]")
    
    # Initialize active context (restore from autosave if available)
    context = TripContext()
    loaded_session = TripContext.load("autosave")
    if loaded_session:
        context.destination = loaded_session.destination
        context.days = loaded_session.days
        context.budget = loaded_session.budget
        context.currency = loaded_session.currency
        context.saved_itinerary = loaded_session.saved_itinerary
        context.chat_history = loaded_session.chat_history
        
        if agent.is_initialized:
            agent.load_history(context.chat_history)
            
        console.print("[travel.success]Restored previous travel session memory.[/]")
        
    print_status_bar(context)
    console.print("[travel.info]Type [/][travel.command]/help[/][travel.info] for a list of commands, or start chatting![/]\n")
    
    # Set up prompt toolkit session
    completer = WordCompleter(list(COMMAND_MAP.keys()) + ["/help", "/exit"], ignore_case=True)
    
    use_fallback_prompt = False
    try:
        session = PromptSession(completer=completer)
    except Exception:
        use_fallback_prompt = True
    
    # REPL loop
    while True:
        try:
            # Styled prompt or fallback
            if use_fallback_prompt:
                loop = asyncio.get_event_loop()
                user_input = await loop.run_in_executor(None, lambda: input("travel-cli ❯ "))
            else:
                user_input = await session.prompt_async(
                    [('class:prompt', 'travel-cli'), ('class:arrow', ' ❯ ')],
                    style=prompt_style
                )
            user_input = user_input.strip()
            if not user_input:
                continue
                
            if user_input.lower() in ("/exit", "/quit"):
                console.print("\n[travel.sand]Safe travels! Goodbye.[/]")
                break
                
            if user_input.lower() == "/help":
                print_help()
                continue
                
            if user_input.startswith("/"):
                try:
                    parts = shlex.split(user_input)
                except ValueError:
                    parts = user_input.split()
                    
                cmd = parts[0].lower()
                args = parts[1:]
                
                if cmd in COMMAND_MAP:
                    try:
                        await COMMAND_MAP[cmd](args, context, agent)
                    except Exception as e:
                        console.print(f"[travel.error]Error executing command {cmd}: {e}[/]")
                else:
                    console.print(f"[travel.error]Unknown command: {cmd}. Type /help for available commands.[/]")
            else:
                # Chat message
                if not agent.is_initialized:
                    # Try to reinitialize in case they set the key later
                    if config.has_gemini_key():
                        agent.initialize()
                        
                if not agent.is_initialized:
                    console.print("[travel.error]Gemini client not initialized. Cannot chat. Set GEMINI_API_KEY first.[/]")
                else:
                    ask_agent_interactive(agent, user_input, context)
                    
            # Auto-save session memory after interaction
            try:
                context.save("autosave")
            except Exception:
                pass
            console.print()  # Spacer line
            
        except KeyboardInterrupt:
            console.print("\n[travel.info]Operation cancelled. Type /exit to quit.[/]\n")
        except EOFError:
            console.print("\n[travel.sand]Safe travels! Goodbye.[/]")
            break
        except Exception as e:
            console.print(f"[travel.error]An unexpected error occurred: {e}[/]\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
