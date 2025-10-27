# MCP-farm – Gårds- och Småbruksassistent

Detta projekt är en **intelligent uppgifts- och prioriteringshanterare** för småbruk eller gemenskaper. Systemet använder en **agent/LLM** för att generera, berika och sortera uppgifter baserat på prioritet, säsong och annan relevant information.

---

## Funktioner

- **Task management:**  
  Skapa och hantera uppgifter med titel och prioritet.  

- **LLM-genererade uppgifter:**  
  Agenten kan skapa fullständiga uppgifter med beskrivning, förberedelser, praktiska instruktioner och eventuella bidrag.  

- **Automatisk berikning:**  
  Om en uppgift saknar beskrivning kan agenten generera rekommendationer och detaljer.  

- **Dubblettkontroll:**  
  Identifierar och tar bort duplicerade uppgifter automatiskt.  

- **Prioritering:**  
  Uppgifter sorteras efter prioritet (1–5) och relevans.  

- **Flexibel front-end:**  
  Kan köras i terminalen eller via en **Streamlit-webbapp** med interaktiva knappar för att lägga till uppgifter, köra agenten och visa task-listan.

---

## Exempel på användning

- Lägg till en manuell uppgift med titel och prioritet, låt agenten fylla i resten:  
  ```python
  new_task = env.add_task(title="Bygga växthus", priority=3)

## Vad jag lärt mig

[x] Integrera LLM/agenter med Python och hantera JSON-data.
[x] Skapa en modellbaserad struktur med Pydantic (Task, Observation, Action).
[x] Skillnaden mellan manuella användarinput och automatgenererade data.
[x] Konvertering och validering av olika typer (str, int, list, dict) för att undvika fel vid serialization.
[x] Bygga en enkel, responsiv frontend med Streamlit.

## Framtida förbättringar

- Lägg till historik/logg över alla utförda åtgärder.
- Implementera notiser/alerts för prioriterade uppgifter.
- Möjlighet att redigera uppgifter direkt i Streamlit.
- Exportera uppgifter till CSV / Excel / PDF.
- Låt LLM föreslå prioritet automatiskt baserat på säsong, tidåtgång, bidrag eller arbetsinsats.
- Koppla projektet till en kalender eller planeringssystem.
- Förbättra LLM-kommunikationen med mer avancerade prompter och templates.