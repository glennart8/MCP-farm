from environment import Environment
from agent import Agent
import time

env = Environment()
agent = Agent()

for step in range(5):
    print(f"\n=== Steg {step+1} ===")

    state = env.observe()
    print("Observation:", state)

    action = agent.decide(state)
    print("Vald åtgärd:", action)

    result = env.apply(action)
    print("Resultat:", result)

    time.sleep(1)
