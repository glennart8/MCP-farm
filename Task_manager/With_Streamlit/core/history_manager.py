from pathlib import Path
from datetime import datetime
import json
from .models import Task

class HistoryManager:
    def __init__(self, history_path="history.json"):
        self.history_path = Path(history_path)
        self.history = []
        self._load_history()

    def _load_history(self):
        if self.history_path.exists():
            with open(self.history_path, "r", encoding="utf-8") as f:
                self.history = json.load(f)

    def _save_history(self):
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def log_action(self, action_type: str, task: Task, info: str = ""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "title": task.title,
            "priority": task.priority,
            "description": task.description,
            "preparations": task.preparations,
            "practical_desc": task.practical_desc,
            "grants": task.grants,
            "info": info
        }
        self.history.append(entry)
        self._save_history()

