"""Research and AI integration module using FREE APIs."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
from config import Config


class ResearchAssistant:
    """Handles web research using FREE search."""
    
    def __init__(self):
        """Initialize research assistant."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        print("✅ Research Assistant initialized")
    
    def search_web(self, query: str, num_results: int = None) -> List[Dict[str, str]]:
        """
        Search the web using FREE DuckDuckGo (no API key needed).
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, and snippet
        """
        if num_results is None:
            num_results = Config.MAX_SEARCH_RESULTS
        
        try:
            from duckduckgo_search import DDGS
            
            results = []
            print(f"🔍 Searching for: {query}")
            
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=num_results)
                
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', result.get('link', '')),
                        'snippet': result.get('body', result.get('description', ''))
                    })
            
            print(f"✅ Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Error searching web: {e}")
            return []
    
    def fetch_webpage_content(self, url: str) -> Optional[str]:
        """
        Fetch and extract main content from a webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            Main text content of the page
        """
        try:
            print(f"📄 Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Return first 5000 characters
            
        except Exception as e:
            print(f"❌ Error fetching webpage: {e}")
            return None
    
    def summarize_search_results(self, results: List[Dict[str, str]]) -> str:
        """Create a summary of search results."""
        if not results:
            return "No results found."
        
        summary = f"I found {len(results)} results:\n\n"
        
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   URL: {result['url']}\n"
            if result['snippet']:
                summary += f"   {result['snippet'][:150]}...\n"
            summary += "\n"
        
        return summary


class AIProcessor:
    """Processes information using FREE AI APIs (Groq + Ollama)."""
    
    def __init__(self):
        """Initialize AI processor with FREE tools."""
        self.groq_available = bool(Config.GROQ_API_KEY)
        self.ollama_available = False
        
        # Setup Groq (FREE & Fast)
        if self.groq_available:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
                print("✅ Groq API initialized (FREE & Fast)")
            except Exception as e:
                print(f"⚠️  Groq initialization error: {e}")
                self.groq_available = False
        
        # Setup Ollama (FREE & Offline)
        if Config.USE_OLLAMA_OFFLINE:
            try:
                import ollama
                # Test connection
                ollama.list()
                self.ollama_available = True
                print("✅ Ollama initialized (FREE & Offline)")
            except Exception as e:
                print(f"⚠️  Ollama not available: {e}")
                print("   Install from: https://ollama.ai")
        
        if not self.groq_available and not self.ollama_available:
            print("⚠️  No AI models available!")
            print("   Option 1: Get FREE Groq API key from https://console.groq.com")
            print("   Option 2: Install Ollama from https://ollama.ai")
    
    def generate_response(self, prompt: str, context: str = "", max_tokens: int = 500) -> Optional[str]:
        """
        Generate an AI response using FREE APIs.
        
        Args:
            prompt: User prompt
            context: Additional context
            max_tokens: Maximum response length
            
        Returns:
            AI-generated response
        """
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        # Try Groq first (FREE & Fast)
        if self.groq_available:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Fast & free
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that provides clear, concise answers."},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
            except Exception as e:
                print(f"⚠️  Groq error: {e}")
        
        # Fallback to Ollama (FREE & Offline)
        if self.ollama_available:
            try:
                import ollama
                response = ollama.chat(
                    model="llama3.2",  # Use llama3.2, mistral, or phi3
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that provides clear, concise answers."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                return response['message']['content']
                
            except Exception as e:
                print(f"⚠️  Ollama error: {e}")
                print("   Try: ollama pull llama3.2")
        
        return None
    
    def summarize_content(self, content: str, max_length: int = 300) -> Optional[str]:
        """Summarize content using FREE AI."""
        prompt = f"Please provide a concise summary of the following content in about {max_length} words:\n\n{content}"
        return self.generate_response(prompt, max_tokens=400)
    
    def answer_question(self, question: str, research_results: List[Dict[str, str]]) -> Optional[str]:
        """Answer a question based on research results using FREE AI."""
        # Build context from research results
        context = "Based on the following search results:\n\n"
        for i, result in enumerate(research_results[:3], 1):  # Use top 3 results
            context += f"{i}. {result['title']}\n{result['snippet']}\n\n"
        
        prompt = f"Question: {question}\n\nPlease provide a clear, accurate answer based on the information above. Keep it concise."
        
        return self.generate_response(prompt, context, max_tokens=500)


class ResearchEngine:
    """Main research engine combining FREE search + FREE AI."""
    
    def __init__(self):
        """Initialize research engine with FREE tools."""
        self.researcher = ResearchAssistant()
        self.ai = AIProcessor()
        print("✅ Research Engine ready!\n")
    
    def research_and_explain(self, topic: str) -> Dict[str, any]:
        """
        Research a topic and provide an explanation using FREE tools.
        
        Args:
            topic: Topic to research
            
        Returns:
            Dictionary with research results and explanation
        """
        print(f"\n{'='*60}")
        print(f"📚 Researching: {topic}")
        print(f"{'='*60}\n")
        
        # Search for information (FREE)
        results = self.researcher.search_web(topic)
        
        if not results:
            return {
                'success': False,
                'message': 'No search results found',
                'results': [],
                'explanation': None
            }
        
        # Generate summary
        summary = self.researcher.summarize_search_results(results)
        print(summary)
        
        # Generate AI explanation (FREE)
        explanation = None
        if self.ai.groq_available or self.ai.ollama_available:
            print("\n🤖 Generating AI explanation...")
            explanation = self.ai.answer_question(
                f"Explain {topic} in simple terms",
                results
            )
        
        return {
            'success': True,
            'results': results,
            'summary': summary,
            'explanation': explanation
        }


# Standalone testing
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Research Engine with FREE Tools")
    print("="*60 + "\n")
    
    engine = ResearchEngine()
    
    # Test research
    test_topic = "What is artificial intelligence?"
    result = engine.research_and_explain(test_topic)
    
    if result['success']:
        print(f"\n{'='*60}")
        print("RESEARCH SUMMARY:")
        print(f"{'='*60}")
        print(result['summary'])
        
        if result['explanation']:
            print(f"\n{'='*60}")
            print("AI EXPLANATION:")
            print(f"{'='*60}")
            print(result['explanation'])
