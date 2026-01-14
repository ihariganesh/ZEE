"""Workspace context awareness for AI co-worker."""
import os
import subprocess
from typing import Dict, List, Optional

class WorkspaceHelper:
    """Help with workspace and development tasks."""
    
    def __init__(self):
        self.current_dir = os.getcwd()
    
    def get_active_window_info(self) -> Dict:
        """Get information about active window."""
        try:
            # Get active window title (works on Hyprland)
            result = subprocess.run(
                ['hyprctl', 'activewindow', '-j'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                import json
                window_info = json.loads(result.stdout)
                return {
                    "title": window_info.get("title", ""),
                    "class": window_info.get("class", ""),
                    "workspace": window_info.get("workspace", {}).get("id", 0)
                }
        except:
            pass
        
        return {"title": "", "class": "", "workspace": 0}
    
    def is_coding(self) -> bool:
        """Check if user is currently coding."""
        window = self.get_active_window_info()
        coding_apps = ["code", "vscode", "cursor", "vim", "nvim", "intellij", "pycharm"]
        
        return any(app in window["class"].lower() for app in coding_apps)
    
    def get_git_status(self, path: str = ".") -> Optional[str]:
        """Get git repository status."""
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if not output:
                    return "Working tree clean"
                
                lines = output.split('\n')
                modified = len([l for l in lines if l.startswith(' M')])
                untracked = len([l for l in lines if l.startswith('??')])
                
                status = []
                if modified > 0:
                    status.append(f"{modified} modified")
                if untracked > 0:
                    status.append(f"{untracked} untracked")
                
                return ", ".join(status) if status else "Changes detected"
        except:
            pass
        
        return None
    
    def suggest_break(self, work_duration_minutes: int = 60) -> bool:
        """Suggest if user should take a break."""
        # Simple heuristic - can be enhanced with actual time tracking
        return work_duration_minutes >= 60
    
    def get_context_summary(self) -> str:
        """Get current workspace context."""
        window = self.get_active_window_info()
        summary = []
        
        if window["title"]:
            summary.append(f"Working on: {window['title']}")
        
        if self.is_coding():
            git_status = self.get_git_status()
            if git_status:
                summary.append(f"Git: {git_status}")
        
        return " | ".join(summary) if summary else "Ready to assist"
