"""Task and reminder management for AI co-worker functionality."""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class TaskManager:
    """Manage tasks, reminders, and to-dos."""
    
    def __init__(self, tasks_file: str = "tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict:
        """Load tasks from file."""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"tasks": [], "reminders": [], "notes": []}
    
    def _save_tasks(self):
        """Save tasks to file."""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, description: str, priority: str = "normal") -> str:
        """Add a new task."""
        task = {
            "id": len(self.tasks["tasks"]) + 1,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created": datetime.now().isoformat(),
            "completed": None
        }
        self.tasks["tasks"].append(task)
        self._save_tasks()
        return f"Task added: {description}"
    
    def complete_task(self, task_id: int) -> str:
        """Mark task as complete."""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
                self._save_tasks()
                return f"Completed: {task['description']}"
        return "Task not found"
    
    def list_tasks(self, status: str = "pending") -> List[Dict]:
        """List tasks by status."""
        return [t for t in self.tasks["tasks"] if t["status"] == status]
    
    def add_note(self, content: str) -> str:
        """Add a quick note."""
        note = {
            "id": len(self.tasks["notes"]) + 1,
            "content": content,
            "created": datetime.now().isoformat()
        }
        self.tasks["notes"].append(note)
        self._save_tasks()
        return "Note saved"
    
    def get_summary(self) -> str:
        """Get task summary."""
        pending = len([t for t in self.tasks["tasks"] if t["status"] == "pending"])
        completed = len([t for t in self.tasks["tasks"] if t["status"] == "completed"])
        
        if pending == 0:
            return "You have no pending tasks. Great job!"
        
        summary = f"You have {pending} pending task"
        if pending != 1:
            summary += "s"
        
        if completed > 0:
            summary += f" and {completed} completed"
        
        # List top 3 pending tasks
        pending_tasks = self.list_tasks("pending")[:3]
        if pending_tasks:
            summary += ". Top tasks: "
            summary += ", ".join([t["description"] for t in pending_tasks])
        
        return summary
