from pathlib import Path
import json

class ComplaintsSystem:
    """Hanterar alla kundklagomål (complaints) och sparar dem till fil."""
    
    def __init__(self, file_path="../logs/complaints.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.complaints = []
        self._load_complaints()

    def _load_complaints(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_complaints(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.complaints, f, ensure_ascii=False, indent=2)

    def create_complaint(self, email):
        complaint = {
            "from": email["from"],
            "subject": email["subject"],
            "body": email["body"],
            "status": "open"
        }
        print(f"Skapar klagomål: '{complaint['subject']}'")
        self.complaints.append(complaint)
        self._save_complaints()

