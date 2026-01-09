# ZEE AI Assistant 🤖

A **FREE**, **cross-platform** (Windows/Linux) AI assistant with **wake word detection** - just like Siri or Google Assistant!

## ✨ Features

✅ **100% FREE** - No paid subscriptions required!  
✅ **Wake Word Activated** - Say "Hey ZEE" anytime (like Siri/Alexa)  
✅ **Auto-Start Service** - Runs in background on boot  
✅ **Cross-Platform** - Works on Windows, Linux (Ubuntu, Arch, etc.)  
✅ **Natural Voice** - Google Neural TTS (sounds like Siri/Gemini)  
✅ **System Control** - Open apps, adjust volume, WiFi, brightness  
✅ **AI Research** - Web search with AI explanations  
✅ **Offline Mode** - Works without internet (with Ollama)  

## 🆓 FREE Tools Used

| Component | Tool | Cost |
|-----------|------|------|
| **AI Model** | Groq API (Llama 3.1) | FREE (14K+ requests/day) |
| **Offline AI** | Ollama (local) | FREE |
| **Voice Input** | Google Speech Recognition | FREE |
| **Voice Output** | Google TTS (neural) | FREE (like Siri/Gemini) |
| **Fallback TTS** | pyttsx3 (offline) | FREE |
| **Web Search** | DuckDuckGo | FREE (no API key) |

## 🎙️ Two Usage Modes

### Mode 1: Background Service (Recommended)
- Auto-starts on boot
- Always listening for "Hey ZEE"
- Hands-free operation
- See [SERVICE_SETUP.md](SERVICE_SETUP.md) for installation

### Mode 2: Command-Line (Manual)
- Run manually when needed
- Type or speak commands
- No wake word required

## 🚀 Quick Start

### 1. Install Dependencies

**On Linux (Ubuntu/Debian):**
```bash
# System dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip portaudio19-dev espeak ffmpeg mpg123

# Clone the repo
git clone https://github.com/ihariganesh/ZEE.git
cd ZEE

# Run setup
chmod +x setup.sh
./setup.sh
```

**On Linux (Arch):**
```bash
# System dependencies
sudo pacman -S python python-pip portaudio espeak ffmpeg mpg123

# Clone and setup
git clone https://github.com/ihariganesh/ZEE.git
cd ZEE
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```cmd
# Clone the repo
git clone https://github.com/ihariganesh/ZEE.git
cd ZEE

# Run setup
setup.bat
```

### 2. Get FREE Groq API Key (Required)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (FREE)
3. Get your API key
4. Edit `config.py`:
   ```python
   GROQ_API_KEY = "your_key_here"
   ```

### 3. Install Ollama (Optional - for Offline AI)

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

**Windows:**
```
Download from: https://ollama.ai/download
Run: ollama pull llama3.2
```

### 4. Choose Your Mode

**Option A: Background Service (Wake Word Mode)**

Install ZEE as a service that auto-starts on boot:

```bash
# See detailed instructions
cat SERVICE_SETUP.md

# Quick install
mkdir -p ~/.config/systemd/user
cp zee-service@.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable zee-service@$USER.service
systemctl --user start zee-service@$USER.service

# Check status
systemctl --user status zee-service@$USER.service

# View logs
tail -f logs/zee_service.log
```

Now say **"Hey ZEE"** or **"ZEE"** anytime!

**Option B: Command-Line Mode (Manual)**

```bash
# Activate virtual environment
source venv/bin/activate  # Linux
# OR
venv\Scripts\activate.bat  # Windows

# Run
python main.py
```

## 🎤 Voice Commands

### Wake Word (Service Mode Only)
```
"Hey ZEE" - Activates the assistant
"ZEE" - Short activation
"OK ZEE" - Alternative activation
```

### Opening Applications
```
"Open browser"
"Open Chrome"
"Open Google"
"Open ChatGPT"
"Open calculator"
```

### System Control
```
"Volume up" / "Volume down"
"Set volume to 50"
"Mute" / "Unmute"
"Turn WiFi on/off"
"Set brightness to 50 percent"
"System info"
```

### Research & AI
```
"Research quantum computing"
"Tell me about machine learning"
"Search for Python tutorials"
"Help" - Show available commands
```

## 🔧 Service Management (Background Mode)

```bash
# Start service
systemctl --user start zee-service@$USER.service

