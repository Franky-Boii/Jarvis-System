import streamlit as st
import ollama
import pandas as pd
from datetime import datetime
import pyttsx3
import json
import os
import time

# ==========================================
# 🌌 TONY STARK VISUAL THEMING (NATIVE CSS INJECTION)
# ==========================================
st.set_page_config(page_title="JARVIS // INTERFACE v4.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
        /* Global Cyberpunk HUD Overrides */
        .reportview-container, .main {
            background-color: #030712 !important;
            font-family: 'Courier New', Courier, monospace !important;
            color: #00f0ff !important;
        }
        /* Glowing Sidebar HUD */
        section[data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 2px solid #00f0ff !important;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }
        /* Neon Chat Containers */
        .stChatMessage {
            background-color: #0d1527 !important;
            border: 1px solid #00f0ff !important;
            border-radius: 4px !important;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.1);
            margin-bottom: 12px !important;
        }
        /* Metrics Telemetry Box */
        div[data-testid="stMetricValue"] {
            color: #ff0055 !important;
            font-size: 2.2rem !important;
            font-weight: bold !important;
            text-shadow: 0 0 10px rgba(255, 0, 85, 0.4);
        }
        /* Custom Glowing Headers */
        h1, h2, h3 {
            color: #00f0ff !important;
            text-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
            letter-spacing: 2px;
        }
        /* Hide default Streamlit aesthetic bloat */
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_with_html=True)

# ==========================================
# SYSTEM SETUP & COMMUNICATIONS BRIDGE
# ==========================================
BRIDGE_FILE = "jarvis_command.json"

if "tts_engine" not in st.session_state:
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if "alex" in voice.name.lower() or "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 185) 
        st.session_state.tts_engine = engine
    except Exception:
        st.session_state.tts_engine = None

def speak_text(text):
    if st.session_state.tts_engine:
        try:
            st.session_state.tts_engine.say(text)
            st.session_state.tts_engine.runAndWait()
        except Exception:
            pass

# Sidebar Command Module
st.sidebar.markdown("## 🛰️ SYSTEM TELEMETRY")
page = st.sidebar.radio(
    "SELECT INTERFACE LAYER:", 
    ["[01] CORE HUD TERMINAL", "[02] FOREX CLIENT LEDGER", "[03] CONTENT BLUEPRINTS"],
    key="jarvis_navigation_radio"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**DAEMON CHANNELS:**")
st.sidebar.markdown("<span style='color:#00ff66;'>● SECURE AUDIO CAPTURE ON</span>", unsafe_with_html=True)
st.sidebar.markdown(f"<span style='color:#00f0ff;'>● TIMELINE SYNC: {datetime.now().strftime('%H:%M:%S')}</span>", unsafe_with_html=True)


# ==========================================
# [01] CORE HUD TERMINAL LAYER
# ==========================================
if page == "[01] CORE HUD TERMINAL":
    st.title("⚡ JARVIS MAIN COMMAND HUD")
    st.markdown("`MAIN BRAIN MATRIX // OFFLINE INTEL LAYER`")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_col, telemetry_col = st.columns([4, 1])

    with telemetry_col:
        st.markdown("### 📊 CORE MATRIX")
        st.info("CPU STATUS: NOMINAL")
        if st.button("⚡ FLUSH CACHE MODULE", width="stretch"):
            st.session_state.messages = []
            st.rerun()

    with chat_col:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    user_prompt = None

    # Check for rapid vocal input data dropped from the background ears.py pipeline
    if os.path.exists(BRIDGE_FILE):
        try:
            with open(BRIDGE_FILE, "r") as f:
                data = json.load(f)
            user_prompt = data.get("command")
            os.remove(BRIDGE_FILE) 
        except Exception:
            pass

    # Standard Fallback Chat Terminal Box
    if not user_prompt:
        text_query = st.chat_input("INITIALIZE DIRECTIVE ENCRYPTION LOOP...")
        if text_query:
            user_prompt = text_query

    if user_prompt:
        with chat_col:
            with st.chat_message("user"):
                st.markdown(f"`CEO //` {user_prompt}")
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        with chat_col:
            with st.chat_message("assistant"):
                with st.spinner("COMPUTING RESPONSE PACKETS..."):
                    try:
                        # Ultra-short context configuration to maximize processing speed on 8GB RAM hardware
                        system_instruction = (
                            "You are JARVIS, a secure cyberpunk AI assistant for a Forex executive. "
                            "Address the user only as 'CEO'. Your responses MUST be under 2 sentences long. "
                            "Be direct, snappy, and clear. No verbose chat filler."
                        )
                        
                        conversation_payload = [{'role': 'system', 'content': system_instruction}]
                        # Force strict minimal memory buffer to eliminate inference processing bottlenecks
                        conversation_payload.extend(st.session_state.messages[-2:])
                        
                        response = ollama.chat(model='phi3:mini', messages=conversation_payload)
                        response_text = response['message']['content']
                        
                        st.markdown(f"`JARVIS //` {response_text}")
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                        speak_text(response_text)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"MATRIX DELAY: {e}")

    # Micro-sleep interval matching hardware tick intervals perfectly
    time.sleep(0.2)
    st.rerun()


# ==========================================
# [02] FOREX CLIENT LEDGER
# ==========================================
elif page == "[02] FOREX CLIENT LEDGER":
    st.title("👥 EXECUTIVE CLIENT LEDGER")
    
    students_data = {
        "STUDENT RECORD": ["Alex Ndlovu", "Sarah Jenkins", "Sipho Khumalo"],
        "STRATEGY TRACK": ["Advanced Price Action", "Foundational Mechanics", "1-on-1 Scalping Mastery"],
        "TIMESTAMP": ["2026-01-15", "2026-03-10", "2026-05-01"],
        "FEE MATRIX": ["PAID", "OVERDUE", "PAID"]
    }
    df = pd.DataFrame(students_data)
    
    col1, col2 = st.columns(2)
    col1.metric("ACTIVE CHANNELS", len(df))
    col2.metric("RENEWAL ALERTS", "1")
    
    st.markdown("### 📊 SEGMENT REGISTER")
    st.dataframe(df, width="stretch")


# ==========================================
# [03] CONTENT BLUEPRINTS
# ==========================================
elif page == "[03] CONTENT BLUEPRINTS":
    st.title("📈 CREATOR STRATEGY ENGINE")
    
    topic = st.text_input("INPUT SPECIFIC CORE FOREX CONCEPT:")
    platform = st.selectbox("TARGET HUD INTERFACE:", ["Instagram Blueprint", "LinkedIn Wire"])
    
    if st.button("🚀 EXECUTE CONTENT DRAFT PACKET"):
        if topic:
            prompt = f"Draft a concise corporate {platform} regarding the implementation of: {topic}."
            try:
                response = ollama.chat(model='phi3:mini', messages=[{'role': 'user', 'content': prompt}])
                st.info(response['message']['content'])
            except Exception as e:
                st.error(f"CRITICAL FAULT: {e}")