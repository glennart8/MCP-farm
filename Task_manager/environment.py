import json
from task_model import Task

class Environment:
    def __init__(self):
        self.data_file = "tasks.json"
        self._load_tasks()
        
    def _load_tasks(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task(**t) for t in data]
        except FileNotFoundError:
            self.tasks = []  # starta tomt om fil saknas
            self._save_tasks()


    def _save_tasks(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in self.tasks], f, ensure_ascii=False, indent=2)

    def get_state(self):
        # Returnera en lista av dicts för agenten
        return {"tasks": [t.dict() for t in self.tasks]}

    def add_task(self, title: str, priority: int):
        task = Task(title=title, priority=priority)
        self.tasks.append(task)
        self._save_tasks()
        return task

    def update_task(self, index, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.tasks[index], key):
                setattr(self.tasks[index], key, value)
        self._save_tasks()
        return f"Updated: {self.tasks[index].title}"
