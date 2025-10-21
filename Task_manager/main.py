from pprint import pprint
from environment import Environment
from agent import Agent

env = Environment()
agent = Agent()

for step in range(3):  
    print(f"\n=== Steg {step + 1} ===")
    
    # --- OBSERVERA ---
    observation = env.get_state()
    print("Observation:")
    pprint(observation, width=80)

    # --- BESLUTA ---
    action = agent.decide(observation)
    print("\nVald åtgärd:")
    pprint(action, width=80)

    # --- KÖR BESLUT ---
    if action["type"] == "update":
        # Använd kwargs istället för content
        result = env.update_task(action["index"], **action["kwargs"])
        print("\nResultat:", result)
    elif action["type"] == "none":
        print("\nAlla uppgifter har redan en beskrivning.")
    else:
        print("\nOkänd åtgärdstyp:", action["type"])
