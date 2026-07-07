# ✈️ Travel-CLI: AI Travel Agent

Travel-CLI is an interactive, AI-powered command-line interface designed to help you plan your next adventure. Powered by Google Gemini, it combines a conversational AI agent with structured commands to manage itineraries, budgets, and travel logistics.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Google Gemini API Key (get one for free at [Google AI Studio](https://aistudio.google.com/))

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd travel-cli
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
The application requires a Google Gemini API key to enable the conversational AI agent. You can provide it in three ways:

1. **Environment Variable (Recommended for Production):**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
2. **`.env` File (Project Root):**
   Create a file named `.env` in the project root with the following content:
   ```ini
   GEMINI_API_KEY="your_api_key_here"
   ```
3. **Interactive Setup:** Simply run the application. If no key is found, the CLI will prompt you to enter your key and offer to save it to a `.env` file for future sessions.

Additional configuration options (default currency, autosave behavior, etc.) can be modified in `config.py`.

## 🛠 Usage

Start the agent by running the main entry point:
```bash
python main.py
```

### Conversational Mode
Simply type your requests naturally! The agent can help you brainstorm destinations, suggest activities, and refine your travel plans. It maintains context about your destination, budget, duration, and saved itinerary.
*Example: "I want to visit Japan for 10 days in October with a $3000 budget. What cities should I visit?"*

### Slash Commands
For structured actions and session management, use the following commands. Arguments containing spaces should be quoted (e.g., `/plan "Paris, France" 7`).

| Command | Description | Example Usage |
| :--- | :--- | :--- |
| `/plan` | Generate a structured travel itinerary for the current context. | `/plan` or `/plan "Tokyo, Japan" 14` |
| `/weather` | Check weather forecasts for the destination. | `/weather` or `/weather "London, UK"` |
| `/flights` | Search for flight options (requires origin/destination in context or args). | `/flights` or `/flights "JFK" "HND"` |
| `/hotels` | Find accommodation recommendations. | `/hotels` or `/hotels "Paris, France"` |
| `/budget` | Manage and calculate travel expenses. | `/budget` or `/budget add "Flight" 500` |
| `/save` | Manually save the current session to a named file. | `/save my_trip` |
| `/load` | Restore a previously saved session by name. | `/load my_trip` |
| `/clear` | Clear the current session context and history. | `/clear` |
| `/help` | Display the help menu with command details. | `/help` |
| `/exit` | Close the application (aliases: `/quit`). | `/exit` |

## 🧠 Features
- **Persistent Memory:** The CLI automatically saves your session to an `autosave` file on every interaction, allowing you to resume your planning with full context and chat history intact.
- **Context-Aware AI Agent:** The `TravelAgent` tracks your destination, budget, duration, currency, and itinerary throughout the conversation to provide highly relevant, personalized suggestions.
- **Rich Terminal UI:** Built with `rich` and `prompt_toolkit`, featuring themed colors, a dynamic status bar (showing destination, days, budget), and command auto-completion.
- **Graceful Fallbacks:** If the AI agent fails to initialize (e.g., missing API key), the system remains fully functional through the command-driven interface.
- **Session Management:** Full save/load/clear workflow for managing multiple trip plans.
- **API Verification Utility:** Includes `verify_apis.py` to validate connectivity to external travel APIs (Amadeus, OpenWeather, etc.) before planning.

## 📂 Project Structure
```
travel-cli/
├── main.py              # Application entry point, REPL loop, command routing
├── agent.py             # TravelAgent class: Gemini integration, chat history, tool use
├── api.py               # External API clients (Amadeus, OpenWeather, etc.)
├── config.py            # Configuration management (API keys, defaults, .env handling)
├── session.py           # TripContext: state management, serialization, autosave
├── verify_apis.py       # Script to verify external API connectivity
├── commands/            # Slash command implementations
│   ├── __init__.py
│   ├── budget.py
│   ├── flights.py
│   ├── hotels.py
│   ├── plan.py
│   ├── session_cmds.py
│   └── weather.py
└── ui/                  # User interface components
    ├── __init__.py
    ├── components.py    # Rich renderables (banner, status bar, help panel)
    └── theme.py         # Color themes and console style definitions
```

## 🤝 Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License
This project is licensed under the MIT License.