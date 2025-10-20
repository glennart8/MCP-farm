import random

class Agent:
    def __init__(self):
        pass

    def decide(self, observation):
        """Ta ett beslut baserat på observationen (innehållet i data.json)."""
        notes = observation["notes"]

        # Om det finns färre än 5 anteckningar, lägg till en ny
        if len(notes) < 5:
            new_note = f"Ny idé {random.randint(1,100)}"
            return {"type": "add", "content": new_note}

        # Annars: slumpa mellan att ta bort eller uppdatera
        action_type = random.choice(["remove", "update"])
        index = random.randint(0, len(notes)-1)

        if action_type == "remove":
            return {"type": "remove", "content": notes[index]}
        else:
            new_content = notes[index] + " (uppdaterad)"
            return {"type": "update", "index": index, "content": new_content}
