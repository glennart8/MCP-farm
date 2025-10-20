from environment import Environment

env = Environment()
print(env.observe())
print(env.apply({"type": "add", "content": "Testa miljön"}))
print(env.observe())
