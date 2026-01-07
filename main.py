"""Main AI Assistant application - Platform Independent (Windows/Linux)."""
import sys
import argparse
from voice_handler import VoiceHandler
from system_controller import SystemController, PhoneController
from automation_controller import AutomationController
from research_engine import ResearchEngine
from config import Config


class AIAssistant:
    """Main AI Assistant that orchestrates all modules."""
    
    def __init__(self):
        """Initialize the AI Assistant."""
        print("\n" + "="*60)
        print("🤖 ZEE AI Assistant - Initializing...")
        print("="*60 + "\n")
        
        # Validate configuration
        Config.validate()
        
        # Initialize all modules
        print("\n📦 Loading modules...")
        self.voice = VoiceHandler()
        self.system = SystemController()
        self.phone = PhoneController()
        self.automation = AutomationController()
        self.research = ResearchEngine()
        
        print("\n" + "="*60)
        print("✅ ZEE AI Assistant Ready!")
        print("="*60)
        print("\n💡 Using FREE Tools:")
        print("   • Voice: Whisper (local) or Google Speech")
        print("   • AI: Groq API (free) + Ollama (offline)")
        print("   • Search: DuckDuckGo (no API key)")
        print("="*60 + "\n")
    
    def process_command(self, command: str) -> bool:
        """
        Process a voice command.
        
        Args:
            command: Command text to process
            
        Returns:
            True to continue, False to exit
        """
        command_lower = command.lower()
        
        # Exit commands
        if any(word in command_lower for word in ['exit', 'quit', 'goodbye', 'stop']):
            self.voice.speak("Goodbye!")
            return False
        
        # System control commands
        elif 'open' in command_lower:
            if 'browser' in command_lower or 'chrome' in command_lower:
                self.system.open_application('browser')
                self.voice.speak("Opening browser")
            elif 'google' in command_lower:
                self.system.open_url('https://www.google.com')
                self.voice.speak("Opening Google")
            elif 'chatgpt' in command_lower or 'chat gpt' in command_lower:
                self.system.open_url('https://chat.openai.com')
                self.voice.speak("Opening ChatGPT")
            else:
                # Extract app name
                app_name = command_lower.replace('open', '').strip()
                if self.system.open_application(app_name):
                    self.voice.speak(f"Opening {app_name}")
                else:
                    self.voice.speak(f"Could not open {app_name}")
        
        # Settings control
        elif 'volume' in command_lower:
            if 'up' in command_lower or 'increase' in command_lower:
                self.system.adjust_volume(change=10)
                self.voice.speak("Volume increased")
            elif 'down' in command_lower or 'decrease' in command_lower:
                self.system.adjust_volume(change=-10)
                self.voice.speak("Volume decreased")
            elif 'mute' in command_lower:
                self.system.adjust_volume(level=0)
                self.voice.speak("Volume muted")
        
        elif 'wifi' in command_lower or 'wi-fi' in command_lower:
            if 'on' in command_lower or 'enable' in command_lower:
                self.system.toggle_wifi(True)
                self.voice.speak("Turning WiFi on")
            elif 'off' in command_lower or 'disable' in command_lower:
                self.system.toggle_wifi(False)
                self.voice.speak("Turning WiFi off")
        
        elif 'brightness' in command_lower:
            # Try to extract percentage
            words = command_lower.split()
            for i, word in enumerate(words):
                if word.isdigit() or (word.endswith('%') and word[:-1].isdigit()):
                    level = int(word.replace('%', ''))
                    self.system.set_brightness(level)
                    self.voice.speak(f"Setting brightness to {level} percent")
                    break
        
        # System info
        elif 'system' in command_lower and 'info' in command_lower:
            info = self.system.get_system_info()
            response = f"CPU usage is {info['cpu_percent']} percent. "
            response += f"Memory usage is {info['memory_percent']} percent. "
            if info['battery']:
                response += f"Battery is at {info['battery']['percent']} percent. "
            self.voice.speak(response)
        
        # Typing automation
        elif 'type' in command_lower or 'write' in command_lower:
            self.voice.speak("What should I type? Start speaking after the beep.")
            text = self.voice.listen(phrase_time_limit=15)
            if text:
                self.automation.type_text(text)
                self.voice.speak("Typing completed")
            else:
                self.voice.speak("I didn't hear anything to type")
        
        elif 'dictate' in command_lower or 'transcribe' in command_lower:
            self.voice.speak("Start dictating. I will type what you say.")
            self.automation.dictate_and_type(self.voice, duration=30)
        
        # Research commands
        elif any(word in command_lower for word in ['research', 'search', 'find', 'look up', 'tell me about']):
            # Extract topic
            for phrase in ['research', 'search for', 'find', 'look up', 'tell me about']:
                if phrase in command_lower:
                    topic = command_lower.split(phrase, 1)[1].strip()
                    break
            else:
                topic = command_lower
            
            if topic:
                self.voice.speak(f"Researching {topic}. This may take a moment.")
                result = self.research.research_and_explain(topic)
                
                if result['success']:
                    # Speak the summary
                    if result['explanation']:
                        self.voice.speak(result['explanation'])
                    else:
                        # Read out the first result
                        first_result = result['results'][0]
                        response = f"Here's what I found: {first_result['title']}. "
                        if first_result['snippet']:
                            response += first_result['snippet'][:200]
                        self.voice.speak(response)
                else:
                    self.voice.speak("Sorry, I couldn't find any information on that topic")
            else:
                self.voice.speak("What would you like me to research?")
        
        # Window management
        elif 'switch window' in command_lower or 'next window' in command_lower:
            self.automation.switch_window()
            self.voice.speak("Switching window")
        
        elif 'minimize' in command_lower:
            self.automation.minimize_window()
            self.voice.speak("Minimizing window")
        
        elif 'maximize' in command_lower:
            self.automation.maximize_window()
            self.voice.speak("Maximizing window")
        
        # Screenshot
        elif 'screenshot' in command_lower or 'screen shot' in command_lower:
            filename = self.automation.screenshot()
            if filename:
                self.voice.speak(f"Screenshot saved as {filename}")
            else:
                self.voice.speak("Failed to take screenshot")
        
        # Help
        elif 'help' in command_lower or 'what can you do' in command_lower:
            help_text = """I can help you with:
            Opening applications like browser, Google, or ChatGPT.
            Controlling settings like volume, WiFi, and brightness.
            Typing automatically based on your voice.
            Researching topics and explaining them to you.
            Taking screenshots and managing windows.
            Just ask me naturally!"""
            self.voice.speak(help_text)
        
        else:
            self.voice.speak("I'm not sure how to help with that. Try saying 'help' to see what I can do.")
        
        return True
    
    def run_interactive(self):
        """Run the assistant in interactive mode with continuous listening."""
        print("\nStarting interactive mode...")
        print("Say 'assistant' to activate, or type commands directly.")
        print("Say 'exit' or 'quit' to stop.\n")
        
        try:
            def command_callback(command: str):
                """Callback for continuous listening."""
                if not self.process_command(command):
                    self.voice.stop_listening()
            
            self.voice.continuous_listen(command_callback, wake_word="assistant")
            
        except KeyboardInterrupt:
            print("\nStopping...")
            self.voice.speak("Goodbye!")
    
    def run_single_command(self, command: str = None):
        """Run a single command."""
        if command is None:
            self.voice.speak("What can I help you with?")
            command = self.voice.listen(phrase_time_limit=15)
        
        if command:
            self.process_command(command)
        else:
            print("No command received")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='AI Assistant')
    parser.add_argument('--mode', choices=['interactive', 'single'], default='interactive',
                       help='Run mode: interactive (continuous) or single command')
    parser.add_argument('--command', type=str, help='Command to execute in single mode')
    
    args = parser.parse_args()
    
    try:
        assistant = AIAssistant()
        
        if args.mode == 'interactive':
            assistant.run_interactive()
        else:
            assistant.run_single_command(args.command)
            
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
