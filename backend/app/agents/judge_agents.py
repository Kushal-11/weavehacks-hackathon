from crewai import Agent, Task, Crew
from typing import List, Dict
from app.tools.wb_llm_tool import WeightsBiasesLLMTool

class HumorJudgeAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Comedy Evaluation Expert",
            goal="Score memes on humor quality with consistent criteria", 
            backstory="""You are a comedy critic who understands humor theory and can 
            objectively assess comedic effectiveness.""",
            tools=[WeightsBiasesLLMTool()],
            verbose=True,
            allow_delegation=False
        )
    
    async def score_humor(self, meme_data: Dict) -> Dict:
        """Return humor score breakdown (0-10 total)"""
        scoring_criteria = {
            "setup_punchline": {"weight": 0.3, "max": 3},
            "timing_delivery": {"weight": 0.3, "max": 3}, 
            "surprise_factor": {"weight": 0.2, "max": 2},
            "wordplay_cleverness": {"weight": 0.2, "max": 2}
        }
        
        # Analyze meme content
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        template_name = meme_data.get("template_name", "")
        
        scores = {}
        total_score = 0
        
        # Setup-Punchline (0-3 points)
        setup_score = self._evaluate_setup_punchline(top_text, bottom_text)
        scores["setup_punchline"] = setup_score
        total_score += setup_score
        
        # Timing-Delivery (0-3 points)
        timing_score = self._evaluate_timing_delivery(top_text, bottom_text, template_name)
        scores["timing_delivery"] = timing_score
        total_score += timing_score
        
        # Surprise Factor (0-2 points)
        surprise_score = self._evaluate_surprise_factor(top_text, bottom_text)
        scores["surprise_factor"] = surprise_score
        total_score += surprise_score
        
        # Wordplay-Cleverness (0-2 points)
        cleverness_score = self._evaluate_wordplay_cleverness(top_text, bottom_text)
        scores["wordplay_cleverness"] = cleverness_score
        total_score += cleverness_score
        
        return {
            "total_score": total_score,
            "max_score": 10,
            "breakdown": scores,
            "feedback": self._generate_humor_feedback(scores, total_score)
        }
    
    def _evaluate_setup_punchline(self, top_text: str, bottom_text: str) -> float:
        """Evaluate setup-punchline structure (0-3 points)"""
        score = 0
        
        # Check if there's a clear setup and punchline
        if top_text and bottom_text:
            score += 1.5
        
        # Check for contrast between setup and punchline
        if top_text and bottom_text and len(top_text) > len(bottom_text):
            score += 0.5
        
        # Check for unexpected twist
        if "but" in bottom_text.lower() or "however" in bottom_text.lower():
            score += 1
        
        return min(score, 3)
    
    def _evaluate_timing_delivery(self, top_text: str, bottom_text: str, template_name: str) -> float:
        """Evaluate timing and delivery (0-3 points)"""
        score = 0
        
        # Check for concise delivery
        if len(bottom_text) <= 50:
            score += 1
        
        # Check for impactful ending
        if bottom_text and bottom_text[-1] in "!?":
            score += 1
        
        # Check for template appropriateness
        if "reaction" in template_name.lower():
            score += 1
        
        return min(score, 3)
    
    def _evaluate_surprise_factor(self, top_text: str, bottom_text: str) -> float:
        """Evaluate surprise factor (0-2 points)"""
        score = 0
        
        # Check for unexpected elements
        unexpected_words = ["actually", "plot twist", "surprise", "unexpected"]
        for word in unexpected_words:
            if word in bottom_text.lower():
                score += 0.5
        
        # Check for subversion of expectations
        if "but" in bottom_text.lower():
            score += 0.5
        
        return min(score, 2)
    
    def _evaluate_wordplay_cleverness(self, top_text: str, bottom_text: str) -> float:
        """Evaluate wordplay and cleverness (0-2 points)"""
        score = 0
        
        # Check for puns or wordplay
        if any(word in bottom_text.lower() for word in ["pun", "play on words", "double meaning"]):
            score += 1
        
        # Check for clever references
        if any(word in bottom_text.lower() for word in ["reference", "callback", "meta"]):
            score += 1
        
        return min(score, 2)
    
    def _generate_humor_feedback(self, scores: Dict, total_score: float) -> str:
        """Generate feedback based on scores"""
        if total_score >= 8:
            return "Excellent humor! Strong setup-punchline structure with great timing."
        elif total_score >= 6:
            return "Good humor! Solid comedic structure with room for improvement."
        elif total_score >= 4:
            return "Decent humor. Consider strengthening the punchline or timing."
        else:
            return "Needs improvement. Focus on setup-punchline structure and timing."

class RelevanceJudgeAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Theme Relevance Evaluator",
            goal="Score how well memes connect to the given theme",
            backstory="""You specialize in thematic analysis and ensure content stays on-topic.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    async def score_relevance(self, meme_data: Dict, theme: str) -> Dict:
        """Score theme relevance (0-10 points)"""
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        template_name = meme_data.get("template_name", "")
        
        # Extract theme keywords
        theme_keywords = self._extract_keywords(theme)
        
        # Calculate relevance score
        relevance_score = 0
        max_score = 10
        
        # Direct keyword matching (0-4 points)
        keyword_score = self._calculate_keyword_relevance(top_text + " " + bottom_text, theme_keywords)
        relevance_score += keyword_score
        
        # Conceptual relevance (0-3 points)
        conceptual_score = self._calculate_conceptual_relevance(top_text, bottom_text, theme)
        relevance_score += conceptual_score
        
        # Template appropriateness (0-3 points)
        template_score = self._calculate_template_relevance(template_name, theme)
        relevance_score += template_score
        
        return {
            "total_score": relevance_score,
            "max_score": max_score,
            "keyword_score": keyword_score,
            "conceptual_score": conceptual_score,
            "template_score": template_score,
            "feedback": self._generate_relevance_feedback(relevance_score, theme)
        }
    
    def _extract_keywords(self, theme: str) -> List[str]:
        """Extract important keywords from theme"""
        # Simple keyword extraction
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = theme.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def _calculate_keyword_relevance(self, text: str, keywords: List[str]) -> float:
        """Calculate keyword relevance (0-4 points)"""
        score = 0
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        
        return min(score, 4)
    
    def _calculate_conceptual_relevance(self, top_text: str, bottom_text: str, theme: str) -> float:
        """Calculate conceptual relevance (0-3 points)"""
        # This is a simplified version - in production, you might use semantic similarity
        score = 0
        
        # Check if the meme addresses the theme concept
        theme_concepts = theme.lower().split()
        meme_text = (top_text + " " + bottom_text).lower()
        
        # Count concept matches
        concept_matches = sum(1 for concept in theme_concepts if concept in meme_text)
        score = min(concept_matches, 3)
        
        return score
    
    def _calculate_template_relevance(self, template_name: str, theme: str) -> float:
        """Calculate template relevance (0-3 points)"""
        score = 0
        
        # Check if template name relates to theme
        theme_words = theme.lower().split()
        template_lower = template_name.lower()
        
        for word in theme_words:
            if word in template_lower:
                score += 1
        
        return min(score, 3)
    
    def _generate_relevance_feedback(self, score: float, theme: str) -> str:
        """Generate relevance feedback"""
        if score >= 8:
            return f"Excellent relevance to '{theme}'! Strong thematic connection."
        elif score >= 6:
            return f"Good relevance to '{theme}'. Clear thematic connection."
        elif score >= 4:
            return f"Moderate relevance to '{theme}'. Could be more focused."
        else:
            return f"Low relevance to '{theme}'. Consider refocusing on the theme."

class OriginalityJudgeAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Creativity Assessment Specialist", 
            goal="Evaluate uniqueness and creative interpretation",
            backstory="""You assess creativity and can distinguish derivative from original content.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    async def score_originality(self, meme_data: Dict, other_memes: List[Dict]) -> Dict:
        """Score originality (0-10 points)"""
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        template_id = meme_data.get("template_id", "")
        
        originality_score = 0
        max_score = 10
        
        # Text originality (0-4 points)
        text_originality = self._evaluate_text_originality(top_text, bottom_text, other_memes)
        originality_score += text_originality
        
        # Creative interpretation (0-3 points)
        creative_interpretation = self._evaluate_creative_interpretation(top_text, bottom_text)
        originality_score += creative_interpretation
        
        # Template usage originality (0-3 points)
        template_originality = self._evaluate_template_originality(template_id, other_memes)
        originality_score += template_originality
        
        return {
            "total_score": originality_score,
            "max_score": max_score,
            "text_originality": text_originality,
            "creative_interpretation": creative_interpretation,
            "template_originality": template_originality,
            "feedback": self._generate_originality_feedback(originality_score)
        }
    
    def _evaluate_text_originality(self, top_text: str, bottom_text: str, other_memes: List[Dict]) -> float:
        """Evaluate text originality (0-4 points)"""
        score = 0
        
        # Check for unique word combinations
        combined_text = (top_text + " " + bottom_text).lower()
        
        # Check against other memes for similarity
        similarity_count = 0
        for other_meme in other_memes:
            other_text = (other_meme.get("top_text", "") + " " + other_meme.get("bottom_text", "")).lower()
            if self._calculate_text_similarity(combined_text, other_text) > 0.7:
                similarity_count += 1
        
        # Deduct points for similarity
        score = max(0, 4 - similarity_count)
        
        return score
    
    def _evaluate_creative_interpretation(self, top_text: str, bottom_text: str) -> float:
        """Evaluate creative interpretation (0-3 points)"""
        score = 0
        
        # Check for creative language use
        creative_elements = ["metaphor", "analogy", "wordplay", "puns", "references"]
        text_lower = (top_text + " " + bottom_text).lower()
        
        for element in creative_elements:
            if element in text_lower:
                score += 0.5
        
        # Check for unexpected combinations
        if len(top_text.split()) > 3 and len(bottom_text.split()) > 3:
            score += 1
        
        return min(score, 3)
    
    def _evaluate_template_originality(self, template_id: str, other_memes: List[Dict]) -> float:
        """Evaluate template usage originality (0-3 points)"""
        score = 0
        
        # Check if template is used uniquely
        template_usage_count = sum(1 for meme in other_memes if meme.get("template_id") == template_id)
        
        if template_usage_count == 0:
            score = 3  # Unique template usage
        elif template_usage_count == 1:
            score = 2  # Rare template usage
        elif template_usage_count == 2:
            score = 1  # Common template usage
        else:
            score = 0  # Overused template
        
        return score
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (0-1)"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _generate_originality_feedback(self, score: float) -> str:
        """Generate originality feedback"""
        if score >= 8:
            return "Highly original! Creative and unique interpretation."
        elif score >= 6:
            return "Good originality! Shows creative thinking."
        elif score >= 4:
            return "Moderate originality. Some creative elements present."
        else:
            return "Low originality. Consider more creative approaches." 