# Stop service
systemctl --user stop zee-service@$USER.service

# Restart service
systemctl --user restart zee-service@$USER.service

# Check status
systemctl --user status zee-service@$USER.service

# View live logs
tail -f ~/ZEE/logs/zee_service.log

# Enable auto-start on boot
systemctl --user enable zee-service@$USER.service

# Disable auto-start
systemctl --user disable zee-service@$USER.service
```

## 📁 Project Structure

```
ZEE/
├── main.py                    # Command-line interface
├── zee_service.py             # Background service daemon
├── zee-service@.service       # Systemd service file
├── config.py                  # Configuration
├── voice_handler.py           # Speech (Google TTS + Speech Recognition)
├── system_controller.py       # System control
├── research_engine.py         # Research (Groq + Ollama + DuckDuckGo)
├── user_profile.py            # User personalization
├── requirements.txt           # Dependencies
├── SERVICE_SETUP.md           # Service installation guide
├── AUDIO_SETUP.md            # Microphone troubleshooting
└── README.md                 # This file
```

## ⚙️ Configuration

Edit `config.py`:

```python
# FREE Groq API (required)
GROQ_API_KEY = "your_groq_api_key_here"

# Ollama (local AI, completely free)
OLLAMA_BASE_URL = "http://localhost:11434"
USE_OLLAMA_OFFLINE = True

# Voice settings
VOICE_LANGUAGE = "en"
SPEECH_RATE = 150

# Research
MAX_SEARCH_RESULTS = 5
```

## 🔧 Troubleshooting

### Service Not Starting
```bash
# Check service status
systemctl --user status zee-service@$USER.service

# View logs
tail -50 ~/ZEE/logs/zee_service.log

# Test manually
cd ~/ZEE
source venv/bin/activate
python zee_service.py
```

### Microphone not working
```bash
# Test microphone
python voice_handler.py

# Linux: Check permissions
sudo usermod -a -G audio $USER
```

### Whisper model download
First run will download Whisper model (~140MB). Wait for it to complete.

### Groq API errors
- Check your API key in `.env`
- Free tier: 14,400 requests/day
- Get key: https://console.groq.com

### Ollama not working
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Install a model
ollama pull llama3.2
```

### Linux audio issues
```bash
# Install missing audio libraries
sudo apt-get install portaudio19-dev python3-pyaudio
```

## 🌐 Platform-Specific Notes

### Windows
- Run as Administrator for system control features
- Windows Defender may block keyboard automation
- Add exception in Settings → Privacy → Accessibility

### Linux
- Some features need sudo (volume, brightness)
- Brightness control varies by hardware
- Use `xbacklight` or `brightnessctl`

### Arch Linux
- Use `yay` or `paru` for AUR packages if needed
- espeak-ng recommended for better TTS

## 🔐 Privacy & Security

✅ **Private**: Whisper runs locally (no cloud)  
✅ **Free**: No paid subscriptions  
✅ **Open**: All code is transparent  
⚠️ **System Access**: Has broad system permissions - use responsibly  

## 📊 Cost Comparison

| Service | This Project | ChatGPT Plus | Claude Pro |
|---------|-------------|--------------|------------|
| **Cost** | **FREE** | $20/month | $20/month |
| **Offline** | ✅ Yes (Ollama) | ❌ No | ❌ No |
| **Voice** | ✅ Free | ❌ Paid | ❌ Paid |
| **Automation** | ✅ Yes | ❌ Limited | ❌ Limited |

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] GUI interface
- [ ] Smart home integration
- [ ] Calendar/email integration
- [ ] Mobile app (Android/iOS)

## 📜 License

MIT License - Free to use, modify, and distribute

## 🙏 Credits

- **Groq** - Free fast AI inference
- **Ollama** - Free local LLM runtime
- **OpenAI Whisper** - Free speech recognition
- **DuckDuckGo** - Free search API

## 🤝 Contributing

Pull requests welcome! Feel free to:
- Add new features
- Fix bugs
- Improve documentation
- Add language support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ihariganesh/ZEE/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ihariganesh/ZEE/discussions)

---

**Made with ❤️ using only FREE tools!**

⭐ Star this repo if you find it useful!
