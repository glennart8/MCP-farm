import json
from pathlib import Path
from .models import Task, Observation, Action
from agent import Agent

agent = Agent()

class Environment:
    def __init__(self, file_path="tasks.json"):
        self.file_path = Path(file_path)
        self.tasks = []
        self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task(**t) for t in data]

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([t.model_dump() for t in self.tasks], f, ensure_ascii=False, indent=2)

    # Publik metod som anropas "manuellt" av användare
    def add_task(self, title: str, priority: int):
        task = Task(title=title, priority=priority)
        self.tasks.append(task)
        self._save()
        return task
    
    # LLM lägger in uppgift
    def add_generated_task(self, task: Task):
        """Lägg till en Task med alla fält (för Gemini/agenten)."""
        self.tasks.append(task)
        self._save()
        return task

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def observe(self) -> Observation:
        return Observation(tasks=self.tasks)
    
    def act(self, action: Action):
        """Utför en given action från agenten."""
        if action.type == "delete" and action.index is not None:
            removed = self.tasks.pop(action.index)
            self._save()
            return f"Deleted: {removed.title}"

        if action.type == "update" and action.index is not None and action.task:
            self.tasks[action.index] = action.task
            self._save()
            return f"Updated: {self.tasks[action.index].title}"

        if action.type == "add" and action.task:
            if not isinstance(action.task, Task):
                action.task = Task(**action.task)
            self.tasks.append(action.task)
            self._save()
            return f"Added: {action.task.title}"

        return "Nothing to do."





