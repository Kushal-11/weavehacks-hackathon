from crewai.tools import BaseTool
import requests
from typing import List, Dict
import os
from pydantic import Field

class ImgflipTool(BaseTool):
    name: str = "Imgflip Template Tool"
    description: str = "Fetch meme templates from Imgflip database"
    base_url: str = "https://api.imgflip.com/get_memes"
    
    def _run(self, search_query: str = None) -> List[Dict]:
        """Fetch popular meme templates, optionally filtered by search"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                return []
                
            templates = data["data"]["memes"]
            
            if search_query:
                # Filter templates by name matching search query
                templates = [t for t in templates if search_query.lower() in t["name"].lower()]
            
            # Return top 20 most popular
            return templates[:20]
        except requests.RequestException as e:
            return []
    
    async def get_popular_templates(self) -> List[Dict]:
        """Get the most popular meme templates"""
        return self._run()
    
    async def search_templates(self, query: str) -> List[Dict]:
        """Search for templates by name"""
        return self._run(query)
    
    async def get_template_by_id(self, template_id: str) -> Dict:
        """Get specific template by ID"""
        try:
            response = requests.get(f"https://api.imgflip.com/get_memes")
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                templates = data["data"]["memes"]
                for template in templates:
                    if template["id"] == template_id:
                        return template
            
            return {}
        except requests.RequestException:
            return {} 