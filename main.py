import subprocess
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# === Settings ===
FILENAME = "user_input.wav"
HISTORY_LIMIT = 5  # Max number of turns to remember

# === Init Whisper ===
whisper_model = whisper.load_model("tiny")  # You can try "base" if you want better accuracy

# === Record voice ===
def record_audio(duration=5, fs=44100):
    print("\n🎙️ Speak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(FILENAME, fs, audio)
    print("✅ Recorded")

# === Transcribe with Whisper ===
def transcribe_audio():
    result = whisper_model.transcribe(FILENAME)
    print("📝 You said:", result["text"])
    return result["text"]

import requests

def ask_ollama(prompt):
    print("🤖 Thinking...")
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "phi",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        data = response.json()
        reply = data.get("message", {}).get("content", "").strip()
        if not reply:
            reply = "Sorry, I didn't understand that."
        print("🧠 AI:", reply)
        return reply
    except Exception as e:
        print("❌ Error talking to Ollama:", e)
        return "There was an error talking to the local AI."

# === Speak response ===
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# === Keep chat history as prompt ===
def build_prompt(history):
    prompt = ""
    for user_msg, ai_msg in history:
        prompt += f"User: {user_msg}\nAssistant: {ai_msg}\n"
    prompt += "User: "
    return prompt

# === Main conversation loop ===
def chat_loop():
    print("🤖 Voice assistant ready. Say 'stop' to exit.")
    history = []

    while True:
        try:
            record_audio()
            user_input = transcribe_audio()
            os.remove(FILENAME)

            if user_input.lower().strip() in ["stop", "exit", "quit"]:
                print("👋 Goodbye!")
                speak("Goodbye!")
                break

            # Prepare the prompt with memory
            recent_history = history[-HISTORY_LIMIT:]
            full_prompt = build_prompt(recent_history) + user_input

            # Ask LLM
            response = ask_ollama(full_prompt)

            # Speak & store history
            speak(response)
            history.append((user_input, response))

        except KeyboardInterrupt:
            print("\n🔌 Stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            speak("Sorry, I had an error.")
            break

if __name__ == "__main__":
    chat_loop()
