import speech_recognition as sr
import json
import pyttsx3
import time

def speak_feedback(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if "alex" in voice.name.lower() or "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 185)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def listen_for_ceo():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # Static energy mapping to prevent listening lags on built-in Mac hardware
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 1200 
    
    print("🟢 JARVIS SECURE AUDIO OVERLAY ONLINE... Say 'Hey Jarvis'")
    
    while True:
        with mic as source:
            try:
                # Fast capture filters looking for a sharp wake signature
                audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=2.0)
                text = recognizer.recognize_google(audio).lower()
                
                if "jarvis" in text or "hey jarvis" in text:
                    print("⚡ Wake Authorized.")
                    speak_feedback("Online. Ready, CEO.")
                    
                    print("🎙️ Capturing command packet...")
                    cmd_audio = recognizer.listen(source, timeout=3.5, phrase_time_limit=5.5)
                    command_text = recognizer.recognize_google(cmd_audio)
                    
                    if command_text:
                        print(f"📥 Packets Parsed: {command_text}")
                        with open("jarvis_command.json", "w") as f:
                            json.dump({"command": command_text}, f)
            except Exception:
                pass
        time.sleep(0.05)

if __name__ == "__main__":
    listen_for_ceo()