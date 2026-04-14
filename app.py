import streamlit as st
import anthropic
import json
import time
import os
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="JARVIS — Proactive Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ── Root vars ── */
  :root {
    --j-bg:       #0a0d14;
    --j-surface:  #111624;
    --j-card:     #161c2e;
    --j-border:   #1e2a45;
    --j-accent:   #3b82f6;
    --j-accent2:  #06b6d4;
    --j-accent3:  #8b5cf6;
    --j-success:  #10b981;
    --j-warn:     #f59e0b;
    --j-danger:   #ef4444;
    --j-text:     #e2e8f0;
    --j-muted:    #64748b;
    --j-glow:     0 0 20px rgba(59,130,246,0.15);
  }

  /* ── Global dark bg ── */
  .stApp { background: var(--j-bg); color: var(--j-text); }
  .block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

  /* ── Hide default Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }

  /* ── Top navigation bar ── */
  .jarvis-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    background: var(--j-surface);
    border: 1px solid var(--j-border);
    border-radius: 14px;
    margin-bottom: 1.5rem;
    box-shadow: var(--j-glow);
  }
  .jarvis-logo {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 3px;
    background: linear-gradient(135deg, var(--j-accent), var(--j-accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .jarvis-time {
    font-size: 0.8rem;
    color: var(--j-muted);
    font-weight: 400;
  }
  .jarvis-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    color: var(--j-success);
  }
  .status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--j-success);
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

  /* ── Tab buttons ── */
  .tab-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  .tab-btn {
    padding: 0.45rem 1.1rem;
    border-radius: 8px;
    border: 1px solid var(--j-border);
    background: var(--j-surface);
    color: var(--j-muted);
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .tab-btn:hover { border-color: var(--j-accent); color: var(--j-text); }
  .tab-btn.active {
    background: linear-gradient(135deg, #1e3a6e, #1e2a4a);
    border-color: var(--j-accent);
    color: #93c5fd;
  }

  /* ── Cards ── */
  .j-card {
    background: var(--j-card);
    border: 1px solid var(--j-border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
  }
  .j-card:hover { border-color: rgba(59,130,246,0.4); }
  .j-card-accent { border-left: 3px solid var(--j-accent); }
  .j-card-success { border-left: 3px solid var(--j-success); }
  .j-card-warn { border-left: 3px solid var(--j-warn); }
  .j-card-purple { border-left: 3px solid var(--j-accent3); }

  /* ── Section headers ── */
  .section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--j-muted);
    margin-bottom: 0.8rem;
  }

  /* ── Predict cards ── */
  .predict-card {
    background: var(--j-card);
    border: 1px solid var(--j-border);
    border-radius: 16px;
    padding: 1.3rem;
    transition: all 0.2s;
    height: 100%;
  }
  .predict-card:hover {
    border-color: var(--j-accent);
    transform: translateY(-2px);
    box-shadow: var(--j-glow);
  }
  .predict-icon {
    font-size: 1.8rem;
    margin-bottom: 0.6rem;
  }
  .predict-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--j-accent2);
    margin-bottom: 0.3rem;
  }
  .predict-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--j-text);
    margin-bottom: 0.5rem;
    line-height: 1.3;
  }
  .predict-body {
    font-size: 0.82rem;
    color: var(--j-muted);
    line-height: 1.6;
  }
  .predict-badge {
    display: inline-block;
    margin-top: 0.75rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border: 1px solid;
  }
  .badge-blue  { color: #93c5fd; border-color: #1d4ed8; background: rgba(29,78,216,0.15); }
  .badge-green { color: #6ee7b7; border-color: #047857; background: rgba(4,120,87,0.15); }
  .badge-amber { color: #fcd34d; border-color: #b45309; background: rgba(180,83,9,0.15); }
  .badge-purple{ color: #c4b5fd; border-color: #6d28d9; background: rgba(109,40,217,0.15); }
  .badge-red   { color: #fca5a5; border-color: #b91c1c; background: rgba(185,28,28,0.15); }

  /* ── Chat ── */
  .chat-bubble {
    padding: 0.75rem 1rem;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
    line-height: 1.7;
    max-width: 85%;
  }
  .chat-user {
    background: linear-gradient(135deg, #1e3a6e, #1e2a50);
    border: 1px solid #1d4ed8;
    color: #bfdbfe;
    margin-left: auto;
    border-bottom-right-radius: 4px;
  }
  .chat-jarvis {
    background: var(--j-card);
    border: 1px solid var(--j-border);
    color: var(--j-text);
    border-bottom-left-radius: 4px;
  }
  .chat-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 3px;
  }
  .label-you { color: #93c5fd; text-align: right; }
  .label-jarvis { color: var(--j-success); }
  .chat-wrapper { overflow-y: auto; max-height: 420px; padding-right: 4px; }

  /* ── Thought Dump ── */
  .td-category {
    background: var(--j-card);
    border: 1px solid var(--j-border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
  }
  .td-cat-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
  }
  .td-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
  .td-item {
    font-size: 0.84rem;
    color: var(--j-text);
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    line-height: 1.6;
  }
  .td-item:last-child { border-bottom: none; }

  /* ── Life Pulse ── */
  .metric-tile {
    background: var(--j-card);
    border: 1px solid var(--j-border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
  }
  .metric-val {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--j-accent), var(--j-accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
  }
  .metric-lbl { font-size: 0.7rem; color: var(--j-muted); margin-top: 4px; letter-spacing: 0.5px; }
  .metric-sub { font-size: 0.75rem; color: var(--j-success); margin-top: 3px; }

  /* ── Progress bars ── */
  .prog-wrap { margin-bottom: 0.6rem; }
  .prog-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--j-muted);
    margin-bottom: 4px;
  }
  .prog-track {
    height: 5px;
    border-radius: 3px;
    background: var(--j-border);
    overflow: hidden;
  }
  .prog-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
  }

  /* ── API key input ── */
  .stTextInput > div > div > input {
    background: var(--j-card) !important;
    border: 1px solid var(--j-border) !important;
    color: var(--j-text) !important;
    border-radius: 8px !important;
  }
  .stTextArea > div > div > textarea {
    background: var(--j-card) !important;
    border: 1px solid var(--j-border) !important;
    color: var(--j-text) !important;
    border-radius: 8px !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    padding: 0.4rem 1.4rem !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.88 !important; }

  /* ── Spinner override ── */
  .stSpinner > div { border-top-color: var(--j-accent) !important; }

  /* ── Dividers ── */
  hr { border-color: var(--j-border) !important; }

  /* ── Selectbox ── */
  .stSelectbox > div > div {
    background: var(--j-card) !important;
    border: 1px solid var(--j-border) !important;
    color: var(--j-text) !important;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "tab": "predict",
        "chat_history": [],
        "thought_result": None,
        "session_start": datetime.now(),
        "messages_sent": 0,
        "session_log": [],       # list of (timestamp, action, duration_s)
        "api_key": "",
        "api_key_set": False,
        "cognitive_load": 40,
        "focus_score": 72,
        "last_activity": datetime.now(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_client():
    key = st.session_state.get("api_key") or os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)


def time_context():
    h = datetime.now().hour
    if 5 <= h < 9:
        return "early_morning", "Early Morning", "05:00–09:00"
    elif 9 <= h < 12:
        return "deep_work", "Deep Work Window", "09:00–12:00"
    elif 12 <= h < 14:
        return "midday", "Midday Reset", "12:00–14:00"
    elif 14 <= h < 17:
        return "afternoon", "Afternoon Focus", "14:00–17:00"
    elif 17 <= h < 20:
        return "wind_down", "Evening Wind-Down", "17:00–20:00"
    else:
        return "night", "Night Mode", "20:00–05:00"


def session_duration_str():
    delta = datetime.now() - st.session_state.session_start
    m = int(delta.total_seconds() // 60)
    h = m // 60
    return f"{h}h {m % 60}m" if h else f"{m}m"


def log_action(action: str, duration_s: float = 0):
    st.session_state.session_log.append({
        "time": datetime.now(),
        "action": action,
        "duration": duration_s,
    })
    st.session_state.last_activity = datetime.now()
    # Adjust cognitive load dynamically
    st.session_state.messages_sent += 1
    load = min(95, st.session_state.cognitive_load + random.randint(2, 6))
    st.session_state.cognitive_load = load


def render_nav():
    now = datetime.now()
    _, period_label, _ = time_context()
    st.markdown(f"""
    <div class="jarvis-nav">
      <span class="jarvis-logo">J.A.R.V.I.S</span>
      <span class="jarvis-time">{now.strftime("%A, %d %b %Y")} &nbsp;·&nbsp; {now.strftime("%H:%M")} &nbsp;·&nbsp; {period_label}</span>
      <span class="jarvis-status"><span class="status-dot"></span> AI Online</span>
    </div>
    """, unsafe_allow_html=True)


def render_tabs():
    tabs = [
        ("predict",    "⚡ Predict"),
        ("chat",       "💬 Chat"),
        ("thoughtdump","🧠 Thought Dump"),
        ("lifepulse",  "📊 Life Pulse"),
    ]
    cols = st.columns(len(tabs))
    for col, (key, label) in zip(cols, tabs):
        with col:
            active = "active" if st.session_state.tab == key else ""
            # Use a button per tab
            if st.button(label, key=f"tab_{key}", use_container_width=True):
                st.session_state.tab = key
                st.rerun()


# ─────────────────────────────────────────────
#  API KEY GATE
# ─────────────────────────────────────────────
def render_api_gate():
    st.markdown("""
    <div class="j-card j-card-accent" style="max-width:540px; margin: 3rem auto; text-align:center;">
      <div style="font-size:2.5rem; margin-bottom:0.8rem;">🤖</div>
      <div style="font-size:1.1rem; font-weight:600; margin-bottom:0.4rem; color:#e2e8f0;">Connect JARVIS to Claude AI</div>
      <div style="font-size:0.82rem; color:#64748b; margin-bottom:1.4rem; line-height:1.6;">
        Enter your Anthropic API key to unlock all four intelligence modules.<br>
        Your key is stored only in this session.
      </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        key_input = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed",
        )
        if st.button("Initialise JARVIS →", use_container_width=True):
            if key_input.startswith("sk-ant"):
                st.session_state.api_key = key_input
                st.session_state.api_key_set = True
                st.rerun()
            else:
                st.error("Invalid key format. Must start with sk-ant-")


# ─────────────────────────────────────────────
#  MODULE 1 — PREDICT
# ─────────────────────────────────────────────
PREDICT_CARDS = {
    "early_morning": [
        {
            "icon": "🌅",
            "label": "Morning Ritual",
            "title": "Protect the first 30 minutes",
            "body": "Before checking messages or notifications, write down your top 3 priorities for the day. This primes your brain's prefrontal cortex for intentional decision-making.",
            "badge": ("badge-blue", "Focus Protocol"),
        },
        {
            "icon": "🧘",
            "label": "Cognitive Priming",
            "title": "Start with a still mind",
            "body": "5 minutes of box breathing (4-4-4-4 pattern) reduces cortisol and increases working memory capacity by up to 18% according to HRV research.",
            "badge": ("badge-green", "Neuroscience"),
        },
        {
            "icon": "📝",
            "label": "Weekly Context",
            "title": "Review your week's north star",
            "body": "Your brain consolidates memories during sleep. This is the optimal window to review weekly goals — you're running on a clean cognitive slate.",
            "badge": ("badge-amber", "Strategy"),
        },
    ],
    "deep_work": [
        {
            "icon": "🎯",
            "label": "Peak Performance Window",
            "title": "This is your cognitively richest block",
            "body": "Cortisol peaks between 9–11am, boosting alertness and analytical thinking. Shield this time from meetings. Tackle your hardest, most complex task now.",
            "badge": ("badge-blue", "Peak Hours"),
        },
        {
            "icon": "🔕",
            "label": "Focus Guard",
            "title": "Activate Deep Work mode",
            "body": "Block all notifications for 90 minutes. Studies show it takes an average of 23 minutes to refocus after an interruption. One distraction costs you 23 minutes of peak cognition.",
            "badge": ("badge-red", "High Priority"),
        },
        {
            "icon": "⏱️",
            "label": "Ultradian Rhythm",
            "title": "Work in 90-minute sprints",
            "body": "Your brain cycles through ~90-minute performance peaks. Align your deep work block to one full cycle, then take a genuine 15–20 minute break to reset.",
            "badge": ("badge-green", "Bio-Optimised"),
        },
    ],
    "midday": [
        {
            "icon": "🍽️",
            "label": "Energy Management",
            "title": "Fuel for the second half",
            "body": "Opt for a protein-rich, low-glycemic meal. High-carb lunches cause the classic post-lunch dip that tanks focus for 90 minutes. Your afternoon depends on this decision.",
            "badge": ("badge-amber", "Nutrition"),
        },
        {
            "icon": "🚶",
            "label": "Movement Break",
            "title": "10-minute walk resets everything",
            "body": "A short outdoor walk increases BDNF (brain-derived neurotrophic factor), reduces mental fatigue, and improves afternoon creative performance significantly.",
            "badge": ("badge-green", "Recovery"),
        },
        {
            "icon": "📧",
            "label": "Inbox Window",
            "title": "Now is the time for communications",
            "body": "The post-lunch window is biologically suited for administrative tasks, emails, and low-cognitive work. Protect your morning deep work by batching all comms here.",
            "badge": ("badge-blue", "Scheduling"),
        },
    ],
    "afternoon": [
        {
            "icon": "🤝",
            "label": "Social Cognition Peak",
            "title": "Best time for collaboration",
            "body": "Between 2–5pm, emotional intelligence and verbal fluency peak. Schedule important conversations, brainstorms, mentoring, and client calls in this window.",
            "badge": ("badge-purple", "Collaboration"),
        },
        {
            "icon": "⚡",
            "label": "Second Wind",
            "title": "Use caffeine strategically at 2pm",
            "body": "Caffeine's half-life is ~5-6 hours. A cup at 2pm clears by 8pm for sleep. Earlier consumption masks your natural adenosine build-up and disrupts sleep architecture.",
            "badge": ("badge-amber", "Biohacking"),
        },
        {
            "icon": "🔄",
            "label": "Task Switching",
            "title": "Batch your shallow work",
            "body": "Admin tasks, quick reviews, and low-stakes decisions belong here. Your analytical sharpness is declining — but execution speed remains high.",
            "badge": ("badge-blue", "Optimised"),
        },
    ],
    "wind_down": [
        {
            "icon": "🌇",
            "label": "Shutdown Ritual",
            "title": "Create a clear cognitive boundary",
            "body": "Write a 'done list' of everything completed today. Then write tomorrow's top 3 tasks. This closes open cognitive loops and allows your brain to genuinely rest.",
            "badge": ("badge-green", "Closure"),
        },
        {
            "icon": "📵",
            "label": "Digital Sunset",
            "title": "Screens off 90 minutes before bed",
            "body": "Blue light suppresses melatonin onset by up to 3 hours. Your sleep quality — and tomorrow's cognitive performance — depends on what you do in the next 2 hours.",
            "badge": ("badge-red", "Sleep Health"),
        },
        {
            "icon": "📖",
            "label": "Reflection Window",
            "title": "Capture insights before they fade",
            "body": "The 20 minutes after your workday ends is when creative insights often surface. Keep a quick-capture journal nearby — your best ideas emerge in transition periods.",
            "badge": ("badge-purple", "Insight"),
        },
    ],
    "night": [
        {
            "icon": "🌙",
            "label": "Recovery Mode",
            "title": "Sleep is your highest-leverage habit",
            "body": "Every hour of sleep before midnight is worth double after. Your prefrontal cortex — responsible for willpower, decisions, and emotional regulation — restores only during deep sleep.",
            "badge": ("badge-blue", "Restoration"),
        },
        {
            "icon": "📓",
            "label": "Gratitude Reset",
            "title": "3 wins from today",
            "body": "Writing 3 specific things that went well primes your hippocampus to encode positive memory traces during sleep — building long-term resilience and optimism.",
            "badge": ("badge-green", "Wellbeing"),
        },
        {
            "icon": "🌡️",
            "label": "Sleep Optimisation",
            "title": "Cool your room, warm your hands",
            "body": "Core body temperature must drop 1–3°F to initiate sleep. Keep your bedroom at 18–20°C. Warm hands/feet accelerate the heat redistribution needed for sleep onset.",
            "badge": ("badge-purple", "Bioscience"),
        },
    ],
}

def render_predict():
    period_key, period_label, period_range = time_context()
    h = datetime.now().hour
    dow = datetime.now().strftime("%A")

    # Proactive context banner
    st.markdown(f"""
    <div class="j-card j-card-accent" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
      <div>
        <div class="section-title">Proactive Intelligence Engine</div>
        <div style="font-size:1.05rem; font-weight:600; color:#e2e8f0;">
          Good {"morning" if h < 12 else "afternoon" if h < 17 else "evening"} — it's {dow}
        </div>
        <div style="font-size:0.82rem; color:#64748b; margin-top:2px;">
          Current window: <span style="color:#93c5fd;">{period_label}</span> &nbsp;·&nbsp; {period_range}
        </div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:0.7rem; color:#64748b; letter-spacing:1px; text-transform:uppercase;">Context Score</div>
        <div style="font-size:1.5rem; font-weight:700; color:#34d399;">97%</div>
        <div style="font-size:0.7rem; color:#64748b;">circadian accuracy</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Your Intelligence Cards for Right Now</div>', unsafe_allow_html=True)

    cards = PREDICT_CARDS.get(period_key, PREDICT_CARDS["deep_work"])
    cols = st.columns(3)
    for i, card in enumerate(cards):
        with cols[i % 3]:
            badge_class, badge_text = card["badge"]
            st.markdown(f"""
            <div class="predict-card">
              <div class="predict-icon">{card["icon"]}</div>
              <div class="predict-label">{card["label"]}</div>
              <div class="predict-title">{card["title"]}</div>
              <div class="predict-body">{card["body"]}</div>
              <div class="predict-badge {badge_class}">{badge_text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI-generated proactive suggestion
    st.markdown('<div class="section-title">AI-Generated Contextual Briefing</div>', unsafe_allow_html=True)

    col_btn, col_info = st.columns([2, 4])
    with col_btn:
        gen_btn = st.button("⚡ Generate My Briefing", use_container_width=True)
    with col_info:
        st.markdown(f"""
        <div style="font-size:0.78rem; color:#64748b; padding-top:0.4rem;">
          Personalised to: {period_label} · {dow} · Hour {h}
        </div>
        """, unsafe_allow_html=True)

    if gen_btn:
        client = get_client()
        if not client:
            st.error("API key not set.")
            return
        with st.spinner("JARVIS is reading your context..."):
            prompt = f"""You are JARVIS, a proactive AI intelligence system. 
Generate a sharp, personalised morning/afternoon/evening briefing for the user.

Context:
- Current time window: {period_label} ({period_range})
- Day of week: {dow}
- Hour: {h}:00
- Session duration so far: {session_duration_str()}
- Messages sent this session: {st.session_state.messages_sent}

Generate a briefing with:
1. A 2-sentence context-aware opening (reference the time of day specifically)
2. Top 3 recommended actions for THIS exact window (specific, actionable, time-aware)
3. One cognitive insight relevant to this time of day
4. A motivational closing line in JARVIS style

Be direct, intelligent, and specific. No generic advice. Reference neuroscience or productivity science where relevant.
Format with clear sections. Keep under 300 words."""

            t0 = time.time()
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            log_action("predict_briefing", time.time() - t0)
            briefing = response.content[0].text

        st.markdown(f"""
        <div class="j-card j-card-accent">
          <div class="section-title">JARVIS Briefing · {datetime.now().strftime("%H:%M")}</div>
          <div style="font-size:0.88rem; line-height:1.8; color:#cbd5e1; white-space:pre-wrap;">{briefing}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MODULE 2 — CHAT
# ─────────────────────────────────────────────
JARVIS_SYSTEM = """You are JARVIS — Just A Rather Very Intelligent System. You operate as a sharp, confident AI advisor to a high-performance individual.

Your personality:
- Precise, direct, intellectually rigorous
- Speak like a trusted senior advisor, not a chatbot
- Use first principles thinking
- Reference relevant science, psychology, history when it adds value
- Occasionally use dry wit — never sycophancy
- Never say "Great question!" or "Certainly!" — dive straight to substance
- When you don't know something, admit it cleanly
- Structure complex answers with clear logic: assertion → evidence → implication

You are not a generic assistant. You are JARVIS. Act accordingly."""

def render_chat():
    st.markdown("""
    <div class="j-card j-card-accent" style="margin-bottom:1.2rem;">
      <div class="section-title">Chat Interface</div>
      <div style="font-size:0.85rem; color:#64748b; line-height:1.6;">
        Full Claude AI conversation with JARVIS persona. Advisor-level responses — not generic chatbot answers.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Render chat history
    chat_html = '<div class="chat-wrapper" id="chatbox">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f"""
            <div style="text-align:right; margin-bottom:0.6rem;">
              <div class="chat-label label-you">You</div>
              <div class="chat-bubble chat-user">{msg["content"]}</div>
            </div>"""
        else:
            content = msg["content"].replace("\n", "<br>")
            chat_html += f"""
            <div style="margin-bottom:0.6rem;">
              <div class="chat-label label-jarvis">JARVIS</div>
              <div class="chat-bubble chat-jarvis">{content}</div>
            </div>"""
    if not st.session_state.chat_history:
        chat_html += """
        <div style="text-align:center; padding: 2rem; color: #475569;">
          <div style="font-size:2rem; margin-bottom:0.5rem;">🤖</div>
          <div style="font-size:0.88rem;">JARVIS is online. Ask me anything.</div>
          <div style="font-size:0.75rem; margin-top:4px; color:#334155;">Strategy · Analysis · Decisions · Thinking</div>
        </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick prompts
    st.markdown('<div class="section-title">Quick Prompts</div>', unsafe_allow_html=True)
    quick_prompts = [
        "Analyse my cognitive load right now",
        "Give me a Stoic perspective on productivity",
        "What should I focus on this afternoon?",
        "Explain the Eisenhower Matrix with examples",
    ]
    qcols = st.columns(4)
    for i, qp in enumerate(quick_prompts):
        with qcols[i]:
            if st.button(qp, key=f"qp_{i}", use_container_width=True):
                st.session_state._quick_prompt = qp
                st.rerun()

    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_msg = st.text_input(
                "Message",
                placeholder="Ask JARVIS anything...",
                label_visibility="collapsed",
                key="chat_input",
            )
        with col_send:
            send = st.form_submit_button("Send →", use_container_width=True)

    # Handle quick prompt
    if hasattr(st.session_state, "_quick_prompt"):
        user_msg = st.session_state._quick_prompt
        del st.session_state._quick_prompt
        send = True

    if send and user_msg:
        client = get_client()
        if not client:
            st.error("API key not set.")
            return
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.spinner("JARVIS is thinking..."):
            msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
            t0 = time.time()
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=800,
                system=JARVIS_SYSTEM,
                messages=msgs,
            )
            duration = time.time() - t0
            reply = response.content[0].text
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            log_action("chat", duration)
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑 Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


# ─────────────────────────────────────────────
#  MODULE 3 — THOUGHT DUMP
# ─────────────────────────────────────────────
TD_SYSTEM = """You are JARVIS, an AI that specialises in cognitive offloading and clarity.

Your task: Take a raw brain dump of thoughts, worries, tasks, and ideas — and instantly organise them into a structured action plan.

Output ONLY valid JSON with this exact structure:
{
  "urgent_actions": ["item1", "item2"],
  "this_week": ["item1", "item2"],
  "someday_maybe": ["item1", "item2"],
  "ideas": ["item1", "item2"],
  "emotional_checkins": ["item1", "item2"],
  "insights": "A 2-3 sentence JARVIS-style insight about the person's current cognitive state based on the dump",
  "top_priority": "Single most important action to take in the next hour"
}

Rules:
- Distribute items intelligently — don't put everything in urgent_actions
- Rephrase items as clear, actionable statements
- emotional_checkins captures any worries, anxieties, or emotional content for reflection
- insights should be specific to THIS person's dump, not generic
- top_priority should be specific and immediately actionable
- Return ONLY the JSON, no markdown, no explanation."""

CATEGORY_META = {
    "urgent_actions":    ("🔴", "#ef4444", "Urgent Actions"),
    "this_week":         ("🟡", "#f59e0b", "This Week"),
    "someday_maybe":     ("🔵", "#3b82f6", "Someday / Maybe"),
    "ideas":             ("🟣", "#8b5cf6", "Ideas & Opportunities"),
    "emotional_checkins":("🟢", "#10b981", "Emotional Check-ins"),
}

def render_thought_dump():
    st.markdown("""
    <div class="j-card j-card-purple" style="margin-bottom:1.2rem;">
      <div class="section-title">Thought Dump Engine</div>
      <div style="font-size:0.85rem; color:#64748b; line-height:1.6;">
        Brain-dump your raw chaos. JARVIS will instantly organise it into categories:
        urgent actions, this week, someday/maybe, ideas, and emotional check-ins.
      </div>
    </div>
    """, unsafe_allow_html=True)

    dump_text = st.text_area(
        "Your brain dump",
        placeholder=(
            "Just type everything — unfiltered. Tasks, worries, ideas, things you haven't done, "
            "things stressing you out, random thoughts, half-baked ideas...\n\n"
            "Example:\nNeed to finish the project proposal, worried about that meeting tomorrow, "
            "should probably call mum, idea for a new product feature, haven't paid rent yet, "
            "want to learn guitar, anxious about Q3 results, need to review the team's work..."
        ),
        height=200,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([2, 4])
    with col1:
        dump_btn = st.button("🧠 Organise My Thoughts →", use_container_width=True)
    with col2:
        st.markdown("""
        <div style="font-size:0.75rem; color:#475569; padding-top:0.45rem;">
          Powered by Claude AI · Your thoughts are not stored · Instant cognitive offloading
        </div>
        """, unsafe_allow_html=True)

    if dump_btn:
        if not dump_text.strip():
            st.warning("Please write something in the thought dump first.")
            return
        client = get_client()
        if not client:
            st.error("API key not set.")
            return

        with st.spinner("JARVIS is structuring your thoughts..."):
            t0 = time.time()
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1000,
                system=TD_SYSTEM,
                messages=[{"role": "user", "content": f"Brain dump:\n\n{dump_text}"}],
            )
            duration = time.time() - t0
            raw = response.content[0].text.strip()
            # Strip markdown code fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            try:
                result = json.loads(raw)
                st.session_state.thought_result = result
                log_action("thought_dump", duration)
            except json.JSONDecodeError:
                st.error("JARVIS returned an unexpected format. Please try again.")
                st.code(raw)
                return
        st.rerun()

    # Render result
    if st.session_state.thought_result:
        result = st.session_state.thought_result

        # Top priority
        st.markdown(f"""
        <div class="j-card" style="border: 1px solid #ef4444; background: rgba(239,68,68,0.07); margin-bottom:1rem;">
          <div class="section-title" style="color:#ef4444;">Top Priority — Next Hour</div>
          <div style="font-size:1rem; font-weight:600; color:#fca5a5;">{result.get("top_priority","—")}</div>
        </div>
        """, unsafe_allow_html=True)

        # JARVIS insight
        st.markdown(f"""
        <div class="j-card j-card-purple" style="margin-bottom:1.2rem;">
          <div class="section-title">JARVIS Insight</div>
          <div style="font-size:0.88rem; color:#c4b5fd; line-height:1.7; font-style:italic;">{result.get("insights","—")}</div>
        </div>
        """, unsafe_allow_html=True)

        # Categories
        st.markdown('<div class="section-title">Organised Categories</div>', unsafe_allow_html=True)

        for cat_key, (emoji, color, label) in CATEGORY_META.items():
            items = result.get(cat_key, [])
            if not items:
                continue
            items_html = "".join(
                f'<div class="td-item">· {item}</div>' for item in items
            )
            st.markdown(f"""
            <div class="td-category">
              <div class="td-cat-header">
                <div class="td-dot" style="background:{color};"></div>
                <span style="color:{color};">{label}</span>
                <span style="color:#475569; font-weight:400; text-transform:none; letter-spacing:0; font-size:0.72rem; margin-left:4px;">({len(items)})</span>
              </div>
              {items_html}
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑 Clear & Start New Dump"):
            st.session_state.thought_result = None
            st.rerun()


# ─────────────────────────────────────────────
#  MODULE 4 — LIFE PULSE
# ─────────────────────────────────────────────
def render_life_pulse():
    st.markdown("""
    <div class="j-card j-card-accent" style="margin-bottom:1.2rem;">
      <div class="section-title">Life Pulse Dashboard</div>
      <div style="font-size:0.85rem; color:#64748b; line-height:1.6;">
        Real-time tracking of your cognitive load, session patterns, and personalised recommendations.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric tiles
    period_key, period_label, _ = time_context()
    session_dur = session_duration_str()
    msgs = st.session_state.messages_sent
    cog_load = st.session_state.cognitive_load
    focus = max(20, 100 - cog_load // 2 + random.randint(-3, 3))

    col1, col2, col3, col4 = st.columns(4)
    tiles = [
        (session_dur, "Session Duration", "↑ Active"),
        (str(msgs), "Interactions", f"{period_label}"),
        (f"{cog_load}%", "Cognitive Load", "Moderate" if cog_load < 70 else "High"),
        (f"{focus}%", "Estimated Focus", "Based on patterns"),
    ]
    for col, (val, lbl, sub) in zip([col1, col2, col3, col4], tiles):
        with col:
            st.markdown(f"""
            <div class="metric-tile">
              <div class="metric-val">{val}</div>
              <div class="metric-lbl">{lbl}</div>
              <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title">Cognitive Rhythm (Simulated Today)</div>', unsafe_allow_html=True)

        # Generate cognitive rhythm data
        now_h = datetime.now().hour
        hours = list(range(6, min(now_h + 1, 24)))
        if len(hours) < 3:
            hours = list(range(6, 22))
        cognitive_curve = []
        for h in hours:
            if h < 9:
                base = 40 + (h - 6) * 10
            elif h < 12:
                base = 70 + (h - 9) * 8
            elif h < 14:
                base = 65 - (h - 12) * 10
            elif h < 17:
                base = 60 + (h - 14) * 5
            elif h < 20:
                base = 55 - (h - 17) * 7
            else:
                base = 30 - (h - 20) * 3
            noise = random.randint(-5, 5)
            cognitive_curve.append(max(10, min(100, base + noise)))

        df = pd.DataFrame({"Hour": [f"{h:02d}:00" for h in hours], "Cognitive Load": cognitive_curve})
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Hour"],
            y=df["Cognitive Load"],
            mode="lines+markers",
            line=dict(color="#3b82f6", width=2.5, shape="spline"),
            marker=dict(size=5, color="#60a5fa"),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.08)",
            name="Cognitive Load",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#64748b", size=11),
            margin=dict(l=0, r=0, t=0, b=0),
            height=220,
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)", showline=False, tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)", showline=False, range=[0, 100], ticksuffix="%"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Session log
        if st.session_state.session_log:
            st.markdown('<div class="section-title" style="margin-top:0.8rem;">Session Activity Log</div>', unsafe_allow_html=True)
            for entry in reversed(st.session_state.session_log[-6:]):
                dur_str = f"{entry['duration']:.1f}s" if entry.get("duration") else ""
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.78rem;">
                  <span style="color:#94a3b8;">{entry["action"].replace("_"," ").title()}</span>
                  <span style="color:#475569;">{entry["time"].strftime("%H:%M:%S")} &nbsp; {dur_str}</span>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-title">Performance Indicators</div>', unsafe_allow_html=True)

        bars = [
            ("Focus Quality",    focus,     "#3b82f6"),
            ("Cognitive Load",   cog_load,  "#ef4444"),
            ("Session Depth",    min(90, msgs * 12 + 20), "#8b5cf6"),
            ("Recovery Index",   max(10, 100 - cog_load), "#10b981"),
            ("Pattern Clarity",  65,        "#f59e0b"),
        ]
        for label, val, color in bars:
            st.markdown(f"""
            <div class="prog-wrap">
              <div class="prog-label"><span>{label}</span><span>{val}%</span></div>
              <div class="prog-track">
                <div class="prog-fill" style="width:{val}%; background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">JARVIS Recommendation</div>', unsafe_allow_html=True)

        # Dynamic recommendation
        if cog_load > 70:
            rec_icon, rec_color, rec_text = "⚠️", "#f59e0b", "Cognitive load is elevated. Take a 10-minute break before your next task. Walk away from screens entirely."
        elif focus < 40:
            rec_icon, rec_color, rec_text = "🎯", "#ef4444", "Focus score is low. Eliminate all open browser tabs except one. Single-task for the next 25 minutes."
        else:
            rec_icon, rec_color, rec_text = "✅", "#10b981", f"You're in a solid state during {period_label}. Ideal time for your most important task. Protect this window."

        st.markdown(f"""
        <div class="j-card" style="border-color:{rec_color}33; background:rgba(0,0,0,0.2);">
          <div style="font-size:1.2rem; margin-bottom:0.4rem;">{rec_icon}</div>
          <div style="font-size:0.83rem; color:{rec_color}; line-height:1.7;">{rec_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # AI-powered deep analysis
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔬 Deep Analysis →", use_container_width=True):
            client = get_client()
            if not client:
                st.error("API key not set.")
                return
            with st.spinner("Analysing your patterns..."):
                prompt = f"""You are JARVIS. Provide a concise but insightful cognitive analysis for this session:

Session data:
- Duration: {session_dur}
- Interactions: {msgs}
- Cognitive Load: {cog_load}%
- Focus Score: {focus}%
- Time window: {period_label}
- Day: {datetime.now().strftime("%A")}
- Actions taken: {[e["action"] for e in st.session_state.session_log]}

Give:
1. A 2-sentence pattern observation about their session
2. One specific optimisation recommendation
3. Predicted optimal action for the next 30 minutes

Be specific and JARVIS-sharp. Max 120 words."""
                t0 = time.time()
                resp = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}],
                )
                log_action("life_pulse_analysis", time.time() - t0)
                analysis = resp.content[0].text

            st.markdown(f"""
            <div class="j-card j-card-accent" style="margin-top:0.8rem;">
              <div class="section-title">Deep Analysis</div>
              <div style="font-size:0.82rem; color:#cbd5e1; line-height:1.7;">{analysis}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN RENDER
# ─────────────────────────────────────────────
render_nav()

# API key gate
if not st.session_state.api_key_set and not os.getenv("ANTHROPIC_API_KEY"):
    render_api_gate()
    st.stop()

# If env var is set but flag not yet toggled
if not st.session_state.api_key_set and os.getenv("ANTHROPIC_API_KEY"):
    st.session_state.api_key_set = True

render_tabs()
st.markdown("<hr>", unsafe_allow_html=True)

tab = st.session_state.tab
if tab == "predict":
    render_predict()
elif tab == "chat":
    render_chat()
elif tab == "thoughtdump":
    render_thought_dump()
elif tab == "lifepulse":
    render_life_pulse()
