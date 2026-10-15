"""
Voice AI Assistant — speech in, Gemini reply out, spoken back via TTS.
"""

from __future__ import annotations

import os
import sys

import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"
LISTEN_LANGUAGE = os.getenv("LISTEN_LANGUAGE", "ar-EG").strip() or "ar-EG"

EXIT_PHRASES = ("وداعاً", "وداعا", "خروج", "انهاء", "إنهاء", "وقف", "bye", "exit", "quit")


def require_api_key() -> str:
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY":
        print(
            "Missing GOOGLE_API_KEY.\n"
            "1) Copy .env.example to .env\n"
            "2) Set GOOGLE_API_KEY from https://aistudio.google.com/apikey"
        )
        sys.exit(1)
    return GOOGLE_API_KEY


def build_model():
    genai.configure(api_key=require_api_key())
    return genai.GenerativeModel(MODEL_NAME)


def create_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", int(os.getenv("TTS_RATE", "160")))
    return engine


def speak(engine, text: str) -> None:
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen(language: str = LISTEN_LANGUAGE) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening…")
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return ""

    try:
        text = recognizer.recognize_google(audio, language=language)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as exc:
        print(f"Speech recognition service error: {exc}")
        return ""


def ask_gemini(model, prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        return text or "I could not generate a response."
    except Exception as exc:  # noqa: BLE001 — surface API failures to the user
        print(f"Gemini error: {exc}")
        return "Sorry, the AI service is unavailable right now. Please try again later."


def should_exit(command: str) -> bool:
    lowered = command.lower().strip()
    return any(phrase in lowered for phrase in EXIT_PHRASES)


def main() -> None:
    model = build_model()
    engine = create_tts_engine()

    speak(engine, "Hello! I am ready to help. Say goodbye or exit to stop.")

    while True:
        command = listen()
        if not command:
            continue
        if should_exit(command):
            break
        reply = ask_gemini(model, command)
        speak(engine, reply)

    speak(engine, "Goodbye! Have a great day.")


if __name__ == "__main__":
    main()
