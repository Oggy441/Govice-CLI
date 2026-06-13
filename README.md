# Govice CLI
### Your AI-Powered Terminal Travel Companion

```
 ██████╗  ██████╗ ██╗    ██╗██╗ ██████╗███████╗
██╔════╝ ██╔═══██╗██║   ██║██║██╔════╝██╔════╝
██║  ███╗██║   ██║██║   ██║██║██║     █████╗  
██║   ██║██║   ██║╚██╗ ██╔╝██║██║     ██╔══╝  
╚██████╔╝╚██████╔╝ ╚████╔╝ ██║╚██████╗███████╗
 ╚═════╝  ╚═════╝   ╚═══╝  ╚═╝ ╚═════╝╚══════╝
```

**Govice CLI** (Go + Advice) is a premium terminal-based AI travel assistant that provides real-time information, budget estimates, local points of interest, weather forecasts, and structured day-by-day travel itineraries. Powered by a conversational AI agent (Gemini 2.5 Flash / Gemma) and integrating live public APIs, it features a polished, responsive command-line UI built with `rich` and `prompt_toolkit`.

---

## 🌟 Key Features

- **Interactive AI Chatbot**: Talk to a travel agent that maintains context of your destination, budget, and travel length. Supports automatic function-calling (weather, attractions, currency rates).
- **Day-by-Day Itineraries**: Generate detailed daily schedules, dining ideas, and transport recommendations using `/plan`.
- **Live Weather Updates**: Fetch real-time weather and a 3-day forecast for any city worldwide using Open-Meteo.
- **Accommodation & POI Recommendations**: Discover top-rated local tourist attractions and recommended hotels (budget, mid-range, luxury).
- **Flight Route Estimates**: Query estimates for airlines, duration, and pricing structures between cities.
- **Budgeting Tool**: Generate detailed itemized travel expenses (accommodation, food, activities) converted to your preferred currency.
- **Session Persistence**: Easily save and resume your custom travel plans and chat logs to JSON files.

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Oggy441/Govice-CLI.git
cd Govice-CLI
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Ensure you have the required dependencies installed:
```bash
pip install google-genai httpx python-dotenv prompt-toolkit rich
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (or copy `.env.example` if available):
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash # or gemini-2.0-flash / gemma-4-31b-it

# Optional keys for live Local Attractions
GEOAPIFY_API_KEY=your_geoapify_key
OPENTRIPMAP_API_KEY=your_opentripmap_key
```

*Note: If a `GEMINI_API_KEY` is not present on launch, the CLI will prompt you to enter one directly.*

---

## 🛠 Usage

To launch the Govice CLI:
```bash
python main.py
```

### Verification
You can verify that the third-party integrations (weather, currency rates, geocoding) are configured and functioning correctly by running:
```bash
python verify_apis.py
```

---

## 📖 Command Reference

Govice CLI supports a variety of slash commands for targeted travel planning tasks:

| Command | Description | Example |
| :--- | :--- | :--- |
| `/plan <destination> <days>` | Generate a day-by-day travel itinerary | `/plan Tokyo 5` |
| `/weather <city>` | Fetch live weather details and forecast | `/weather Paris` |
| `/flights <from> <to> <date>` | Estimate flight routes and cost ranges | `/flights NYC Tokyo 2026-09-01` |
| `/hotels <city>` | Get points of interest and hotel details | `/hotels Rome` |
| `/budget <destination> <days>` | Generate estimated expense breakdown | `/budget Iceland 7` |
| `/save <name>` | Save active session context to disk | `/save my_japan_trip` |
| `/load <name>` | Load a previously saved trip session | `/load my_japan_trip` |
| `/clear` | Reset active trip context and chat history | `/clear` |
| `/exit` | Exit the travel assistant | `/exit` |

---

## 🎨 Design Theme
Adhering to modern visual aesthetics, the CLI utilizes a custom terminal stylesheet:
- **Primary Teal (`#006d77`)**: Emphasized accents and console statuses.
- **Secondary Warm Sand (`#e29578`)**: Context indicators and tables.
- **Amber Gold (`#e9c46a`)**: Highlights and command usage suggestions.
- **Dark Charcoal Background**: Optimized for modern terminals.
