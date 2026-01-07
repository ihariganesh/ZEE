"""Voice recognition and text-to-speech module using FREE tools."""
import speech_recognition as sr
import pyttsx3
import threading
import tempfile
import os
from typing import Optional, Callable
from config import Config


class VoiceHandler:
    """Handles voice input and speech output using FREE tools."""
    
    def __init__(self):
        """Initialize voice recognition and text-to-speech engines."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize FREE text-to-speech engine (offline)
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', Config.SPEECH_RATE)
        
        # Try to use female voice if available
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Whisper setup (FREE local speech recognition)
        self.use_whisper = Config.USE_WHISPER
        self.whisper_model = None
        
        if self.use_whisper:
            try:
                import whisper
                print("Loading Whisper model (one-time setup)...")
                # Use 'base' model for good balance of speed/accuracy
                # Options: tiny, base, small, medium, large
                self.whisper_model = whisper.load_model("base")
                print("✅ Whisper loaded successfully!")
            except Exception as e:
                print(f"⚠️  Whisper not available: {e}")
                print("   Falling back to Google Speech Recognition (requires internet)")
                self.use_whisper = False
        
        # Adjust for ambient noise
        print("Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone ready!")
        
        self.listening = False
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text using FREE tools.
        
        Args:
            timeout: Maximum seconds to wait for phrase to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Recognized text or None if recognition failed
        """
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            
            # Try Whisper first (FREE & offline)
            if self.use_whisper and self.whisper_model:
                try:
                    # Save audio to temp file
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                        f.write(audio.get_wav_data())
                        temp_file = f.name
                    
                    # Transcribe with Whisper
                    result = self.whisper_model.transcribe(temp_file, language=Config.VOICE_LANGUAGE)
                    text = result["text"].strip()
                    
                    # Clean up
                    os.unlink(temp_file)
                    
                    print(f"💬 You said: {text}")
                    return text
                    
                except Exception as e:
                    print(f"Whisper error: {e}, falling back to Google...")
            
            # Fallback to Google (requires internet but FREE)
            text = self.recognizer.recognize_google(audio, language=Config.VOICE_LANGUAGE)
            print(f"💬 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️  Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Service error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def speak(self, text: str, async_mode: bool = False):
        """
        Convert text to speech using FREE offline TTS.
        
        Args:
            text: Text to speak
            async_mode: If True, speak in a separate thread
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str):
        """Synchronous speech helper method."""
        print(f"🔊 Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def continuous_listen(self, callback: Callable[[str], None], wake_word: str = "assistant"):
        """
        Continuously listen for the wake word, then process commands.
        
        Args:
            callback: Function to call with recognized speech
            wake_word: Word to activate the assistant
        """
        self.listening = True
        print(f"\n👂 Continuous listening mode activated.")
        print(f"   Say '{wake_word}' to activate.")
        print(f"   Press Ctrl+C to stop.\n")
        
        while self.listening:
            text = self.listen(timeout=10)
            if text and wake_word.lower() in text.lower():
                self.speak("Yes, how can I help?", async_mode=True)
                command = self.listen(timeout=5, phrase_time_limit=15)
                if command:
                    callback(command)
    
    def stop_listening(self):
        """Stop continuous listening mode."""
        self.listening = False
        print("🛑 Stopped listening.")


# Standalone testing
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Voice Handler with FREE Tools")
    print("="*60 + "\n")
    
    voice = VoiceHandler()
    
    # Test speaking
    voice.speak("Hello! Voice handler initialized successfully with free tools.")
    
    # Test listening
    print("\n💬 Say something to test speech recognition:")
    result = voice.listen()
    if result:
        voice.speak(f"You said: {result}")
