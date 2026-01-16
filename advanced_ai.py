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
            return "No previous conversation."
        
        context = "Recent conversation:\n"
        for msg in list(self.conversation_history)[-6:]:  # Last 6 messages for better context
            role = "User" if msg["role"] == "user" else "ZEE"
            timestamp = msg.get("timestamp", "")
            # Truncate long messages for context
            content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
            context += f"[{role}]: {content}\n"
        return context
    
    def detect_topic(self, text: str) -> Optional[str]:
        """Detect conversation topic."""
        text_lower = text.lower()
        
        topics = {
            "coding": ["code", "programming", "debug", "error", "function", "python", "javascript", "git", "commit", "repository", "variable", "class", "api"],
            "research": ["research", "search", "find", "learn", "explain", "what is", "how does", "tell me about", "information"],
            "tasks": ["task", "todo", "reminder", "deadline", "meeting", "schedule", "note", "complete"],
            "system": ["open", "close", "volume", "brightness", "wifi", "type", "window", "application"],
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
    
    def generate_smart_response(self, query: str, context: str = None) -> str:
        """Generate contextually aware response."""
        # Improve query understanding first
        improved_query = self.improve_query_understanding(query)
        
        # Add to conversation history
        self.conversation.add_message("user", query)
        self.conversation.update_topic(query)
        
        # Analyze sentiment for empathetic responses
        sentiment = self.analyze_sentiment(query)
        
        # Build context-aware prompt
        context_str = self.conversation.get_context_string()
        topic = self.conversation.current_topic or 'general'
        
        # Enhanced system prompt based on topic
        system_context = self._get_system_context(topic, sentiment)
        
        # Additional context from workspace/tasks if provided
        workspace_context = f"\n\nCurrent Context:\n{context}" if context else ""
        
        enhanced_prompt = f"""{system_context}

Conversation History:
{context_str}

Current Topic: {topic}
User Sentiment: {sentiment}{workspace_context}

User Query: {improved_query}

Provide a natural, conversational response. Keep it concise (2-3 sentences max) unless detailed explanation is needed. Be actionable and specific."""
        
        # Generate response with better parameters
        response = self.research.ai.generate_response(
            enhanced_prompt,
            max_tokens=800  # Increased for better quality
        )
        
        # Filter and improve response quality
        if response:
            response = self._filter_response(response)
            self.conversation.add_message("assistant", response)
            self._learn_from_query(query, response)
        
        return response
    
    def _get_system_context(self, topic: str, sentiment: str) -> str:
        """Get appropriate system context based on topic and sentiment."""
        base_context = "You are ZEE, an intelligent AI co-worker assistant. You are helpful, friendly, and efficient."
        
        topic_contexts = {
            "coding": "You have expertise in software development. Provide practical code examples and best practices. Be technical but clear. Include relevant commands or code snippets.",
            "research": "You excel at finding and explaining information. Provide comprehensive yet digestible answers with key points. Break down complex topics.",
            "tasks": "You help with productivity and task management. Be organized, suggest priorities, and offer actionable steps with time estimates when relevant.",
            "system": "You assist with system operations. Be precise with commands and explain potential impacts. Include safety warnings if needed."
        }
        
        topic_context = topic_contexts.get(topic, "You answer questions clearly and provide useful, accurate information with practical examples.")
        
        sentiment_context = ""
        if sentiment == "urgent":
            sentiment_context = " This is URGENT - prioritize speed and effectiveness. Provide immediate, actionable solutions first, then brief explanations."
        elif sentiment == "negative":
            sentiment_context = " The user is facing an issue - be empathetic, patient, and solution-focused. Acknowledge their frustration and provide step-by-step help."
        elif sentiment == "positive":
            sentiment_context = " The user is satisfied - maintain the positive tone, be encouraging, and offer to help with next steps."
        
        return f"{base_context} {topic_context}{sentiment_context}"
    
    def _filter_response(self, response: str) -> str:
        """Filter and improve response quality."""
        # Remove common AI artifacts
        response = response.strip()
        
        # Remove unnecessary prefixes
        prefixes_to_remove = [
            "As ZEE, ",
            "As an AI assistant, ",
            "As your AI assistant, ",
            "Based on the context, ",
            "Sure! ",
            "Certainly! "
        ]
        
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):]
                break
        
        # Capitalize first letter if needed
        if response and response[0].islower():
            response = response[0].upper() + response[1:]
        
        return response
    
    def _learn_from_query(self, query: str, response: str):
        """Learn from user queries."""
        query_lower = query.lower()
        
        # Track common queries
        if query_lower not in self.learning_data["common_queries"]:
            self.learning_data["common_queries"][query_lower] = {
                "count": 0,
                "topic": self.conversation.current_topic,
                "last_response_length": 0
            }
        
        self.learning_data["common_queries"][query_lower]["count"] += 1
        self.learning_data["common_queries"][query_lower]["last_response_length"] = len(response)
        self.learning_data["common_queries"][query_lower]["topic"] = self.conversation.current_topic
        
        # Track user patterns (time of day, query types)
        current_hour = datetime.now().hour
        time_period = "morning" if 6 <= current_hour < 12 else "afternoon" if 12 <= current_hour < 18 else "evening"
        
        if time_period not in self.learning_data["user_patterns"]:
            self.learning_data["user_patterns"][time_period] = {}
        
        topic = self.conversation.current_topic or "general"
        if topic not in self.learning_data["user_patterns"][time_period]:
            self.learning_data["user_patterns"][time_period][topic] = 0
        self.learning_data["user_patterns"][time_period][topic] += 1
        
        # Save learning data periodically
        if len(self.learning_data["common_queries"]) % 5 == 0:
            self._save_learning_data()
    
    def get_proactive_suggestion(self, context: str = None) -> Optional[str]:
        """Generate proactive suggestions based on context and learning patterns."""
        current_hour = datetime.now().hour
        time_period = "morning" if 6 <= current_hour < 12 else "afternoon" if 12 <= current_hour < 18 else "evening"
        
        # Check user patterns for this time period
        patterns = self.learning_data.get("user_patterns", {}).get(time_period, {})
        common_topic = max(patterns.items(), key=lambda x: x[1])[0] if patterns else None
        
        # Morning suggestions
        if 6 <= current_hour < 12:
            if not self.conversation.conversation_history:
                suggestions = ["Good morning! Would you like your daily briefing?"]
                if common_topic == "coding":
                    suggestions.append("Morning! Ready to check your git status and start coding?")
                return suggestions[0] if not common_topic else suggestions[-1]
        
        # Afternoon productivity check
        elif 14 <= current_hour < 15:
            if common_topic == "tasks":
                return "Afternoon check-in: How are your tasks progressing? Need any help?"
            return "It's afternoon. Time for a quick break or task review?"
        
        # End of day wrap-up
        elif 17 <= current_hour < 18:
            return "End of workday approaching. Should I summarize your completed tasks?"
        
        return None
    
    def improve_query_understanding(self, query: str) -> str:
        """Improve query understanding with context."""
        query_lower = query.lower()
        
        # Get last user and assistant messages for context
        recent_messages = list(self.conversation.conversation_history)[-3:]
        
        # Handle pronouns with context
        pronouns = ['it', 'this', 'that', 'they', 'them', 'those', 'these']
        if any(f' {pronoun} ' in f' {query_lower} ' or query_lower.startswith(f'{pronoun} ') for pronoun in pronouns):
            if self.conversation.current_topic:
                return f"{query} [Context: discussing {self.conversation.current_topic}]"
            elif recent_messages:
                # Add reference to last topic discussed
                last_user_msg = next((msg['content'] for msg in reversed(recent_messages) if msg['role'] == 'user'), None)
                if last_user_msg:
                    return f"{query} [Previous question: {last_user_msg[:100]}]"
        
        # Handle follow-up questions
        followup_starters = ['and', 'also', 'what about', 'how about', 'why', 'can you', 'tell me more']
        if any(query_lower.startswith(starter) for starter in followup_starters):
            if recent_messages:
                last_context = recent_messages[-1]['content'][:150]
                return f"{query} [Continuing from: {last_context}]"
        
        # Handle comparative questions
        if any(word in query_lower for word in ['compare', 'difference', 'versus', 'vs', 'or']):
            return f"{query} [Provide clear comparison with pros/cons]"
        
        # Handle how-to questions
        if query_lower.startswith(('how to', 'how do i', 'how can i')):
            return f"{query} [Provide step-by-step instructions]"
        
        return query
    
    def analyze_sentiment(self, text: str) -> str:
        """Enhanced sentiment analysis."""
        positive_words = ['good', 'great', 'awesome', 'thanks', 'perfect', 'excellent', 'wonderful', 'love', 'amazing', 'fantastic', 'appreciate', 'helpful']
        negative_words = ['bad', 'error', 'problem', 'issue', 'wrong', 'failed', 'broken', 'stuck', 'help', 'confused', 'frustrated', 'not working', 'crash']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Check for urgent/emergency indicators
        if any(word in text_lower for word in ['urgent', 'emergency', 'critical', 'asap', 'immediately']):
            return "urgent"
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        
        return "neutral"
