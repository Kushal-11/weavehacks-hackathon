from crewai import Agent, Task, Crew
from typing import List, Dict
from app.tools.exa_tool import ExaSearchTool
from app.tools.wb_llm_tool import WeightsBiasesLLMTool

class ThemeGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Creative Theme Curator",
            goal="Generate 3 engaging and meme-worthy themes for each game round",
            backstory="""You are a cultural trend expert with deep knowledge of internet culture. 
            You understand what topics generate the best memes and can identify themes that are 
            current, relatable, and conducive to creative humor.""",
            tools=[ExaSearchTool(), WeightsBiasesLLMTool()],
            verbose=True,
            allow_delegation=False
        )
    
    async def generate_themes(self, difficulty_level: str = "medium") -> List[Dict]:
        """Generate 3 themes for the game rounds"""
        # Use Exa.ai to find trending topics
        exa_tool = ExaSearchTool()
        trending_results = await exa_tool.search_trending_topics("general")
        
        # Generate themes based on trending topics
        themes = []
        for i, topic in enumerate(trending_results[:3]):
            theme = {
                "id": f"theme_{i+1}",
                "name": topic.get("title", f"Trending Topic {i+1}"),
                "description": topic.get("text", ""),
                "difficulty": difficulty_level,
                "category": "trending"
            }
            themes.append(theme)
        
        return themes

class ThemeContextAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Cultural Context Researcher",
            goal="Provide rich context and background for selected themes",
            backstory="""You are a cultural anthropologist who provides context that helps 
            players understand themes deeply and create more meaningful memes.""",
            tools=[ExaSearchTool(), WeightsBiasesLLMTool()],
            verbose=True,
            allow_delegation=False
        )
    
    async def enrich_theme_context(self, theme: Dict) -> Dict:
        """Add cultural context to a theme"""
        exa_tool = ExaSearchTool()
        context_data = await exa_tool.get_cultural_context(theme["name"])
        
        enriched_theme = theme.copy()
        enriched_theme["context"] = context_data.get("results", [])
        enriched_theme["meme_potential"] = self._assess_meme_potential(theme["name"])
        
        return enriched_theme
    
    def _assess_meme_potential(self, theme_name: str) -> Dict:
        """Assess the meme potential of a theme"""
        # Simple heuristic for meme potential
        meme_keywords = ["viral", "trending", "controversial", "relatable", "funny", "absurd"]
        potential_score = 0
        
        for keyword in meme_keywords:
            if keyword.lower() in theme_name.lower():
                potential_score += 1
        
        return {
            "score": min(potential_score, 5),
            "max_score": 5,
            "factors": ["trending", "relatable", "controversial", "funny", "viral"]
        } 