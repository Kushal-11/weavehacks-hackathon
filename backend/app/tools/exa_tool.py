from crewai.tools import BaseTool
from typing import List, Dict, Optional, Any
import os
from app.config import settings
from pydantic import Field

try:
    from exa_py import Exa
    EXA_INSTALLED = True
except ImportError:
    EXA_INSTALLED = False
    Exa = None

class ExaSearchTool(BaseTool):
    name: str = "Exa Search Tool"
    description: str = "Search for trending topics, meme templates, and cultural context"
    api_key: str = Field(default_factory=lambda: settings.EXA_API_KEY)
    exa_client: Optional[Any] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not EXA_INSTALLED:
            raise ImportError("exa_py is not installed. Run: pip install exa_py")
        
        if self.api_key and self.api_key != "your_exa_api_key_here":
            self.exa_client = Exa(api_key=self.api_key)
        else:
            self.exa_client = None
    
    def _run(self, query: str, search_type: str = "trending") -> Dict:
        """Search Exa.ai for content based on query"""
        if not self.exa_client:
            return {"error": "Exa client not initialized", "results": []}
        
        try:
            if search_type == "templates":
                # Search for meme templates
                search_query = f"meme template {query} site:imgflip.com OR site:knowyourmeme.com"
            elif search_type == "trending":
                # Search for trending topics
                search_query = f"trending {query} 2024 2025"
            elif search_type == "context":
                # Search for cultural context
                search_query = f"{query} meaning context meme culture"
            else:
                search_query = query
            
            # Use exa_py to search with content
            result = self.exa_client.search_and_contents(
                search_query,
                text=True,
                num_results=10
            )
            
            return {
                "results": result.results if hasattr(result, 'results') else [],
                "content": result.content if hasattr(result, 'content') else []
            }
            
        except Exception as e:
            return {"error": f"Exa API request failed: {str(e)}", "results": []}
    
    async def search_trending_topics(self, category: str = "general") -> List[Dict]:
        """Search for trending topics in a category"""
        result = self._run(f"trending {category} topics 2024", "trending")
        return result.get("results", [])
    
    async def search_meme_templates(self, theme: str) -> List[Dict]:
        """Search for meme templates related to a theme"""
        result = self._run(theme, "templates")
        return result.get("results", [])
    
    async def get_cultural_context(self, topic: str) -> Dict:
        """Get cultural context for a topic"""
        result = self._run(topic, "context")
        return result
    
    async def search_meme_templates_with_images(self, query: str) -> List[Dict]:
        """Search for meme templates with image URLs"""
        if not self.exa_client:
            return []
        
        try:
            # Search for meme templates with image content
            search_query = f"meme template {query} imgflip knowyourmeme"
            result = self.exa_client.search_and_contents(
                search_query,
                text=True,
                num_results=20
            )
            
            templates = []
            for item in result.results:
                template = {
                    "id": item.id if hasattr(item, 'id') else str(hash(item.url)),
                    "name": item.title if hasattr(item, 'title') else "Meme Template",
                    "url": item.url if hasattr(item, 'url') else "",
                    "description": item.text if hasattr(item, 'text') else "",
                    "image_url": item.url if hasattr(item, 'url') else "",
                    "source": "exa_search"
                }
                templates.append(template)
            
            return templates
            
        except Exception as e:
            print(f"Error searching meme templates: {e}")
            return [] 