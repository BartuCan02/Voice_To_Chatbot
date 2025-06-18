# 🗣️ Offline Voice Chatbot with Whisper + Ollama

This is a fully offline voice assistant built with Python. It allows you to speak a question or command into your microphone, transcribes it using OpenAI's Whisper, sends it to a **local LLM** (e.g. `phi`) via [Ollama](https://ollama.com), and responds with synthesized speech.

---

## 📦 Features

- 🎙️ Voice input (recorded via microphone)
- 📝 Transcription using [Whisper](https://github.com/openai/whisper)
- 🧠 Local LLM (like `phi`, `mistral`, etc.) using [Ollama](https://ollama.com)
- 🔊 Voice response using `pyttsx3`
- ✅ 100% offline — no internet or API key required

---

## 🚀 Demo

https://user-images.githubusercontent.com/your-demo.gif

> “What's the capital of France?”
>
> 🧠 → “The capital of France is Paris.”

---

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install pyttsx3 sounddevice scipy requests
pip install git+https://github.com/openai/whisper.git
