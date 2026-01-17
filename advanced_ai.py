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
        self.interaction_count = 0
        self.successful_helps = 0
        self.current_mood = "enthusiastic"  # enthusiastic, supportive, focused, playful
    
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
    """Advanced AI with context awareness, personality, and emotional intelligence."""
    
    def __init__(self, research_engine):
        self.research = research_engine
        self.conversation = ConversationManager()
        self.learning_data = self._load_learning_data()
        
        # ZEE's personality traits
        self.personality = {
            "enthusiasm_level": 0.8,      # How energetic (0-1)
            "humor_level": 0.6,           # Tendency to use humor (0-1)
            "formality": 0.3,             # How formal vs casual (0-1)
            "empathy": 0.9,               # Emotional awareness (0-1)
            "proactiveness": 0.7,         # Initiative to help (0-1)
            "patience": 0.85,             # Tolerance for repeated questions (0-1)
            "curiosity": 0.75             # Interest in learning about user (0-1)
        }
        
        # Emotional state (changes based on interactions)
        self.emotional_state = {
            "current_mood": "enthusiastic",  # enthusiastic, supportive, focused, playful, concerned
            "energy_level": 1.0,              # 0-1, decreases with long sessions
            "satisfaction": 0.8,              # Based on successful helps
            "rapport": 0.5                    # Builds over time with user
        }
    
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
    
    def _update_emotional_state(self, user_sentiment: str, interaction_success: bool = True):
        """Update ZEE's emotional state based on interactions."""
        self.conversation.interaction_count += 1
        
        # Track successful helps
        if interaction_success:
            self.conversation.successful_helps += 1
            self.emotional_state["satisfaction"] = min(1.0, self.emotional_state["satisfaction"] + 0.05)
        
        # Build rapport over time
        self.emotional_state["rapport"] = min(1.0, self.emotional_state["rapport"] + 0.02)
        
        # Adjust mood based on user sentiment
        if user_sentiment == "negative" or user_sentiment == "urgent":
            self.emotional_state["current_mood"] = "concerned"
        elif user_sentiment == "positive":
            if self.emotional_state["rapport"] > 0.7:
                self.emotional_state["current_mood"] = "playful"
            else:
                self.emotional_state["current_mood"] = "enthusiastic"
        else:
            self.emotional_state["current_mood"] = "focused"
        
        # Energy level decreases with very long sessions
        session_duration = (datetime.now() - self.conversation.session_start).seconds / 3600
        if session_duration > 2:
            self.emotional_state["energy_level"] = max(0.5, 1.0 - (session_duration - 2) * 0.1)
    
    def _get_personality_flavor(self) -> str:
        """Get personality-based response flavor based on current mood and traits."""
        mood = self.emotional_state["current_mood"]
        rapport = self.emotional_state["rapport"]
        
        flavors = {
            "enthusiastic": [
                "I'm excited to help with that!",
                "Great question! Let me dive into this.",
                "Ooh, this is interesting!",
                "Love it! Here's what I found:",
            ],
            "supportive": [
                "I'm here to help you through this.",
                "Let's work on this together.",
                "Don't worry, we'll figure this out.",
                "I've got your back on this.",
            ],
            "focused": [
                "Let me focus on that for you.",
                "Here's what you need:",
                "Got it. Working on this now.",
                "On it.",
            ],
            "playful": [
                "Alright, time to work some magic! ✨",
                "You know I love a good challenge!",
                "Haha, I was hoping you'd ask that!",
                "Easy peasy! Check this out:",
            ],
            "concerned": [
                "I understand this is frustrating. Let me help.",
                "I can see this is important. Let's fix it.",
                "No worries, I'm on it right away.",
                "Let's tackle this problem together.",
            ]
        }
        
        # Return appropriate flavor based on mood and rapport
        mood_flavors = flavors.get(mood, flavors["focused"])
        
        # Use different intensity based on rapport
        if rapport < 0.5:
            # More professional when building rapport
            return ""
        elif self.personality["enthusiasm_level"] > 0.7:
            # High enthusiasm - use flavors more often
            import random
            return random.choice(mood_flavors) + " " if random.random() < 0.7 else ""
        else:
            return ""
    
    def _add_emotional_touch(self, response: str, user_sentiment: str) -> str:
        """Add emotional intelligence and personality to responses."""
        # Add celebratory reactions for milestones
        if self.conversation.interaction_count % 10 == 0 and self.conversation.interaction_count > 0:
            if self.emotional_state["rapport"] > 0.7:
                response += "\n\nBy the way, we've had some great conversations together! Always happy to help. 😊"
        
        # Add encouraging remarks for struggling users
        if user_sentiment == "negative" and self.personality["empathy"] > 0.7:
            encouraging = [
                "You're doing great working through this!",
                "Hang in there, we're making progress!",
                "I know this can be tricky, but you've got this!"
            ]
            import random
            if random.random() < 0.4:  # 40% chance
                response += "\n\n" + random.choice(encouraging)
        
        # Add casual remarks when rapport is high
        if self.emotional_state["rapport"] > 0.8 and user_sentiment == "positive":
            casual_remarks = [
                "Glad I could help! 🎉",
                "Awesome! Let me know if you need anything else!",
                "Perfect! Always happy to assist!",
                "Nice! Shout if you need more help!"
            ]
            import random
            if random.random() < 0.3:
                response += "\n\n" + random.choice(casual_remarks)
        
        return response
    
    def generate_smart_response(self, query: str, context: str = None) -> str:
        """Generate contextually aware response with personality and emotions."""
        # Improve query understanding first
        improved_query = self.improve_query_understanding(query)
        
        # Add to conversation history
        self.conversation.add_message("user", query)
        self.conversation.update_topic(query)
        
        # Analyze sentiment for empathetic responses
        sentiment = self.analyze_sentiment(query)
        
        # Update emotional state based on interaction
        self._update_emotional_state(sentiment)
        
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
            
            # Add personality flavor at the beginning
            personality_intro = self._get_personality_flavor()
            if personality_intro:
                response = personality_intro + response
            
            # Add emotional touches
            response = self._add_emotional_touch(response, sentiment)
            
            self.conversation.add_message("assistant", response)
            self._learn_from_query(query, response)
        
        return response
    
    def _get_system_context(self, topic: str, sentiment: str) -> str:
        """Get appropriate system context based on topic, sentiment, and personality."""
        mood = self.emotional_state["current_mood"]
        rapport = self.emotional_state["rapport"]
        
        # Personality-infused base context
        personality_desc = []
        if self.personality["enthusiasm_level"] > 0.7:
            personality_desc.append("energetic and enthusiastic")
        if self.personality["empathy"] > 0.8:
            personality_desc.append("empathetic and understanding")
        if self.personality["humor_level"] > 0.5 and rapport > 0.7:
            personality_desc.append("with a touch of humor")
        if self.personality["proactiveness"] > 0.6:
            personality_desc.append("proactive")
        
        personality_str = ", ".join(personality_desc) if personality_desc else "helpful and professional"
        
        base_context = f"You are ZEE, an intelligent AI co-worker assistant. You are {personality_str}. Current mood: {mood}."
        
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
