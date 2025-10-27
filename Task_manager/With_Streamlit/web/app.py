import sys
from pathlib import Path

# Lägg till projektets root-mapp (With_Streamlit) i sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.environment import Environment
from core.agent import Agent

env = Environment()
agent = Agent()

st.title("Task Manager")

# Lägg till task manuellt
st.header("Lägg till uppgift")
with st.form("add_task_form"):
    title = st.text_input("Titel")
    priority = st.number_input("Prioritet (1–5)", min_value=1, max_value=5, step=1)
    submitted = st.form_submit_button("Lägg till uppgift")
    if submitted:
        new_task = env.add_task(title=title, priority=priority)
        st.success(f"Ny uppgift skapad: {new_task.title} (prio {new_task.priority})")

# Visa alla tasks
st.subheader("Alla uppgifter")
for t in env.get_tasks():
    st.write(f"{t.title} — Prioritet: {t.priority}")
    
# Generera task via Gemini
st.header("Generera ny uppgift")
if st.button("Skapa med Gemini"):
    new_task = agent._create_task()
    env.add_generated_task(new_task)
    st.success(f"Ny uppgift skapad: {new_task.title}")
    st.write(f"Beskrivning: {new_task.description}")

# Agenten agerar
st.header("Låt agenten agera")
if st.button("Kör agent"):
    obs = env.observe()
    action = agent.decide(obs)
    
    if action.type == "add" and action.task:
        # Om det är en fullständig Task från agent/LLM
        env.add_generated_task(action.task)
        st.success(f"Ny uppgift tillagd: {action.task.title}")
    
    elif action.type == "update":
        env.tasks[action.index] = action.task
        env._save()
        st.success(f"Task '{action.task.title}' uppdaterad!")
        
    elif action.type == "delete":
        deleted_task = env.tasks.pop(action.index)
        env._save()
        st.success(f"Task '{deleted_task.title}' raderad!")
    else:
        st.info("Inga åtgärder behövdes.")