import uuid
from typing import Dict, List, Optional
from datetime import datetime
from app.database.redis_client import RedisClient
from app.database.postgres_client import PostgresClient
from app.agents.meme_agents import QualityCheckerAgent

class MemeService:
    def __init__(self):
        self.redis = RedisClient()
        self.postgres = PostgresClient()
        self.quality_checker = QualityCheckerAgent()
    
    async def validate_meme(self, meme_data: Dict) -> Dict:
        """Validate meme quality and appropriateness"""
        validation_result = await self.quality_checker.validate_meme(meme_data)
        
        # Additional validation logic
        if validation_result["is_valid"]:
            # Check for duplicate submissions
            is_duplicate = await self._check_duplicate_meme(meme_data)
            if is_duplicate:
                validation_result["is_valid"] = False
                validation_result["issues"].append("Duplicate meme detected")
        
        return validation_result
    
    async def _check_duplicate_meme(self, meme_data: Dict) -> bool:
        """Check if meme is a duplicate"""
        # This is a simplified duplicate check
        # In production, you might use image hashing or more sophisticated methods
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        template_id = meme_data.get("template_id", "")
        
        # Check recent memes with same template and similar text
        recent_memes = await self._get_recent_memes(template_id)
        
        for recent_meme in recent_memes:
            if (recent_meme.get("top_text") == top_text and 
                recent_meme.get("bottom_text") == bottom_text):
                return True
        
        return False
    
    async def _get_recent_memes(self, template_id: str, hours: int = 24) -> List[Dict]:
        """Get recent memes for duplicate checking"""
        # This would query the database for recent memes
        # For now, return empty list
        return []
    
    async def store_meme(self, meme_data: Dict) -> str:
        """Store meme in database"""
        meme_id = str(uuid.uuid4())
        
        # Add metadata
        meme_data["id"] = meme_id
        meme_data["created_at"] = datetime.utcnow().isoformat()
        
        # Store in Redis for quick access
        await self.redis.set(f"meme:{meme_id}", meme_data)
        
        # Store in PostgreSQL for persistence
        try:
            await self.postgres.insert_meme(meme_data)
        except Exception as e:
            print(f"Error storing meme in PostgreSQL: {e}")
        
        return meme_id
    
    async def get_meme(self, meme_id: str) -> Optional[Dict]:
        """Get meme by ID"""
        # Try Redis first
        meme_data = await self.redis.get(f"meme:{meme_id}")
        if meme_data:
            return meme_data
        
        # Fallback to PostgreSQL
        try:
            meme_data = await self.postgres.get_meme(meme_id)
            if meme_data:
                # Cache in Redis
                await self.redis.set(f"meme:{meme_id}", meme_data)
            return meme_data
        except Exception as e:
            print(f"Error retrieving meme from PostgreSQL: {e}")
            return None
    
    async def render_meme(self, meme_data: Dict) -> str:
        """Render meme using Imgflip API"""
        # This would use the Imgflip API to render the meme
        # For now, return a placeholder URL
        template_id = meme_data.get("template_id", "")
        top_text = meme_data.get("top_text", "")
        bottom_text = meme_data.get("bottom_text", "")
        
        # In production, this would make an API call to Imgflip
        # rendered_url = await self._call_imgflip_api(template_id, top_text, bottom_text)
        
        # Placeholder implementation
        rendered_url = f"https://imgflip.com/i/{template_id}?text0={top_text}&text1={bottom_text}"
        
        return rendered_url
    
    async def _call_imgflip_api(self, template_id: str, top_text: str, bottom_text: str) -> str:
        """Call Imgflip API to render meme"""
        # This would be the actual API call implementation
        # For now, return placeholder
        return f"https://imgflip.com/i/{template_id}"
    
    async def get_meme_statistics(self, meme_id: str) -> Dict:
        """Get statistics for a meme"""
        meme_data = await self.get_meme(meme_id)
        if not meme_data:
            return {"error": "Meme not found"}
        
        # Calculate statistics
        stats = {
            "meme_id": meme_id,
            "template_id": meme_data.get("template_id"),
            "text_length": len(meme_data.get("top_text", "") + meme_data.get("bottom_text", "")),
            "created_at": meme_data.get("created_at"),
            "quality_score": meme_data.get("quality_score", 0),
            "scores": meme_data.get("scores", {})
        }
        
        return stats
    
    async def search_memes(self, query: str, limit: int = 10) -> List[Dict]:
        """Search memes by text content"""
        # This would implement a search function
        # For now, return empty list
        return []
    
    async def get_popular_memes(self, limit: int = 10) -> List[Dict]:
        """Get popular memes based on scores"""
        # This would query the database for high-scoring memes
        # For now, return empty list
        return []
    
    async def update_meme_scores(self, meme_id: str, scores: Dict):
        """Update meme scores after judging"""
        meme_data = await self.get_meme(meme_id)
        if meme_data:
            meme_data["scores"] = scores
            meme_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Update in Redis
            await self.redis.set(f"meme:{meme_id}", meme_data)
            
            # Update in PostgreSQL
            try:
                await self.postgres.update_meme(meme_id, {"scores": scores})
            except Exception as e:
                print(f"Error updating meme scores in PostgreSQL: {e}") 