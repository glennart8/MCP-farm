import streamlit as st
from core.environment import Environment
from core.agent import Agent

st.set_page_config(
    page_title="TaskFarm",
    layout="wide",  
    initial_sidebar_state="expanded"
)

image_url = "https://images.unsplash.com/photo-1444858291040-58f756a3bdd6?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1378"

st.markdown(
    f"""
    <style>
    .stApp {{
        /* Bakgrundsbild + mörk overlay */
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
            url("{image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


env = Environment()
agent = Agent()

st.title("Task Manager")

col1, col2 = st.columns(2)

with col1:
    # Lägg till task manuellt
    st.header("Lägg till uppgift")
    with st.form("add_task_form"):
        title = st.text_input("Titel")
        priority = st.number_input("Prioritet (1–5)", min_value=1, max_value=5, step=1)
        submitted = st.form_submit_button("Lägg till uppgift")
        if submitted:
            new_task = env.add_task(title=title, priority=priority)
            st.success(f"Ny uppgift skapad: {new_task.title} (prio {new_task.priority})")
            
# --- Hämta uppgifter och titlar ---
with col2:
    tasks = env.get_tasks()
    
    # Skapa en lista med titel och prioritet ihopslagna
    sorted_tasks = sorted(tasks, key=lambda t: -t.priority)
    task_and_prio = [f"{t.title} - Prio: {t.priority}" for t in sorted_tasks]

    st.subheader("Välj en uppgift")
    selected_option = st.selectbox("Välj en task:", task_and_prio)

    # Ta bort prioritet ur task_and_prio
    selected_title = selected_option.split(' - Prio:')[0]
    selected_task = next((t for t in tasks if t.title == selected_title), None)

    if selected_task:
        st.write(f"**Titel:** {selected_task.title}")
        st.write(f"**Prioritet:** {selected_task.priority}")
        st.write(f"**Beskrivning:** {selected_task.description}")
        st.write(f"**Förberedelser:** {selected_task.practical_desc}")
        st.write(f"**Grants:** {selected_task.grants}")


with col1:        
    # Generera task via Gemini
    st.header("Generera ny uppgift")
    if st.button("Skapa med Gemini"):
        new_task = agent._create_task()
        env.add_generated_task(new_task)
        st.success(f"Ny uppgift skapad: {new_task.title}")
        st.write(f"Beskrivning: {new_task.description}")
    
    # MCP - Observe, decide, act
    st.header("Låt agenten agera")
    if st.button("Kör agent"):
        while True:
            obs = env.observe()
            action = agent.decide(obs)
            result = env.act(action)
            st.write(result)
            if action.type == "none":
                break
            
with col2:
    pass