from rich.console import Console
from rich.theme import Theme

# Define the custom travel theme with a Warm Sand & Deep Teal palette.
# Avoid using blue themes, adhering to user's guidelines.
travel_theme = Theme({
    # Accents & Roles
    "travel.teal": "bold #006d77",      # Primary Teal accent
    "travel.sand": "#e29578",           # Secondary Sand/Coral accent
    "travel.gold": "bold #e9c46a",      # Highlight Accent (Gold/Amber)
    "travel.error": "bold #e63946",     # Red error style
    "travel.success": "bold #2a9d8f",   # Green success style
    "travel.info": "#8d99ae",           # Muted grey text
    "travel.bg": "on #2b2d42",          # Dark charcoal background style
    
    # Text types
    "travel.command": "bold #e9c46a",   # Slash commands in help / inputs
    "travel.text": "#edf6f9",           # Neutral light text
    "travel.header": "bold #006d77",    # Section headers
    "travel.border": "#006d77",         # Default panel border
})

# Single shared console instance with custom theme
console = Console(theme=travel_theme)
