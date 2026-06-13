import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SESSIONS_DIR = DATA_DIR / "sessions"

# Automatically create .env from .env.example if .env does not exist
env_file = BASE_DIR / ".env"
env_example = BASE_DIR / ".env.example"
if not env_file.exists() and env_example.exists():
    try:
        shutil.copy(env_example, env_file)
    except Exception:
        pass

# Load environment variables from .env
load_dotenv(dotenv_path=env_file)

# Ensure directories exist
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

def has_gemini_key() -> bool:
    return bool(GEMINI_API_KEY)

def set_gemini_key(key: str, save_to_env: bool = False):
    """Set Gemini API key for the current session, optionally saving to .env"""
    global GEMINI_API_KEY
    GEMINI_API_KEY = key
    os.environ["GEMINI_API_KEY"] = key
    
    if save_to_env:
        env_file = BASE_DIR / ".env"
        lines = []
        if env_file.exists():
            try:
                lines = env_file.read_text(encoding="utf-8").splitlines()
            except Exception:
                pass
            
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={key}")
                updated = True
            else:
                new_lines.append(line)
                
        if not updated:
            new_lines.append(f"GEMINI_API_KEY={key}")
            
        try:
            env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        except Exception:
            pass
