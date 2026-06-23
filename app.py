import streamlit as st
import ollama
import pandas as pd
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import threading
import time

# ==========================================
# SYSTEM SETUP & INITIALIZATION
# ==========================================

st.set_page_config(page_title="JARVIS: Forex CEO", page_icon="💼", layout="wide")

# Persistent Audio Engine Safe Init with Male Voice Configuration
if "tts_engine" not in st.session_state:
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Look for a native male voice option on macOS (typically index 0 or named 'Alex')
        male_voice_found = False
        for voice in voices:
            if "alex" in voice.name.lower() or "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                male_voice_found = True
                break
        if not male_voice_found and len(voices) > 0:
            engine.setProperty('voice', voices[0].id) # Fallback to first available
            
        engine.setProperty('rate', 180) # Crisp, natural cadence
        st.session_state.tts_engine = engine
    except Exception:
        st.session_state.tts_engine = None

def speak_text(text):
    if st.session_state.tts_engine:
        try:
            st.session_state.tts_engine.say(text)
            st.session_state.tts_engine.runAndWait()
        except Exception as e:
            print(f"[TTS Error]: {e}")

# Continuous Background Listening Daemon Engine
def background_voice_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # Calibrate for environmental noise floor gently
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
    
    while True:
        # Only poll the room audio if JARVIS isn't already actively thinking/processing a prompt
        if not st.session_state.get("processing_command", False):
            with mic as source:
                try:
                    # Snappy listen phase strictly watching for the wake word
                    audio = recognizer.listen(source, timeout=2.0, phrase_time_limit=2.5)
                    text = recognizer.recognize_google(audio).lower()
                    
                    if "jarvis" in text or "hey jarvis" in text:
                        st.session_state.wake_triggered = True
                        speak_text("Online. Systems operational, CEO.")
                        
                        # Immediately listen for the follow-up executive command
                        st.toast("🎙️ JARVIS Active! Listening to your command, CEO...")
                        cmd_audio = recognizer.listen(source, timeout=4.0, phrase_time_limit=6.0)
                        command_text = recognizer.recognize_google(cmd_audio)
                        
                        if command_text:
                            st.session_state.pending_prompt = command_text
                            st.session_state.processing_command = True
                            break # Break loop temporarily to force Main UI update thread
                except Exception:
                    pass
        time.sleep(0.1)

# Spawn the isolated background ear thread exactly once when the web server registers
if "voice_thread_spawned" not in st.session_state:
    st.session_state.wake_triggered = False
    st.session_state.pending_prompt = None
    st.session_state.processing_command = False
    
    listener_thread = threading.Thread(target=background_voice_listener, daemon=True)
    listener_thread.start()
    st.session_state.voice_thread_spawned = True

# Sidebar Navigation Control
st.sidebar.title("⚙️ JARVIS Navigation")
page = st.sidebar.radio(
    "Go to:", 
    ["Core AI Assistant", "Student Management", "Content & Strategy"],
    key="jarvis_navigation_radio"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:**")
st.sidebar.success("🟢 Hands-Free Wake System Active")
st.sidebar.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")


# ==========================================
# PAGE 1: CORE AI ASSISTANT
# ==========================================
if page == "Core AI Assistant":
    st.title("🤖 JARVIS Core Terminal")
    st.caption("Offline Local Intelligence Engine — Passive Background Thread Listening")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_col, action_col = st.columns([4, 1])

    with action_col:
        st.markdown("### Terminal State")
        st.success("🟢 Listening for 'Hey Jarvis'...")
        st.markdown("---")
        if st.button("🗑️ Clear Terminal Cache", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with chat_col:
        # Display conversation history panels
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Collect inputs from either the background ear thread or standard text bar backup
    user_prompt = None

    if st.session_state.pending_prompt:
        user_prompt = st.session_state.pending_prompt
        # Reset state parameters immediately
        st.session_state.pending_prompt = None
    else:
        text_query = st.chat_input("Or type a directive here, CEO...")
        if text_query:
            user_prompt = text_query

    # Execute text token processing through the Ollama pipeline safely
    if user_prompt:
        with chat_col:
            with st.chat_message("user"):
                st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        with chat_col:
            with st.chat_message("assistant"):
                with st.spinner("Processing analysis layers..."):
                    try:
                        system_instruction = (
                            "You are JARVIS, an advanced personal AI assistant for a Forex CEO. "
                            "Address the user exclusively as 'CEO'. Your tone is crisp, professional, and confident. "
                            "Keep spoken responses under 3 sentences long so they remain snappy and fast. Never break character."
                        )
                        
                        conversation_payload = [{'role': 'system', 'content': system_instruction}]
                        # Append only the last 4 exchanges to keep processing fast and lag-free
                        conversation_payload.extend(st.session_state.messages[-4:])
                        
                        response = ollama.chat(model='phi3:mini', messages=conversation_payload)
                        response_text = response['message']['content']
                        
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                        # Clear flag blocks before talking out loud to turn the ears back on cleanly next loop
                        st.session_state.processing_command = False
                        speak_text(response_text)
                        
                        # Re-spawn background monitoring loop thread seamlessly
                        listener_thread = threading.Thread(target=background_voice_listener, daemon=True)
                        listener_thread.start()
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Execution Delay: {e}")
                        st.session_state.processing_command = False

    # Soft pacing delay to keep Streamlit's web rendering thread alive and listening 
    time.sleep(0.2)
    st.rerun()


# ==========================================
# PAGE 2: STUDENT MANAGEMENT
# ==========================================
elif page == "Student Management":
    st.title("👥 Mentorship Student Hub")
    st.write("Track and monitor your active Forex students seamlessly.")
    
    students_data = {
        "Student Name": ["Alex Ndlovu", "Sarah Jenkins", "Sipho Khumalo"],
        "Course Track": ["Advanced Price Action", "Foundational Mechanics", "1-on-1 Scalping Mastery"],
        "Join Date": ["2026-01-15", "2026-03-10", "2026-05-01"],
        "Payment Status": ["Paid", "Overdue", "Paid"]
    }
    df = pd.DataFrame(students_data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Students", len(df))
    col2.metric("Pending Renewals", "1")
    
    st.markdown("### Active Roster")
    st.dataframe(df, use_container_width=True)


# ==========================================
# PAGE 3: CONTENT & STRATEGY
# ==========================================
elif page == "Content & Strategy":
    st.title("📈 Forex Creator Suite")
    st.write("Generate high-impact content blueprints for your trading community.")
    
    topic = st.text_input("Enter a concept:")
    platform = st.selectbox("Target Platform", ["Instagram Caption", "LinkedIn Professional Post"])
    
    if st.button("🚀 Ask JARVIS to Draft Copy"):
        if topic:
            prompt = f"Write a brief {platform} about: {topic} tailored for Forex traders."
            try:
                response = ollama.chat(model='phi3:mini', messages=[{'role': 'user', 'content': prompt}])
                st.info(response['message']['content'])
            except Exception as e:
                st.error(f"Error: {e}")