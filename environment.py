import json
from pathlib import Path

class Environment:
    def __init__(self, filename="data.json"):
        self.file = Path(filename)
        if not self.file.exists():
            self._init_file()

    def _init_file(self):
        """Skapa en grundfil med lite startdata."""
        data = {"notes": ["Lär mig om AI", "Skriv en enkel agent"]}
        self._save(data)

    def _load(self):
        """Läs in JSON-filen."""
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        """Spara JSON-filen."""
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def observe(self):
        """Returnera nuvarande tillstånd."""
        return self._load()

    def apply(self, action):
        """Utför en åtgärd (lägg till, ta bort, ändra anteckning)."""
        data = self._load()
        act_type = action.get("type")
        content = action.get("content")

        if act_type == "add":
            data["notes"].append(content)
            self._save(data)
            return f"Added: {content}"

        elif act_type == "remove":
            if content in data["notes"]:
                data["notes"].remove(content)
                self._save(data)
                return f"Removed: {content}"
            return f"Note not found: {content}"

        elif act_type == "update":
            idx = action.get("index", 0)
            if 0 <= idx < len(data["notes"]):
                old = data["notes"][idx]
                data["notes"][idx] = content
                self._save(data)
                return f"Updated: '{old}' → '{content}'"
            return "Invalid index."

        else:
            return "Unknown action type."
