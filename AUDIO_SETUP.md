# Audio Troubleshooting Guide

## 🎤 Microphone Not Picking Up Voice

### Quick Fixes:

1. **Test your microphone first:**
```bash
# Record 5 seconds of audio
arecord -d 5 test.wav

# Play it back
aplay test.wav
```

2. **Check microphone levels:**
```bash
# Open audio mixer
alsamixer

# Press F4 to show capture devices
# Use arrow keys to increase "Capture" volume to 80-100%
```

3. **List available microphones:**
```bash
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

4. **Select specific microphone in code:**
Edit `voice_handler.py` line 17:
```python
# Use specific device (get index from list above)
self.microphone = sr.Microphone(device_index=0)  # Change 0 to your mic index
```

## 🔊 Voice Quality Issues

### Improve Text-to-Speech:

1. **Install better voices (Arch Linux):**
```bash
# Install festival with better voices
sudo pacman -S festival festival-english

# Test it
echo "Hello, this is a test" | festival --tts
```

2. **Or use alternative TTS (piper):**
```bash
# Install piper (high-quality neural TTS)
yay -S piper-tts

# Download a voice
piper --download-voice en_US-amy-medium
```

3. **Alternative: Use espeak-ng with MBROLA (better quality):**
```bash
sudo pacman -S espeak-ng mbrola mbrola-voices-en1
```

## 🎯 If Assistant Can't Hear You:

### Check these settings in `/home/hari/ZEE/voice_handler.py`:

```python
# Line ~55: Increase sensitivity
self.recognizer.energy_threshold = 200  # Lower = more sensitive (try 100-300)

# Line ~73: Longer listening time
audio = self.recognizer.listen(
    source,
    timeout=15,        # Wait longer for you to start speaking
    phrase_time_limit=20  # Allow longer phrases
)
```

## 🔧 Advanced: PulseAudio Configuration

If using PulseAudio:
```bash
# Check default input device
pactl list short sources

# Set default input (replace INDEX)
pactl set-default-source INDEX

# Increase input volume
pactl set-source-volume @DEFAULT_SOURCE@ 150%
```

## ✅ Quick Test Commands

```bash
cd /home/hari/ZEE

# Test voice recognition only
python -c "from voice_handler import VoiceHandler; v = VoiceHandler(); print(v.listen())"

# Test TTS only
python -c "from voice_handler import VoiceHandler; v = VoiceHandler(); v.speak('Testing voice output')"
```

## 💡 Pro Tips:

1. **Speak clearly** - 6-12 inches from microphone
2. **Reduce background noise** - Close windows, turn off fans
3. **Adjust room lighting** if using laptop webcam mic
4. **Use headset mic** for better quality than built-in laptop mic
5. **Wait for "🎤 Listening..."** before speaking
