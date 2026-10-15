"""Quick TTS smoke test for pyttsx3 (English + optional Arabic voice)."""

import pyttsx3

print("Initializing pyttsx3…")
engine = pyttsx3.init()
engine.setProperty("rate", 150)

print("Speaking English…")
engine.say("Hello, this is a test from pyttsx3.")
engine.runAndWait()

print("Looking for an Arabic voice…")
arabic_voice_id = None
for voice in engine.getProperty("voices"):
    langs = getattr(voice, "languages", []) or []
    normalized = []
    for lang in langs:
        if isinstance(lang, bytes):
            lang = lang.decode("utf-8", errors="ignore")
        normalized.append(str(lang).lower())
    if any(item.startswith("ar") for item in normalized) or "arabic" in voice.name.lower():
        arabic_voice_id = voice.id
        print(f"Found Arabic voice: {voice.name}")
        break

if arabic_voice_id:
    engine.setProperty("voice", arabic_voice_id)
else:
    print("No Arabic voice found; using the default voice.")

engine.say("مرحباً، هذا اختبار للصوت.")
engine.runAndWait()
print("TTS test complete.")
