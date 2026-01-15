#!/usr/bin/env python3
"""ZEE Service Daemon - Runs in background and responds to wake word."""
import sys
import os
import signal
import time
from pathlib import Path

# Suppress ALSA warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
import warnings
warnings.filterwarnings('ignore')

# Redirect stderr to suppress ALSA messages
import ctypes
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    pass

# Add project directory to path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

# Redirect stdout/stderr to log file for service mode
import sys
log_file = project_dir / "logs" / "zee_service.log"
log_file.parent.mkdir(exist_ok=True)
sys.stdout = open(log_file, 'a', buffering=1)
sys.stderr = sys.stdout
print(f"\n{'='*60}")
print(f"ZEE Service Log - {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}\n")

from voice_handler import VoiceHandler
from system_controller import SystemController, PhoneController
from research_engine import ResearchEngine
from user_profile import UserProfile
from daily_briefing import DailyBriefing
from task_manager import TaskManager
from workspace_helper import WorkspaceHelper
from advanced_ai import AdvancedAI
from config import Config


class ZEEService:
    """ZEE AI Assistant running as background service."""
    
    def __init__(self):
        """Initialize ZEE service."""
        self.running = False
        self.profile = UserProfile()
        
        print("\n" + "="*60)
        print("🤖 ZEE AI Service - Starting...")
        print("="*60)
        
        # Initialize modules
        self.voice = VoiceHandler()
        self.system = SystemController()
        self.phone = PhoneController()
        self.research = ResearchEngine()
        self.briefing = DailyBriefing()
        self.tasks = TaskManager()
        self.workspace = WorkspaceHelper()
        self.advanced_ai = AdvancedAI(self.research)
        
        # No automation for now (X11 issues)
        self.automation = None
        
        print("✅ Advanced AI initialized - Context-aware responses")
        print("\n✅ ZEE Service Ready!")
        print("="*60)
        print("💡 Say 'Hey ZEE' or 'ZEE' to activate")
        print("   Press Ctrl+C to stop service")
        print("="*60 + "\n")
    
    def greet_user(self):
        """Greet user on service start."""
        if not self.profile.has_name():
            self.voice.speak("Hey! I'm ZEE, your AI assistant. What's your name?")
            name_response = self.voice.listen(timeout=15, phrase_time_limit=5)
            if name_response:
                name = name_response.lower().replace("my name is", "").replace("i'm", "").replace("i am", "").strip()
                name = name.split()[0].capitalize() if name else "Friend"
                self.profile.set_name(name)
                self.voice.speak(f"Nice to meet you, {name}! I'm always here when you need me. Just say 'Hey ZEE'!")
            else:
                self.voice.speak("No worries! Just say 'Hey ZEE' whenever you need me.")
        else:
            name = self.profile.get_name()
            self.voice.speak(f"Hey {name}! ZEE is ready. Just say my name whenever you need help!")
        
        self.profile.update_last_use()
    
    def process_command(self, command: str):
        """Process voice command."""
        command_lower = command.lower()
        print(f"\n🎯 Processing: {command}")
        
        # Add user message to conversation history
        self.advanced_ai.conversation.add_message("user", command)
        
        # Stop speaking command
        if any(word in command_lower for word in ['stop', 'quiet', 'shut up', 'stop talking', 'stop speaking']):
            self.voice.stop_speech()
            return
        
        # Daily briefing
        elif any(phrase in command_lower for phrase in ["what's special today", 'whats special today', 'daily briefing', "what's today", "today's briefing"]):
            city = self.profile.get_preference('city', 'Karur')
            country = self.profile.get_preference('country', 'India')
            briefing = self.briefing.format_briefing(city, country)
            self.voice.speak(briefing)
        
        # Exit/sleep commands
        elif any(word in command_lower for word in ['sleep', 'goodbye', 'stop listening']):
            self.voice.speak("Going to sleep. Say 'Hey ZEE' to wake me up!")
            return
        
        # System control
        elif 'open' in command_lower:
            self.voice.speak("On it!")
            if 'browser' in command_lower or 'chrome' in command_lower:
                self.system.open_application('browser')
                self.voice.speak("Browser opened")
            elif 'google' in command_lower:
                self.system.open_url('https://www.google.com')
                self.voice.speak("Google opened")
            elif 'youtube' in command_lower:
                self.system.open_url('https://www.youtube.com')
                self.voice.speak("YouTube opened")
            else:
                app_name = command_lower.replace('open', '').strip()
                if self.system.open_application(app_name):
                    self.voice.speak(f"{app_name} opened")
                else:
                    self.voice.speak(f"Sorry, couldn't find {app_name}")
        
        # Volume control
        elif 'volume' in command_lower:
            if 'up' in command_lower or 'increase' in command_lower:
                self.system.adjust_volume(change=10)
                self.voice.speak("Volume up")
            elif 'down' in command_lower or 'decrease' in command_lower:
                self.system.adjust_volume(change=-10)
                self.voice.speak("Volume down")
            elif 'mute' in command_lower:
                self.system.adjust_volume(level=0)
                self.voice.speak("Muted")
        
        # Research
        elif 'research' in command_lower or 'search' in command_lower or 'tell me about' in command_lower:
            topic = command_lower.replace('research', '').replace('search', '').replace('tell me about', '').strip()
            if topic:
                self.voice.speak(f"Researching {topic}")
                result = self.research.research_and_explain(topic)
                if result:
                    self.voice.speak(result)
            else:
                self.voice.speak("What would you like me to research?")
        
        # Help
        elif 'help' in command_lower or 'what can you do' in command_lower:
            help_text = """I'm your AI co-worker with advanced context awareness! I can help with: 
            Opening apps and websites. 
            Managing your tasks and notes. 
            Checking your workspace and git status. 
            Researching topics and answering questions with conversation memory. 
            Typing text and controlling your system. 
            I remember our conversation context and learn from your patterns. 
            Just ask me naturally!"""
            self.voice.speak(help_text)
        
        # Typing commands
        elif any(word in command_lower for word in ['type', 'write', 'enter', 'search for']):
            # Extract what to type
            text_to_type = command
            for word in ['type', 'Type', 'write', 'Write', 'enter', 'Enter', 'search for', 'Search for', 
                        'in my browser', 'in browser', 'on my screen', 'something', 'this']:
                text_to_type = text_to_type.replace(word, '')
            text_to_type = text_to_type.strip()
            
            if text_to_type:
                import pyautogui
                import time
                self.voice.speak("Typing")
                time.sleep(0.5)  # Brief delay to switch to window
                pyautogui.write(text_to_type, interval=0.05)
                print(f"✍️ Typed: {text_to_type}")
            else:
                self.voice.speak("What should I type?")
        
        # Task management
        elif any(phrase in command_lower for phrase in ['add task', 'new task', 'create task', 'remind me to', 'todo']):
            # Extract task description
            task_desc = command_lower
            for phrase in ['add task', 'new task', 'create task', 'remind me to', 'todo', 'to do']:
                task_desc = task_desc.replace(phrase, '')
            task_desc = task_desc.strip()
            
            if task_desc:
                self.tasks.add_task(task_desc)
                self.voice.speak(f"Added to your tasks: {task_desc}")
            else:
                self.voice.speak("What task should I add?")
        
        elif any(phrase in command_lower for phrase in ['list tasks', 'show tasks', 'my tasks', 'what tasks', 'task summary']):
            summary = self.tasks.get_summary()
            self.voice.speak(summary)
        
        elif 'complete task' in command_lower or 'task done' in command_lower:
            # Try to extract task ID or use first pending task
            pending = self.tasks.list_tasks("pending")
            if pending:
                self.tasks.complete_task(pending[0]["id"])
                self.voice.speak(f"Marked as complete: {pending[0]['description']}")
            else:
                self.voice.speak("No pending tasks to complete")
        
        # Note taking
        elif any(phrase in command_lower for phrase in ['take note', 'make note', 'note this', 'remember this']):
            note_content = command_lower
            for phrase in ['take note', 'make note', 'note this', 'remember this', 'that']:
                note_content = note_content.replace(phrase, '')
            note_content = note_content.strip()
            
            if note_content:
                self.tasks.add_note(note_content)
                self.voice.speak("Note saved")
            else:
                self.voice.speak("What should I note?")
        
        # Workspace awareness
        elif any(phrase in command_lower for phrase in ['what am i working on', 'current context', 'workspace status']):
            context = self.workspace.get_context_summary()
            self.voice.speak(context)
        
        elif 'git status' in command_lower:
            git_status = self.workspace.get_git_status()
            if git_status:
                self.voice.speak(f"Git status: {git_status}")
            else:
                self.voice.speak("Not in a git repository")
        
        else:
            # General query - use advanced context-aware AI
            self.voice.speak("Let me think about that")
            
            # Add current context to the conversation
            workspace_context = self.workspace.get_context_summary()
            task_context = self.tasks.get_summary()
            
            # Generate smart response with context
            result = self.advanced_ai.generate_smart_response(
                command,
                context=f"Workspace: {workspace_context}\nTasks: {task_context}"
            )
            
            if result:
                self.voice.speak(result)
            else:
                self.voice.speak("I'm not sure how to help with that. Try asking differently!")
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word 'ZEE' or 'Hey ZEE'."""
        # Accept various pronunciations Vosk might recognize
        wake_words = ['zee', 'hey zee', 'ok zee', 'hey z', ' z ', 'z', 'hazy', 'hey easy', 'easy', 'the z']
        
        while self.running:
            try:
                # Listen with longer phrase limit to catch full commands
                text = self.voice.listen(timeout=30, phrase_time_limit=10)
                
                if text:
                    text_lower = text.lower()
                    
                    # Check for wake word
                    wake_word_found = None
                    for wake in wake_words:
                        if wake in text_lower:
                            wake_word_found = wake
                            break
                    
                    if wake_word_found:
                        print(f"\n🎤 Wake word detected: {text}")
                        
                        # Check if command is already in the same sentence
                        command_part = text_lower.replace(wake_word_found, '', 1).strip()
                        
                        if command_part and len(command_part) > 3:
                            # Process command immediately (e.g., "zee open browser")
                            print(f"🚀 Immediate command: {command_part}")
                            self.process_command(command_part)
                        else:
                            # No command yet, ask for it
                            self.voice.speak("Yes?")
                            
                            # Listen for actual command
                            command = self.voice.listen(timeout=10, phrase_time_limit=15)
                            if command:
                                self.process_command(command)
                            else:
                                self.voice.speak("I didn't catch that.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                time.sleep(1)
    
    def start(self):
        """Start the ZEE service."""
        self.running = True
        
        # Greet user on first start
        self.greet_user()
        
        # Start listening for wake word
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping ZEE service...")
            self.voice.speak("Goodbye! ZEE service stopped.")
            self.running = False
    
    def stop(self):
        """Stop the ZEE service."""
        self.running = False


def main():
    """Main entry point for ZEE service."""
    service = ZEEService()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n\n🛑 Received stop signal...")
        service.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start service
    service.start()


if __name__ == "__main__":
    main()
