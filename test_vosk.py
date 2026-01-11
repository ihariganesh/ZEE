#!/usr/bin/env python3
"""Test Vosk offline speech recognition with Bluetooth microphone."""
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import json
import os

print("=" * 60)
print("🎤 Testing Vosk (Offline Speech Recognition)")
print("=" * 60)

# Check model
model_path = os.path.expanduser("~/vosk-model-small-en-us-0.15")
if not os.path.exists(model_path):
    print(f"❌ Vosk model not found at: {model_path}")
    exit(1)

print(f"✅ Vosk model found: {model_path}")

# Initialize
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 200
recognizer.dynamic_energy_threshold = True

print("✅ Microphone initialized")
print()

# Load Vosk model
print("📦 Loading Vosk model (may take a few seconds)...")
model = Model(model_path)
print("✅ Vosk model loaded!")
print()

# Test
print("🎤 Say 'Hey ZEE' or anything else (5 seconds)...")
print("   (Vosk works offline and better with Bluetooth audio)")
print()

try:
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    
    print("🔄 Processing with Vosk...")
    
    # Convert to WAV data that Vosk expects
    wav_data = audio.get_wav_data(convert_rate=16000, convert_width=2)
    
    # Recognize with Vosk
    rec = KaldiRecognizer(model, 16000)
    
    if rec.AcceptWaveform(wav_data):
        result = json.loads(rec.Result())
        text = result.get('text', '').strip()
        
        if text:
            print(f"✅ SUCCESS! Heard: '{text}'")
            
            if 'zee' in text.lower() or 'z' in text.lower():
                print("🎉 PERFECT! Wake word detected!")
        else:
            print("❌ No speech detected by Vosk")
    else:
        # Partial result
        partial = json.loads(rec.PartialResult())
        text = partial.get('partial', '').strip()
        if text:
            print(f"⚠️  Partial recognition: '{text}'")
        else:
            print("❌ Vosk couldn't recognize speech")
            
except sr.WaitTimeoutError:
    print("⏱️  Timeout - no speech detected")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("=" * 60)
print("If Vosk recognized your speech:")
print("  ✅ Restart ZEE service and try 'Hey ZEE'")
print("  systemctl --user restart zee-service@$USER.service")
print()
print("If Vosk failed:")
print("  📢 Speak LOUDER and more CLEARLY")
print("  🎚️  Increase volume: pactl set-source-volume @DEFAULT_SOURCE@ 200%")
print("=" * 60)
