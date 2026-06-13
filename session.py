import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from config import SESSIONS_DIR

@dataclass
class TripContext:
    destination: Optional[str] = None
    days: Optional[int] = None
    budget: Optional[float] = None
    currency: str = "INR"
    saved_itinerary: Optional[str] = None
    chat_history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TripContext":
        return cls(
            destination=data.get("destination"),
            days=data.get("days"),
            budget=data.get("budget"),
            currency=data.get("currency", "INR"),
            saved_itinerary=data.get("saved_itinerary"),
            chat_history=data.get("chat_history", [])
        )

    def save(self, name: str) -> str:
        """Saves current session context to a JSON file in sessions dir. Returns file path."""
        # Sanitize name
        clean_name = "".join(c for c in name if c.isalnum() or c in ("-", "_")).strip()
        if not clean_name:
            clean_name = "default"
        filepath = SESSIONS_DIR / f"{clean_name}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
        return str(filepath)

    @classmethod
    def load(cls, name: str) -> Optional["TripContext"]:
        """Loads a session by name from the sessions dir."""
        clean_name = "".join(c for c in name if c.isalnum() or c in ("-", "_")).strip()
        filepath = SESSIONS_DIR / f"{clean_name}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def list_saved_sessions(cls) -> List[str]:
        """Lists names of all saved session files (without extension)."""
        if not SESSIONS_DIR.exists():
            return []
        return [f.stem for f in SESSIONS_DIR.glob("*.json")]
