from pprint import pprint
from environment import Environment
from agent import Agent


env = Environment()
agent = Agent()

# new_task=env.add_task(title="Bygga fårhus", priority=1)

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
