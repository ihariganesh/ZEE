# ZEE Service Setup Guide

This guide will help you install ZEE as a background service that automatically starts when your laptop boots, just like Siri or Google Assistant.

## What You Get

- ✅ ZEE runs in the background automatically on boot
- ✅ Say "Hey ZEE" or "ZEE" to activate it anytime
- ✅ Natural voice responses (like Siri/Gemini)
- ✅ Control system, open apps, do research - hands-free!
- ✅ Uses FREE AI tools (Groq, Ollama, Whisper)

## Installation Steps

### 1. Install the Systemd Service

```bash
# Create systemd user directory if it doesn't exist
mkdir -p ~/.config/systemd/user

# Copy service file
cp ~/ZEE/zee-service@.service ~/.config/systemd/user/

# Reload systemd to recognize new service
systemctl --user daemon-reload

# Enable service to auto-start on boot
systemctl --user enable zee-service@${USER}.service

# Start service now
systemctl --user start zee-service@${USER}.service
```

### 2. Verify Service is Running

```bash
# Check status
systemctl --user status zee-service@${USER}.service

# Watch live logs
journalctl --user -u zee-service@${USER}.service -f
```

You should see:
```
✓ Found built-in microphone: ...
✅ Google TTS initialized - Natural voice mode
✅ Microphone ready! (High sensitivity mode)
👋 Hi! I'm ZEE, your AI assistant...
🎤 Listening for wake word... (say "Hey ZEE" or "ZEE")
```

### 3. Test Wake Word Detection

1. Make sure service is running: `systemctl --user status zee-service@${USER}.service`
2. Say clearly: **"Hey ZEE"** or **"ZEE"**
3. You should hear: "Yes, I'm listening!"
4. Then say your command, like:
   - "Open Chrome"
   - "Search for quantum computing"
   - "Set volume to 50"
   - "Help"

### 4. Control the Service

```bash
# Start ZEE
systemctl --user start zee-service@${USER}.service

# Stop ZEE
systemctl --user stop zee-service@${USER}.service

# Restart ZEE
systemctl --user restart zee-service@${USER}.service

# Check if running
systemctl --user is-active zee-service@${USER}.service

# View logs (last 50 lines)
journalctl --user -u zee-service@${USER}.service -n 50

# View live logs
journalctl --user -u zee-service@${USER}.service -f

# Disable auto-start on boot
systemctl --user disable zee-service@${USER}.service
```

## Troubleshooting

### Microphone Not Working

1. **Check microphone devices:**
   ```bash
   python -c "import speech_recognition as sr; [print(f'{i}: {name}') for i, name in enumerate(sr.Microphone.list_microphone_names())]"
   ```

2. **Test recording:**
   ```bash
   arecord -d 5 -f cd test.wav && aplay test.wav
   ```

3. **Check PulseAudio:**
   ```bash
   pactl list sources short
   ```

4. **Ensure you're in audio group:**
   ```bash
   groups $USER | grep audio
   # If not there:
   sudo usermod -aG audio $USER
   # Then logout and login again
   ```

### Service Not Starting

1. **Check logs for errors:**
   ```bash
   journalctl --user -u zee-service@${USER}.service -n 100
   ```

2. **Check Python dependencies:**
   ```bash
   ~/ZEE/venv/bin/pip list | grep -E "groq|ollama|gtts|speech"
   ```

3. **Verify Groq API key:**
   ```bash
   grep GROQ_API_KEY ~/ZEE/config.py
   ```

4. **Test service manually:**
   ```bash
   cd ~/ZEE
   source venv/bin/activate
   python zee_service.py
   ```

### Wake Word Not Detected

1. **Speak louder and closer to microphone**
   - Try: "HEY ZEE" (emphasize both words)
   - Try: "OKAY ZEE"

2. **Check microphone volume:**
   ```bash
   alsamixer
   # Press F6 to select sound card
   # Press F4 to show capture devices
   # Increase microphone volume
   ```

3. **Adjust sensitivity in code:**
   Edit `voice_handler.py` line 84:
   ```python
   self.recognizer.energy_threshold = 200  # Lower = more sensitive
   ```

4. **Test without wake word (debug mode):**
   ```bash
   cd ~/ZEE
   source venv/bin/activate
   python main.py  # Command-line mode without wake word
   ```

### Voice Output Issues

1. **Check audio player:**
   ```bash
   which mpg123 || which ffplay
   # If neither exists:
   sudo pacman -S mpg123  # For Arch
   ```

2. **Test Google TTS:**
   ```python
   from gtts import gTTS
   tts = gTTS("Hello from ZEE", lang='en')
   tts.save("test.mp3")
   ```
   ```bash
   mpg123 test.mp3
   ```

3. **Fallback to offline TTS:**
   Edit `config.py`:
   ```python
   USE_GTTS = False  # Use pyttsx3 instead
   ```

## Performance Tips

1. **Faster wake word detection:**
   - Edit `zee_service.py` line 61, reduce timeout:
   ```python
   text = self.voice.listen(timeout=20, phrase_time_limit=10)
   ```

2. **Use Ollama for offline mode:**
   - Ensure Ollama is running: `ollama serve`
   - Model loaded: `ollama run llama3.2`

3. **Reduce CPU usage:**
   - Edit `config.py`:
   ```python
   USE_WHISPER = False  # Use Google Speech API instead
   ```

## Advanced Configuration

### Custom Wake Words

Edit `zee_service.py` line 56:
```python
wake_words = ['zee', 'hey zee', 'ok zee', 'jarvis', 'computer']
```

### Change Voice Speed

Edit `voice_handler.py` Google TTS section:
```python
tts = gTTS(text, lang='en', slow=False)  # Set slow=True for slower speech
```

### Auto-Restart on Failure

Service already configured with `Restart=on-failure` in systemd unit.
Adjust restart delay by editing `zee-service@.service`:
```ini
RestartSec=5  # Wait 5 seconds before restart
```

## Uninstall

```bash
# Stop and disable service
systemctl --user stop zee-service@${USER}.service
systemctl --user disable zee-service@${USER}.service

# Remove service file
rm ~/.config/systemd/user/zee-service@.service

# Reload systemd
systemctl --user daemon-reload

# Optional: Remove ZEE completely
rm -rf ~/ZEE
```

## Need Help?

- GitHub Issues: https://github.com/ihariganesh/ZEE/issues
- Check logs: `journalctl --user -u zee-service@${USER}.service -f`
- Test manually: `cd ~/ZEE && source venv/bin/activate && python zee_service.py`

---

**Enjoy your personal AI assistant! 🎤✨**
