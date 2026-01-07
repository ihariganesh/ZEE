# ZEE AI Assistant 🤖

A **FREE**, **cross-platform** (Windows/Linux) voice-controlled AI assistant that uses only free tools and APIs.

## ✨ Features

✅ **100% FREE** - No paid subscriptions required!  
✅ **Cross-Platform** - Works on Windows, Linux (Ubuntu, Arch, etc.)  
✅ **Voice Control** - Hands-free operation  
✅ **System Control** - Open apps, adjust settings  
✅ **Auto-Typing** - Voice-to-text automation  
✅ **AI Research** - Web search with AI explanations  
✅ **Offline Mode** - Works without internet (with Ollama)  

## 🆓 FREE Tools Used

| Component | Tool | Cost |
|-----------|------|------|
| **AI Model** | Groq API (Llama 3.1) | FREE (14K+ requests/day) |
| **Offline AI** | Ollama (local) | FREE |
| **Voice Input** | OpenAI Whisper (local) | FREE |
| **Voice Output** | pyttsx3 (offline TTS) | FREE |
| **Web Search** | DuckDuckGo | FREE (no API key) |

## 🚀 Quick Start

### 1. Install Dependencies

**On Linux (Ubuntu/Debian):**
```bash
# System dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip portaudio19-dev espeak ffmpeg

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
sudo pacman -S python python-pip portaudio espeak ffmpeg

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

### 2. Get FREE Groq API Key (Optional but Recommended)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (FREE)
3. Get your API key
4. Edit `.env` file:
   ```
   GROQ_API_KEY=your_key_here
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

### 4. Run the Assistant

```bash
# Activate virtual environment
source venv/bin/activate  # Linux
# OR
venv\Scripts\activate.bat  # Windows

# Run
python main.py --mode interactive
```

Say "**assistant**" followed by your command!

## 🎤 Voice Commands

### Opening Applications
```
"Open browser"
"Open Google"
"Open ChatGPT"
"Open calculator"
```

### System Control
```
"Volume up" / "Volume down"
"Mute volume"
"Turn WiFi on/off"
"Set brightness to 50 percent"
"System info"
```

### Auto-Typing
```
"Type [text]"
"Dictate"  # Start continuous typing
```

### Research & AI
```
"Research quantum computing"
"Tell me about machine learning"
"Search for Python tutorials"
```

### Window Management
```
"Switch window"
"Minimize window"
"Take screenshot"
```

### Exit
```
"Exit" / "Quit" / "Goodbye"
```

## 📁 Project Structure

```
ZEE/
├── main.py                    # Main application
├── config.py                  # Configuration
├── voice_handler.py           # Speech (Whisper + pyttsx3)
├── system_controller.py       # System control
├── automation_controller.py   # Typing automation
├── research_engine.py         # Research (Groq + Ollama)
├── requirements.txt           # Dependencies
├── .env                       # API keys (create from .env.example)
└── README.md                 # This file
```

## ⚙️ Configuration

Edit `.env` file:

```bash
# FREE Groq API (highly recommended)
GROQ_API_KEY=your_groq_api_key_here

# Ollama (local AI, completely free)
OLLAMA_BASE_URL=http://localhost:11434
USE_OLLAMA_OFFLINE=true

# Voice settings
USE_WHISPER=true  # Use local Whisper (free)
VOICE_LANGUAGE=en
SPEECH_RATE=150

# Research
MAX_SEARCH_RESULTS=5
```

## 🔧 Troubleshooting

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
