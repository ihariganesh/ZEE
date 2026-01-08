"""User profile and personalization module."""
import json
import os
from datetime import datetime
from typing import Optional


class UserProfile:
    """Manages user profile and personalization."""
    
    def __init__(self, profile_file: str = "user_profile.json"):
        """Initialize user profile."""
        self.profile_file = profile_file
        self.profile = self._load_profile()
    
    def _load_profile(self) -> dict:
        """Load user profile from file."""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Could not load profile: {e}")
        
        # Default profile
        return {
            "name": None,
            "first_use": datetime.now().isoformat(),
            "last_use": None,
            "preferences": {},
            "interaction_count": 0
        }
    
    def _save_profile(self):
        """Save user profile to file."""
        try:
            with open(self.profile_file, 'w') as f:
                json.dump(self.profile, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save profile: {e}")
    
    def get_name(self) -> Optional[str]:
        """Get user's name."""
        return self.profile.get("name")
    
    def set_name(self, name: str):
        """Set user's name."""
        self.profile["name"] = name
        self._save_profile()
        print(f"✅ Remembered your name: {name}")
    
    def has_name(self) -> bool:
        """Check if user has set their name."""
        return self.profile.get("name") is not None
    
    def update_last_use(self):
        """Update last use timestamp."""
        self.profile["last_use"] = datetime.now().isoformat()
        self.profile["interaction_count"] = self.profile.get("interaction_count", 0) + 1
        self._save_profile()
    
    def get_greeting(self) -> str:
        """Get personalized greeting."""
        name = self.get_name()
        if name:
            return f"Hi {name}! I'm ready for today's tasks."
        return "Hi there! What's your name?"
    
    def is_first_time(self) -> bool:
        """Check if this is user's first time."""
        return self.profile.get("interaction_count", 0) == 0
