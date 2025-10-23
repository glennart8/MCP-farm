from pprint import pprint
from environment import Environment
from agent import Agent


env = Environment()
agent = Agent()

# new_task=env.add_task(title="Bygga fårhus", priority=1)


while True:
    choice = input("""Vad vill du göra?
                   1. Vissa alla uppgifter
                   2. Lägg till uppgift
                   3. Generera utförlig beskrivning av uppgift
                   4. Generera ny uppgift (gemini)
                   5. Avsluta
                   """)

    if choice == "1":
        # Lägg till möjlighet att läsa fullständig info
        for i, t in enumerate(env.tasks):
            print(f"{i}: {t.title} (prio {t.priority})")

    elif choice == "2":
        print("\nLägg till uppgift:")
        title = input("Titel: ")
        priority = input("Prioritet (1 – 5): ")
        try:
            priority = int(priority)
        except ValueError:
            priority = 1  # sätter default om ingen int skrevs in

        new_task = env.add_task(title=title, priority=priority)
        print(f"Uppgiften '{new_task.title}' har skapats.\n")
        
            
    elif choice == "3":
        # Visa tasks
        for i, t in enumerate(env.tasks):
            print(f"{i}: {t.title}")
            
        task_to_edit = int(input("\nVilken task vill du generera mer info för (ange index): "))
        print(f"\nDu uppdaterar: {env.tasks[task_to_edit].title}")

        # Agenten skapar saknade fält
        task_update = agent.enrich_task_info(env.tasks[task_to_edit].title)

        # Uppdaterar den valda uppgiften i miljön
        env.update_task(task_to_edit, **task_update.model_dump())

        print(f"\nUppgiften '{env.tasks[task_to_edit].title}' har uppdaterats.")    
    elif choice == "4":
        print("\nGenererar ny uppgift med Gemini, vänta lite...")

        # Agenten skapa en ny Task
        new_task_from_gemini = agent.create_a_proper_task()

        # Lägg till uppgift i env
        env.add_task(
            title=new_task_from_gemini.title,
            priority=new_task_from_gemini.priority,
            description=new_task_from_gemini.description,
            preparations=new_task_from_gemini.preparations,
            practical_desc=new_task_from_gemini.practical_desc,
            grants=new_task_from_gemini.grants
        )
        
        print(f"Ny uppgift skapad: {new_task_from_gemini.title}")
        print(f"Beskrivning: {new_task_from_gemini.description}\n")
    elif choice == "5":
        break






if __name__ == "__main__":
    pass


for step in range(3):  
    print(f"\n=== Steg {step + 1} ===")
    
    # --- OBSERVERA ---
    observation = env.get_state()
    print("Observation:")
    pprint(observation, width=100)

    # --- BESLUTA --- 
    """
    Just nu endast att uppdatera en post med info för de som saknar description
    """
    action = agent.decide_what_to_do(observation)
    print("\nVald åtgärd:")
    pprint(action, width=100)

    # --- KÖR BESLUT ---
    if action["type"] == "update":
        # Använd kwargs istället för content
        result = env.update_task(action["index"], **action["kwargs"])
        print("\nResultat:", result)
    if action["type"] == "add":
        result = env.add_task(**action["kwargs"])

        print("\nResultat:", result)
    elif action["type"] == "none":
        print("\nAlla uppgifter har redan en beskrivning.")
    else:
        print("\nOkänd åtgärdstyp:", action["type"])
