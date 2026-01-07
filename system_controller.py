"""System control module for laptop and phone operations."""
import subprocess
import platform
import psutil
import os
from typing import List, Optional
from config import Config


class SystemController:
    """Controls system-level operations on laptop and phone."""
    
    def __init__(self):
        """Initialize system controller."""
        self.os_type = platform.system()
        print(f"System Controller initialized for {self.os_type}")
    
    # ===== Application Control =====
    
    def open_application(self, app_name: str) -> bool:
        """
        Open an application by name.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            True if successful, False otherwise
        """
        try:
            app_name_lower = app_name.lower()
            
            if self.os_type == "Windows":
                # Windows application mapping
                apps = {
                    "chrome": "chrome",
                    "browser": "chrome",
                    "firefox": "firefox",
                    "notepad": "notepad",
                    "calculator": "calc",
                    "explorer": "explorer",
                }
                cmd = apps.get(app_name_lower, app_name)
                subprocess.Popen([cmd])
                
            elif self.os_type == "Darwin":  # macOS
                # macOS application mapping
                apps = {
                    "chrome": "Google Chrome",
                    "browser": "Safari",
                    "safari": "Safari",
                    "firefox": "Firefox",
                    "notes": "Notes",
                    "calculator": "Calculator",
                }
                app = apps.get(app_name_lower, app_name)
                subprocess.Popen(["open", "-a", app])
                
            elif self.os_type == "Linux":
                # Linux application mapping
                apps = {
                    "chrome": "google-chrome",
                    "browser": "firefox",
                    "firefox": "firefox",
                    "terminal": "gnome-terminal",
                    "calculator": "gnome-calculator",
                }
                cmd = apps.get(app_name_lower, app_name)
                subprocess.Popen([cmd])
            
            print(f"Opened application: {app_name}")
            return True
            
        except Exception as e:
            print(f"Error opening application {app_name}: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """
        Open a URL in the default browser.
        
        Args:
            url: URL to open
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import webbrowser
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            print(f"Opened URL: {url}")
            return True
        except Exception as e:
            print(f"Error opening URL {url}: {e}")
            return False
    
    def close_application(self, app_name: str) -> bool:
        """
        Close an application by name.
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            True if successful, False otherwise
        """
        try:
            app_name_lower = app_name.lower()
            killed = False
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if app_name_lower in proc.info['name'].lower():
                        proc.terminate()
                        killed = True
                        print(f"Closed: {proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return killed
            
        except Exception as e:
            print(f"Error closing application {app_name}: {e}")
            return False
    
    # ===== System Settings =====
    
    def adjust_volume(self, level: Optional[int] = None, change: Optional[int] = None) -> bool:
        """
        Adjust system volume.
        
        Args:
            level: Set volume to specific level (0-100)
            change: Increase/decrease volume by amount (+/- value)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.os_type == "Darwin":  # macOS
                if level is not None:
                    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
                elif change is not None:
                    current = subprocess.check_output(
                        ["osascript", "-e", "output volume of (get volume settings)"]
                    )
                    new_level = max(0, min(100, int(current) + change))
                    subprocess.run(["osascript", "-e", f"set volume output volume {new_level}"])
                print(f"Volume adjusted")
                return True
                
            elif self.os_type == "Linux":
                if level is not None:
                    subprocess.run(["amixer", "set", "Master", f"{level}%"])
                elif change is not None:
                    direction = "+" if change > 0 else "-"
                    subprocess.run(["amixer", "set", "Master", f"{abs(change)}%{direction}"])
                print(f"Volume adjusted")
                return True
                
            elif self.os_type == "Windows":
                # Windows volume control requires additional library
                print("Volume control on Windows requires nircmd or similar utility")
                return False
                
        except Exception as e:
            print(f"Error adjusting volume: {e}")
            return False
    
    def set_brightness(self, level: int) -> bool:
        """
        Set screen brightness (0-100).
        
        Args:
            level: Brightness level (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            level = max(0, min(100, level))
            
            if self.os_type == "Darwin":  # macOS
                subprocess.run(["brightness", str(level / 100)])
                print(f"Brightness set to {level}%")
                return True
                
            elif self.os_type == "Linux":
                # This varies by system, using xrandr as example
                subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", str(level / 100)])
                print(f"Brightness set to {level}%")
                return True
                
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False
    
    def toggle_wifi(self, enable: bool) -> bool:
        """
        Toggle WiFi on/off.
        
        Args:
            enable: True to enable, False to disable
            
        Returns:
            True if successful, False otherwise
        """
        try:
            action = "on" if enable else "off"
            
            if self.os_type == "Darwin":  # macOS
                subprocess.run(["networksetup", "-setairportpower", "en0", action])
                print(f"WiFi turned {action}")
                return True
                
            elif self.os_type == "Linux":
                subprocess.run(["nmcli", "radio", "wifi", action])
                print(f"WiFi turned {action}")
                return True
                
        except Exception as e:
            print(f"Error toggling WiFi: {e}")
            return False
    
    # ===== System Information =====
    
    def get_system_info(self) -> dict:
        """
        Get system information.
        
        Returns:
            Dictionary with system info
        """
        try:
            info = {
                "os": self.os_type,
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "battery": None
            }
            
            # Get battery info if available
            battery = psutil.sensors_battery()
            if battery:
                info["battery"] = {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged
                }
            
            return info
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}


class PhoneController:
    """Controls phone operations via ADB (Android Debug Bridge)."""
    
    def __init__(self):
        """Initialize phone controller."""
        self.enabled = Config.ENABLE_PHONE_CONTROL
        if not self.enabled:
            print("Phone control is disabled in configuration")
    
    def check_connection(self) -> bool:
        """Check if phone is connected via ADB."""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True
            )
            devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
            return len(devices) > 0
        except FileNotFoundError:
            print("ADB not found. Please install Android platform tools.")
            return False
    
    def open_app(self, package_name: str) -> bool:
        """
        Open an app on phone.
        
        Args:
            package_name: Android package name (e.g., com.android.chrome)
        """
        if not self.enabled:
            return False
        
        try:
            subprocess.run(["adb", "shell", "monkey", "-p", package_name, "-c", 
                          "android.intent.category.LAUNCHER", "1"])
            print(f"Opened app: {package_name}")
            return True
        except Exception as e:
            print(f"Error opening app on phone: {e}")
            return False
    
    def send_notification(self, title: str, message: str) -> bool:
        """Send a notification to the phone."""
        if not self.enabled:
            return False
        
        try:
            subprocess.run([
                "adb", "shell",
                f"am broadcast -a android.intent.action.VIEW -d '{message}'"
            ])
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False


# Standalone testing
if __name__ == "__main__":
    sys_ctrl = SystemController()
    
    # Test opening browser
    print("\nTesting browser launch...")
    sys_ctrl.open_application("browser")
    
    # Test system info
    print("\nSystem Information:")
    info = sys_ctrl.get_system_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
