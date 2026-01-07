"""Automation module for typing and keyboard/mouse control."""
import time
from typing import Optional


class AutomationController:
    """Handles automated typing and keyboard/mouse operations."""
    
    def __init__(self):
        """Initialize automation controller."""
        # Check if X11 display is available
        import os
        if not os.environ.get('DISPLAY'):
            raise RuntimeError("No DISPLAY environment variable - GUI automation requires X11")
        
        # Import here to avoid X11 issues
        try:
            import pyautogui
            import keyboard
            self.pyautogui = pyautogui
            self.keyboard = keyboard
            
            # Set up safety settings
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
            print("✅ Automation Controller initialized")
        except Exception as e:
            raise RuntimeError(f"Automation not available: {e}")
    
    # ===== Typing Automation =====
    
    def type_text(self, text: str, interval: float = 0.05, press_enter: bool = False):
        """
        Type text automatically.
        
        Args:
            text: Text to type
            interval: Seconds between each keystroke
            press_enter: Whether to press Enter after typing
        """
        try:
            print(f"Typing: {text[:50]}...")  # Show first 50 chars
            time.sleep(1)  # Give user time to focus on the desired window
            
            self.pyautogui.write(text, interval=interval)
            
            if press_enter:
                self.pyautogui.press('enter')
            
            print("Typing completed")
            return True
            
        except Exception as e:
            print(f"Error during automated typing: {e}")
            return False
    
    def press_keys(self, *keys):
        """
        Press one or more keys.
        
        Args:
            *keys: Key names to press (e.g., 'ctrl', 'c', 'enter')
        """
        try:
            if len(keys) == 1:
                self.pyautogui.press(keys[0])
            else:
                self.pyautogui.hotkey(*keys)
            print(f"Pressed keys: {' + '.join(keys)}")
            return True
        except Exception as e:
            print(f"Error pressing keys: {e}")
            return False
    
    def keyboard_shortcut(self, shortcut: str):
        """
        Execute a keyboard shortcut.
        
        Args:
            shortcut: Shortcut string like "ctrl+c", "alt+tab"
        """
        try:
            keys = shortcut.lower().split('+')
            self.pyautogui.hotkey(*keys)
            print(f"Executed shortcut: {shortcut}")
            return True
        except Exception as e:
            print(f"Error executing shortcut: {e}")
            return False
    
    # ===== Clipboard Operations =====
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            print(f"Copied to clipboard: {text[:50]}...")
            return True
        except ImportError:
            print("pyperclip not available, using alternative method")
            # Fallback method
            self.keyboard.write(text)
            self.keyboard.send('ctrl+a')
            self.keyboard.send('ctrl+c')
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    def paste_from_clipboard(self):
        """Paste from clipboard."""
        try:
            self.pyautogui.hotkey('ctrl', 'v')
            print("Pasted from clipboard")
            return True
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")
            return False
    
    # ===== Mouse Operations =====
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """
        Move mouse to coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to complete movement in seconds
        """
        try:
            self.pyautogui.moveTo(x, y, duration=duration)
            print(f"Moved mouse to ({x}, {y})")
            return True
        except Exception as e:
            print(f"Error moving mouse: {e}")
            return False
    
    def click_mouse(self, x: Optional[int] = None, y: Optional[int] = None, 
                    clicks: int = 1, button: str = 'left'):
        """
        Click mouse at current or specified position.
        
        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            clicks: Number of clicks
            button: 'left', 'right', or 'middle'
        """
        try:
            if x is not None and y is not None:
                self.pyautogui.click(x=x, y=y, clicks=clicks, button=button)
                print(f"Clicked at ({x}, {y})")
            else:
                self.pyautogui.click(clicks=clicks, button=button)
                print(f"Clicked at current position")
            return True
        except Exception as e:
            print(f"Error clicking mouse: {e}")
            return False
    
    def scroll(self, clicks: int):
        """
        Scroll up (positive) or down (negative).
        
        Args:
            clicks: Number of scroll clicks (positive=up, negative=down)
        """
        try:
            self.pyautogui.scroll(clicks)
            direction = "up" if clicks > 0 else "down"
            print(f"Scrolled {direction} {abs(clicks)} clicks")
            return True
        except Exception as e:
            print(f"Error scrolling: {e}")
            return False
    
    # ===== Screen Operations =====
    
    def get_screen_size(self) -> tuple:
        """Get screen dimensions."""
        return self.pyautogui.size()
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position."""
        return self.pyautogui.position()
    
    def screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot.
        
        Args:
            filename: Optional filename to save to
            
        Returns:
            Filename where screenshot was saved
        """
        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            
            screenshot = self.pyautogui.screenshot()
            screenshot.save(filename)
            print(f"Screenshot saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return ""
    
    # ===== Text Input with Voice =====
    
    def dictate_and_type(self, voice_handler, duration: int = 10):
        """
        Listen to voice and type what's said.
        
        Args:
            voice_handler: VoiceHandler instance
            duration: Maximum recording duration
        """
        try:
            print("Start speaking (will type what you say)...")
            time.sleep(1)
            
            text = voice_handler.listen(phrase_time_limit=duration)
            if text:
                self.type_text(text)
                return True
            else:
                print("No speech detected")
                return False
                
        except Exception as e:
            print(f"Error during dictation: {e}")
            return False
    
    # ===== Window Management =====
    
    def switch_window(self):
        """Switch to next window (Alt+Tab)."""
        return self.keyboard_shortcut("alt+tab")
    
    def minimize_window(self):
        """Minimize current window."""
        import platform
        if platform.system() == "Darwin":
            return self.keyboard_shortcut("command+m")
        else:
            return self.keyboard_shortcut("win+down")
    
    def maximize_window(self):
        """Maximize current window."""
        import platform
        if platform.system() == "Darwin":
            # macOS doesn't have a standard maximize shortcut
            return self.press_keys('f11')  # Fullscreen
        else:
            return self.keyboard_shortcut("win+up")


# Standalone testing
if __name__ == "__main__":
    automation = AutomationController()
    
    # Display screen info
    screen_size = automation.get_screen_size()
    mouse_pos = automation.get_mouse_position()
    
    print(f"\nScreen size: {screen_size}")
    print(f"Mouse position: {mouse_pos}")
    
    # Test typing (commented out to prevent accidental typing)
    # print("\nTesting typing in 3 seconds...")
    # time.sleep(3)
    # automation.type_text("Hello from AI Assistant!", press_enter=True)
