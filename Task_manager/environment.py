import json
from models import Task, Observation, Action

class Environment:
    def __init__(self, path="tasks.json"):
        self.path = path
        self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task(**t) for t in data]
        except FileNotFoundError:
            self.tasks = []
            self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in self.tasks], f, ensure_ascii=False, indent=2)

    # === MCP hooks ===
    def observe(self) -> Observation:
        """Returnerar nuvarande miljötillstånd."""
        return Observation(tasks=self.tasks)

    def act(self, action: Action):
        """Utför en handling som agenten har beslutat."""
        # Lägg till
        if action.type == "add" and action.task:
            self.tasks.append(action.task)
            self._save()
            return f"Added: {action.task.title}"

        # Uppdatera
        elif action.type == "update" and action.index is not None and action.task:
            for key, val in action.task.model_dump().items():
                if val is not None:
                    setattr(self.tasks[action.index], key, val)
            self._save()
            return f"Updated: {self.tasks[action.index].title}"
        
        # Ta bort
        elif action.type == "delete" and action.index is not None:
            removed = self.tasks.pop(action.index)
            self._save()
            return f"Deleted: {removed.title}"

        elif action.type == "none":
            return "Nothing to do."

        else:
            return "Unknown action type."




    # Publik metod som anropas "manuellt" av anv
    def add_task(self, title: str, priority: int):
        task = Task(title=title, priority=priority)
        self.tasks.append(task)
        self._save()
        return task
    
    def add_generated_task(self, task: Task):
        """Lägg till en färdiggenererad uppgift från AI-agenten."""
        self.tasks.append(task)
        self._save()
        return task