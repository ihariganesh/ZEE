"""Advanced AI conversation manager with context and memory."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque

class ConversationManager:
    """Manage conversation context and history."""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversation_history = deque(maxlen=max_history)
        self.current_topic = None
        self.user_preferences = {}
        self.session_start = datetime.now()
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
    
    def get_context(self) -> List[Dict]:
        """Get recent conversation context."""
        return list(self.conversation_history)
    
    def get_context_string(self) -> str:
        """Get context as formatted string for AI."""
        if not self.conversation_history:
            return ""
        
        context = "Recent conversation:\n"
        for msg in list(self.conversation_history)[-5:]:  # Last 5 messages
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        return context
    
    def detect_topic(self, text: str) -> Optional[str]:
        """Detect conversation topic."""
        text_lower = text.lower()
        
        topics = {
            "coding": ["code", "programming", "debug", "error", "function", "python", "javascript"],
            "research": ["research", "search", "find", "learn", "explain", "what is"],
            "tasks": ["task", "todo", "reminder", "deadline", "meeting"],
            "system": ["open", "close", "volume", "brightness", "wifi"],
        }
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return None
    
    def update_topic(self, text: str):
        """Update current conversation topic."""
        topic = self.detect_topic(text)
        if topic:
            self.current_topic = topic
    
    def clear_context(self):
        """Clear conversation history."""
        self.conversation_history.clear()
        self.current_topic = None


class AdvancedAI:
    """Advanced AI with context awareness and smart responses."""
    
    def __init__(self, research_engine):
        self.research = research_engine
        self.conversation = ConversationManager()
        self.learning_data = self._load_learning_data()
    
    def _load_learning_data(self) -> Dict:
        """Load AI learning data."""
        file_path = "ai_learning.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "common_queries": {},
            "user_patterns": {},
            "feedback": []
        }
    
    def _save_learning_data(self):
        """Save AI learning data."""
        try:
            with open("ai_learning.json", 'w') as f:
                json.dump(self.learning_data, f, indent=2)
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def generate_smart_response(self, query: str, context: Dict = None) -> str:
        """Generate contextually aware response."""
        # Add to conversation history
        self.conversation.add_message("user", query)
        self.conversation.update_topic(query)
        
        # Build context-aware prompt
        context_str = self.conversation.get_context_string()
        
        enhanced_prompt = f"""You are ZEE, an intelligent AI co-worker assistant. 
Be helpful, concise, and proactive. Provide actionable insights.

{context_str}

Current topic: {self.conversation.current_topic or 'general'}

User query: {query}

Respond naturally and helpfully. If this relates to previous messages, acknowledge that context."""
        
        # Generate response with context
        response = self.research.ai.generate_response(enhanced_prompt)
        
        # Add response to history
        if response:
            self.conversation.add_message("assistant", response)
            
            # Learn from interaction
            self._learn_from_query(query, response)
        
        return response
    
    def _learn_from_query(self, query: str, response: str):
        """Learn from user queries."""
        query_lower = query.lower()
        
        # Track common queries
        if query_lower not in self.learning_data["common_queries"]:
            self.learning_data["common_queries"][query_lower] = 0
        self.learning_data["common_queries"][query_lower] += 1
        
        # Save learning data periodically
        if len(self.learning_data["common_queries"]) % 10 == 0:
            self._save_learning_data()
    
    def get_proactive_suggestion(self, context: Dict = None) -> Optional[str]:
        """Generate proactive suggestions based on context."""
        current_hour = datetime.now().hour
        
        # Morning suggestions
        if 6 <= current_hour < 12:
            if not self.conversation.conversation_history:
                return "Good morning! Would you like your daily briefing?"
        
        # Afternoon productivity check
        elif 14 <= current_hour < 15:
            return "It's afternoon. Time for a quick break or task review?"
        
        # End of day wrap-up
        elif 17 <= current_hour < 18:
            return "End of workday approaching. Should I summarize your completed tasks?"
        
        return None
    
    def improve_query_understanding(self, query: str) -> str:
        """Improve query understanding with context."""
        query_lower = query.lower()
        
        # Handle pronouns with context
        if any(word in query_lower for word in ['it', 'this', 'that']) and self.conversation.current_topic:
            # Add topic context to query
            return f"{query} (regarding {self.conversation.current_topic})"
        
        # Handle follow-up questions
        if query_lower.startswith(('and', 'also', 'what about', 'how about')):
            context = self.conversation.get_context_string()
            return f"{query}\n\nContext: {context}"
        
        return query
    
    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis."""
        positive_words = ['good', 'great', 'awesome', 'thanks', 'perfect', 'excellent']
        negative_words = ['bad', 'error', 'problem', 'issue', 'wrong', 'failed']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in positive_words):
            return "positive"
        elif any(word in text_lower for word in negative_words):
            return "negative"
        
        return "neutral"
