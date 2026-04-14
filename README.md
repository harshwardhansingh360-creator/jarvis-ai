# J.A.R.V.I.S — Proactive Intelligence System

A full-stack AI productivity assistant with four intelligence modules, built on Streamlit + Anthropic Claude.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Either set as an environment variable:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Or enter it directly in the app's login screen.

### 3. Run
```bash
streamlit run app.py
```

---

## Four Modules

### ⚡ Predict — Proactive Intelligence Engine
- Context-aware cards that auto-update based on time of day
- Covers 6 circadian windows: Early Morning, Deep Work, Midday, Afternoon, Wind-Down, Night
- AI-generated personalised briefings with neuroscience-backed insights
- No user input required — JARVIS predicts what you need

### 💬 Chat — JARVIS Persona
- Full Claude AI conversation with sharp JARVIS advisor persona
- Quick prompt buttons for common queries
- Persistent conversation history within session
- Direct, advisor-level responses — not generic chatbot answers

### 🧠 Thought Dump — Cognitive Offloading
- Brain-dump raw, messy thoughts in freeform text
- AI instantly organises into 5 categories:
  - Urgent Actions
  - This Week
  - Someday / Maybe
  - Ideas & Opportunities
  - Emotional Check-ins
- Surfaces your top priority for the next hour
- JARVIS insight on your current cognitive state

### 📊 Life Pulse — Real-Time Dashboard
- Cognitive load tracking (session-aware)
- Circadian rhythm chart for the day
- 5 performance indicators with live progress bars
- Session activity log
- AI-powered deep analysis of your patterns

---

## Architecture

```
app.py
├── Time context engine (6 windows × 3 cards = 18 proactive cards)
├── Session state manager (cognitive load, focus score, activity log)
├── Module 1: Predict (static cards + Claude briefing)
├── Module 2: Chat (multi-turn Claude conversation)
├── Module 3: Thought Dump (JSON-structured Claude output)
└── Module 4: Life Pulse (Plotly charts + Claude analysis)
```

## Model Used
`claude-opus-4-5` — all four AI-powered features use this model.

## Notes
- No data is stored beyond the current browser session
- Cognitive load and focus scores are session-derived estimates
- The circadian rhythm chart generates realistic synthetic data for illustration
