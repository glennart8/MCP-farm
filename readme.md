# MCP – Mail

Detta projekt är en **intelligent assistent** för att hantera inkommande e-post och uppgifter för småföretag eller team. Systemet använder en **LLM/agent** för att analysera mejl, klassificera dem och automatiskt utföra åtgärder som supportärenden, försäljning, mötesbokningar eller autosvar.

---

## --- MCP FLOW ---
    
1. **Observe (Environment)** – Hämtar nya e-postmeddelanden via en lokal eller Gmail-klient.
2. **Decide (Agent)** – AI/LLM analyserar e-postens innehåll och bestämmer kategori:
   - `support` → skapa klagomål i systemet
   - `sales` → vidarebefordra till försäljning och skapa order
   - `meeting` → schemalägg möten i Google Calendar
   - `other` → skicka autosvar
3. **Act (Environment)** – Utför åtgärder automatiskt baserat på AI:s beslut.

---

## Funktioner

- **E-postklassificering:**  
  AI kan tolka inkommande mejl och avgöra om det rör support, försäljning, möte eller annat.

- **Support:**  
  Skapar automatiskt supportärenden baserat på klagomål och genererar autogenererade svar via LLM.

- **Försäljning:**  
  AI vidarebefordrar orderförfrågningar, skapar låtsasorder, och skickar automatiska orderbekräftelser.

- **Möteshantering:**  
  AI identifierar mötesförfrågningar i e-post, extraherar datum/tid, och lägger till möten direkt i Google Calendar.

- **Autosvar:**  
  Skickar automatiska svar på e-post som inte kräver annan åtgärd.

- **Loggning:**  
  Alla åtgärder loggas med avsändare, ämne, kategori, utförd åtgärd och produkt (om relevant).

---

## Teknisk struktur

- `classes/environment.py` – Hanterar e-postflödet, AI-beslut och utför åtgärder.
- `classes/autoresponder.py` – Genererar och skickar autosvar via Gmail API.
- `classes/complaints.py` – Skapar och hanterar supportärenden.
- `classes/sales.py` – Hanterar försäljningsflöden och låtsasorder.
- `classes/calendar.py` – Lägger till möten i Google Calendar.
- `classes/mail.py` – Lokalt testmail-system eller integration med Gmail.
- `controller.py` – Kör hela MCP-flödet: observe → decide → act.

---

## Vad jag lärt mig

- [x] Integrera LLM/agent med Python och JSON-data.  
- [x] Skapa beslutslogik och automatiserade åtgärder baserat på AI-klassificering.  
- [x] Skicka e-post via Gmail API och hantera autentisering med `credentials.json`.  
- [x] Skapa möten automatiskt i Google Calendar baserat på texttolkning.  
- [x] Generera autogenererade svar för klagomål och försäljning.  
- [x] Hantera fallback-lösningar när tidpunkt eller produkt inte anges.  

## TODO
- [] Kräv att ett autogenererat mail granskas innan det skickas till kund, t.ex. vid offertbegäran

# MCP-farm – Gårds- och Småbruksassistent

Detta projekt är en **intelligent uppgifts- och prioriteringshanterare** för småbruk eller gemenskaper. Systemet använder en **agent/LLM** för att generera, berika och sortera uppgifter baserat på prioritet, säsong och annan relevant information.


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


## Vad jag lärt mig

- [x] Integrera LLM/agenter med Python och hantera JSON-data.
- [x] Skapa en modellbaserad struktur med Pydantic (Task, Observation, Action).
- [x] Skillnaden mellan manuella användarinput och automatgenererade data.
- [x] Konvertering och validering av olika typer (str, int, list, dict) för att undvika fel vid serialization.
- [x] Bygga en enkel, responsiv frontend med Streamlit.


## Framtida förbättringar

- Lägg till historik/logg över alla utförda åtgärder.
- Implementera notiser/alerts för prioriterade uppgifter.
- Möjlighet att redigera uppgifter direkt i Streamlit.
- Exportera uppgifter till CSV / Excel / PDF.
- Låt LLM föreslå prioritet automatiskt baserat på säsong, tidåtgång, bidrag eller arbetsinsats.
- Koppla projektet till en kalender eller planeringssystem.
- Förbättra LLM-kommunikationen med mer avancerade prompter och templates.