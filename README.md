# Voice AI Assistant

A small **Python voice assistant** that listens through your microphone, sends your speech to **Google Gemini**, and speaks the reply back using offline TTS (`pyttsx3`).

Built as a focused demo of speech recognition + generative AI + text-to-speech on Windows.

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" />
  <img alt="Gemini" src="https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## Features

- **Speech-to-text** via Google Speech Recognition (default locale: Egyptian Arabic `ar-EG`)
- **LLM answers** powered by Google Gemini
- **Text-to-speech** replies with `pyttsx3` (system voices)
- **Exit phrases** in Arabic / English (`وداعاً`, `خروج`, `bye`, `exit`, …)
- **Config via `.env`** — no API keys in source code

---

## Project layout

```
AI_Assistant_Project/
├── assistant.py      # Main voice loop
├── test_tts.py       # Optional TTS smoke test
├── requirements.txt
├── .env.example
└── README.md
```

---

## Requirements

- Python **3.11+** recommended  
- Working microphone  
- Windows: a system voice pack (Arabic voice optional for nicer Arabic TTS)  
- Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

---

## Setup

```bash
cd AI_Assistant_Project
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Edit `.env` and set:

```env
GOOGLE_API_KEY=your_key_here
```

### PyAudio on Windows

If `pip install PyAudio` fails, install a matching wheel for your Python version, or use:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## Run

```bash
python assistant.py
```

Speak after “Listening…”. Say **goodbye** / **خروج** / **وداعاً** to stop.

Optional TTS check:

```bash
python test_tts.py
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | — | Required Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Model id |
| `LISTEN_LANGUAGE` | `ar-EG` | Speech recognition locale |
| `TTS_RATE` | `160` | Words-per-minute for `pyttsx3` |

---

## How it works

1. Capture microphone audio (`SpeechRecognition` + `PyAudio`)  
2. Transcribe with Google Speech API  
3. Send text prompt to Gemini  
4. Speak the model’s reply with `pyttsx3`  

---

## Security notes

- Never commit `.env` or hard-code API keys  
- If a key was ever pasted into source, **rotate it** in Google AI Studio  

---

## Author

Portfolio / learning project — voice interface around Google Gemini.

---

## License

MIT
