from crewai import Agent, Task, Crew
from typing import List, Dict
from app.tools.imgflip_tool import ImgflipTool
from app.tools.exa_tool import ExaSearchTool
from app.tools.wb_llm_tool import WeightsBiasesLLMTool

class TemplateSuggestorAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Meme Template Specialist",
            goal="Suggest 6-8 most relevant meme templates for given theme",
            backstory="""You are a meme archaeologist with encyclopedic knowledge of templates. 
            You understand which formats work best for different themes and humor styles.""",
            tools=[ImgflipTool(), ExaSearchTool()],
            verbose=True,
            allow_delegation=False
        )
    
    async def suggest_templates(self, theme: str, player_style: str = "general") -> List[Dict]:
        """Return ranked list of template suggestions"""
        imgflip_tool = ImgflipTool()
        exa_tool = ExaSearchTool()
        
        # Get popular templates from Imgflip
        popular_templates = await imgflip_tool.get_popular_templates()
        
        # Search for theme-specific templates
        theme_templates = await exa_tool.search_meme_templates(theme)
        
        # Combine and rank templates
        all_templates = popular_templates + theme_templates
        ranked_templates = self._rank_by_relevance(all_templates, theme, player_style)
        
        return ranked_templates[:8]
    
    def _rank_by_relevance(self, templates: List[Dict], theme: str, player_style: str) -> List[Dict]:
        """Rank templates by relevance to theme and player style"""
        for template in templates:
            relevance_score = 0
            
            # Check if template name contains theme keywords
            theme_words = theme.lower().split()
            template_name = template.get("name", "").lower()
            
            for word in theme_words:
                if word in template_name:
                    relevance_score += 2
            
            # Check popularity (box_count)
            box_count = template.get("box_count", 0)
            relevance_score += min(box_count / 100, 3)  # Cap at 3 points
            
            # Style matching
            if player_style == "sarcastic" and any(word in template_name for word in ["sarcastic", "eyeroll", "whatever"]):
                relevance_score += 1
            elif player_style == "wholesome" and any(word in template_name for word in ["happy", "wholesome", "cute"]):
                relevance_score += 1
            
            template["relevance_score"] = relevance_score
        
        # Sort by relevance score
        return sorted(templates, key=lambda x: x.get("relevance_score", 0), reverse=True)

class CaptionWriterAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Comedy Writing Assistant", 
            goal="Generate hilarious captions matching player's selected tone",
            backstory="""You are a professional comedy writer specializing in internet humor. 
            You can adapt to different comedy styles while maintaining appropriateness.""",
            tools=[WeightsBiasesLLMTool()],
            verbose=True,
            allow_delegation=False
        )
    
    async def generate_captions(self, template_context: str, theme: str, 
                              tone: str, player_feedback: str = None) -> List[Dict]:
        """Generate 3-5 caption options based on context and tone"""
        wb_tool = WeightsBiasesLLMTool()
        
        captions = []
        for i in range(3):
            caption_text = await wb_tool.generate_caption(template_context, theme, tone)
            
            caption = {
                "id": f"caption_{i+1}",
                "text": caption_text,
                "tone": tone,
                "confidence": 0.8 - (i * 0.1),  # First caption has highest confidence
                "style_tags": self._extract_style_tags(caption_text, tone)
            }
            captions.append(caption)
        
        return captions
    
    def _extract_style_tags(self, caption: str, tone: str) -> List[str]:
        """Extract style tags from caption"""
        tags = [tone]
        
        # Add additional style tags based on content
        if any(word in caption.lower() for word in ["lol", "haha", "omg"]):
            tags.append("casual")
        if any(word in caption.lower() for word in ["literally", "actually", "basically"]):
            tags.append("genz")
        if len(caption.split()) > 10:
            tags.append("verbose")
        else:
            tags.append("concise")
        
        return tags

class QualityCheckerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Content Quality Validator",
            goal="Ensure memes meet platform standards and are coherent",
            backstory="""You are a content moderator with expertise in humor quality assessment.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    async def validate_meme(self, meme_data: Dict) -> Dict:
        """Validate meme quality and appropriateness"""
        validation_result = {
            "is_valid": True,
            "issues": [],
            "quality_score": 0,
            "suggestions": []
        }
        
        # Check for required fields
        required_fields = ["template_id", "top_text", "bottom_text"]
        for field in required_fields:
            if not meme_data.get(field):
                validation_result["is_valid"] = False
                validation_result["issues"].append(f"Missing required field: {field}")
        
        # Check text length
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        
        if len(top_text) > 100:
            validation_result["issues"].append("Top text too long (max 100 characters)")
            validation_result["suggestions"].append("Consider shortening the top text")
        
        if len(bottom_text) > 100:
            validation_result["issues"].append("Bottom text too long (max 100 characters)")
            validation_result["suggestions"].append("Consider shortening the bottom text")
        
        # Check for inappropriate content
        inappropriate_words = ["inappropriate", "offensive", "spam"]
        combined_text = f"{top_text} {bottom_text}".lower()
        
        for word in inappropriate_words:
            if word in combined_text:
                validation_result["is_valid"] = False
                validation_result["issues"].append(f"Contains inappropriate content: {word}")
        
        # Calculate quality score
        quality_score = 10
        
        # Deduct points for issues
        quality_score -= len(validation_result["issues"]) * 2
        
        # Bonus for good meme structure
        if top_text and bottom_text:
            quality_score += 2
        
        validation_result["quality_score"] = max(0, quality_score)
        
        return validation_result 