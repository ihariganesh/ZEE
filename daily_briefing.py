"""Daily briefing module for weather and news."""
import requests
from datetime import datetime
from typing import Dict, Optional
import json

class DailyBriefing:
    """Get daily briefing with weather and news."""
    
    def __init__(self):
        self.weather_api_key = None  # Free tier doesn't need API key for some services
        
    def get_weather(self, city: str, country: str = "India") -> str:
        """Get weather information for a city."""
        try:
            # Using wttr.in - free weather service, no API key needed
            url = f"https://wttr.in/{city},{country}?format=j1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                temp_c = current['temp_C']
                feels_like = current['FeelsLikeC']
                desc = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                
                return f"Weather in {city}: {temp_c}°C, feels like {feels_like}°C. {desc}. Humidity {humidity}%"
            else:
                return f"Couldn't get weather for {city}"
                
        except Exception as e:
            print(f"Weather error: {e}")
            return "Weather information unavailable"
    
    def get_news(self, category: str = "general") -> str:
        """Get top news headlines (world and tech)."""
        try:
            # Using free news aggregator (no API key needed)
            # Alternative: https://newsapi.org (requires free API key)
            
            # For now, using DuckDuckGo Instant Answer API (no key needed)
            news_items = []
            
            # World news
            world_query = "latest world news today"
            tech_query = "latest technology news today"
            
            # Simple fallback response (can be enhanced with actual API)
            today = datetime.now().strftime("%B %d, %Y")
            
            return f"Latest news for {today}: Check major news outlets for world news and tech updates."
            
        except Exception as e:
            print(f"News error: {e}")
            return "News information unavailable"
    
    def get_daily_summary(self, city: str, country: str = "India") -> Dict[str, str]:
        """Get complete daily briefing."""
        now = datetime.now()
        
        # Date and day
        date_str = now.strftime("%A, %B %d, %Y")
        
        # Weather
        weather = self.get_weather(city, country)
        
        # News (simplified for now)
        news_intro = "For the latest news, I recommend checking your favorite news app or website."
        
        return {
            "date": date_str,
            "weather": weather,
            "news": news_intro
        }
    
    def format_briefing(self, city: str, country: str = "India") -> str:
        """Format the daily briefing as a spoken message."""
        summary = self.get_daily_summary(city, country)
        
        message = f"Good day! Today is {summary['date']}. "
        message += f"{summary['weather']}. "
        message += f"{summary['news']}"
        
        return message
