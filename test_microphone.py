#!/usr/bin/env python3
"""Test script to verify Bluetooth microphone is working with ZEE."""
import speech_recognition as sr
import sys

print("=" * 60)
print("🎤 ZEE Bluetooth Microphone Test")
print("=" * 60)
print()

# Initialize recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

print(f"✅ Using default system microphone")
print()

# Configure settings
recognizer.energy_threshold = 200  # Bluetooth-optimized
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

print("🔧 Microphone settings:")
print(f"   Energy threshold: {recognizer.energy_threshold}")
print(f"   Dynamic threshold: {recognizer.dynamic_energy_threshold}")
print(f"   Pause threshold: {recognizer.pause_threshold}")
print()

# Test ambient noise
print("📊 Testing ambient noise levels...")
try:
    with microphone as source:
        print("   (Calibrating for 2 seconds - stay quiet...)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"   ✅ Ambient noise level: {recognizer.energy_threshold}")
        print()
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test voice recognition
print("🎤 TEST 1: Say something (you have 5 seconds)...")
try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    
    print("   🔄 Processing audio...")
    text = recognizer.recognize_google(audio)
    print(f"   ✅ SUCCESS! Heard: '{text}'")
    print()
    
except sr.WaitTimeoutError:
    print("   ⏱️  TIMEOUT - No speech detected")
    print()
    print("⚠️  DIAGNOSIS:")
    print("   1. Your Bluetooth microphone might not be active")
    print("   2. Check volume: Speak LOUDER and CLOSER to mic")
    print("   3. Test mic with: arecord -d 3 -f cd test.wav && aplay test.wav")
    print()
    sys.exit(1)
    
except sr.UnknownValueError:
    print("   ❌ HEARD AUDIO but couldn't understand")
    print("   💡 Microphone is working! Speak more clearly")
    print()
    
except sr.RequestError as e:
    print(f"   ❌ Service error: {e}")
    print("   💡 Check internet connection")
    sys.exit(1)
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Second test
print("🎤 TEST 2: Say 'Hey ZEE' (you have 5 seconds)...")
try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    
    print("   🔄 Processing audio...")
    text = recognizer.recognize_google(audio)
    print(f"   ✅ SUCCESS! Heard: '{text}'")
    
    if 'zee' in text.lower() or 'z' in text.lower():
        print("   🎉 PERFECT! Wake word detected!")
    else:
        print(f"   💡 Heard '{text}' - try saying 'Hey ZEE' more clearly")
    print()
    
except sr.WaitTimeoutError:
    print("   ⏱️  TIMEOUT - No speech detected")
    print()
    
except sr.UnknownValueError:
    print("   ❌ HEARD AUDIO but couldn't understand")
    print()
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print()

print("=" * 60)
print("✅ Microphone test complete!")
print()
print("If tests passed:")
print("   Your Bluetooth mic is working!")
print("   ZEE service should hear you now.")
print()
print("If tests failed:")
print("   1. Check Bluetooth connection")
print("   2. Test mic: pactl list sources | grep -i bluez")
print("   3. Adjust mic volume: pactl set-source-volume @DEFAULT_SOURCE@ 150%")
print("   4. Run setup: ./setup_bluetooth_mic.sh")
print("=" * 60)
