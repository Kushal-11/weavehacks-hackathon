import uuid
import json
from typing import Dict, List, Optional
from datetime import datetime
from app.database.redis_client import RedisClient
from app.database.postgres_client import PostgresClient
from app.models.game import GameModel, GameStatus

class GameService:
    def __init__(self):
        self.redis = RedisClient()
        self.postgres = PostgresClient()
    
    async def find_or_create_match(self, player_id: str) -> Dict:
        """Find existing waiting game or create new one"""
        # Check for waiting games
        waiting_games = await self.redis.get("waiting_games") or []
        
        if waiting_games:
            # Join existing game
            game_id = waiting_games.pop(0)
            await self.redis.set("waiting_games", waiting_games)
            
            # Add player to game
            game_data = await self.redis.get(f"game:{game_id}")
            if game_data:
                game = GameModel.parse_raw(game_data)
                game.players.append(player_id)
                game.status = GameStatus.IN_PROGRESS
                
                await self.redis.set(f"game:{game_id}", game.json())
                
                return {
                    "status": "matched",
                    "game_id": game_id,
                    "opponent": game.players[0],
                    "player_number": 2
                }
        
        # Create new game
        game_id = str(uuid.uuid4())
        game = GameModel(
            id=game_id,
            players=[player_id],
            status=GameStatus.WAITING,
            current_round=1,
            themes=[],
            rounds_data=[],
            created_at=datetime.utcnow()
        )
        
        await self.redis.set(f"game:{game_id}", game.json())
        
        # Add to waiting queue
        waiting_games.append(game_id)
        await self.redis.set("waiting_games", waiting_games)
        
        return {
            "status": "waiting",
            "game_id": game_id,
            "player_number": 1
        }
    
    async def get_game(self, game_id: str) -> Optional[Dict]:
        """Get game data"""
        game_data = await self.redis.get(f"game:{game_id}")
        if game_data:
            return json.loads(game_data) if isinstance(game_data, str) else game_data
        return None
    
    async def get_game_status(self, game_id: str) -> Dict:
        """Get current game status"""
        game_data = await self.get_game(game_id)
        if not game_data:
            return {"error": "Game not found"}
        
        # Check if both players submitted memes
        memes = await self.get_round_memes(game_id)
        both_submitted = len(memes) >= 2
        
        return {
            "game_id": game_id,
            "status": game_data.get("status"),
            "current_round": game_data.get("current_round", 1),
            "players": game_data.get("players", []),
            "both_submitted": both_submitted,
            "memes_submitted": len(memes)
        }
    
    async def submit_player_meme(self, game_id: str, player_id: str, meme_data: Dict):
        """Store player's meme submission"""
        meme_key = f"meme:{game_id}:{player_id}:{meme_data.get('round', 1)}"
        meme_data["submitted_at"] = datetime.utcnow().isoformat()
        await self.redis.set(meme_key, meme_data)
    
    async def get_round_memes(self, game_id: str) -> List[Dict]:
        """Get all memes for current round"""
        game_data = await self.get_game(game_id)
        if not game_data:
            return []
        
        current_round = game_data.get("current_round", 1)
        memes = []
        
        for player_id in game_data.get("players", []):
            meme_key = f"meme:{game_id}:{player_id}:{current_round}"
            meme_data = await self.redis.get(meme_key)
            if meme_data:
                if isinstance(meme_data, str):
                    meme_data = json.loads(meme_data)
                memes.append(meme_data)
        
        return memes
    
    async def set_game_themes(self, game_id: str, themes: List[Dict]):
        """Set themes for a game"""
        game_data = await self.get_game(game_id)
        if game_data:
            game_data["themes"] = themes
            await self.redis.set(f"game:{game_id}", game_data)
    
    async def get_game_themes(self, game_id: str) -> List[Dict]:
        """Get themes for a game"""
        game_data = await self.get_game(game_id)
        return game_data.get("themes", []) if game_data else []
    
    async def store_round_results(self, game_id: str, results: Dict):
        """Store judging results for round"""
        results_key = f"results:{game_id}:{results.get('round', 1)}"
        await self.redis.set(results_key, results)
        
        # Update game data
        game_data = await self.get_game(game_id)
        if game_data:
            if "rounds_data" not in game_data:
                game_data["rounds_data"] = []
            game_data["rounds_data"].append(results)
            
            # Increment round
            game_data["current_round"] = game_data.get("current_round", 1) + 1
            
            await self.redis.set(f"game:{game_id}", game_data)
    
    async def get_current_round(self, game_id: str) -> int:
        """Get current round number"""
        game_data = await self.get_game(game_id)
        return game_data.get("current_round", 1) if game_data else 1
    
    async def calculate_final_results(self, game_id: str) -> Dict:
        """Calculate final game results"""
        game_data = await self.get_game(game_id)
        if not game_data:
            return {"error": "Game not found"}
        
        rounds_data = game_data.get("rounds_data", [])
        players = game_data.get("players", [])
        
        # Calculate total scores for each player
        player_scores = {player_id: 0 for player_id in players}
        
        for round_data in rounds_data:
            for player_result in round_data.get("player_results", []):
                player_id = player_result.get("player_id")
                total_score = player_result.get("total_score", 0)
                if player_id in player_scores:
                    player_scores[player_id] += total_score
        
        # Determine winner
        winner_id = max(player_scores, key=player_scores.get) if player_scores else None
        
        final_results = {
            "game_id": game_id,
            "winner": winner_id,
            "player_scores": player_scores,
            "rounds_data": rounds_data,
            "total_rounds": len(rounds_data)
        }
        
        # Mark game as completed
        game_data["status"] = GameStatus.COMPLETED
        game_data["completed_at"] = datetime.utcnow().isoformat()
        await self.redis.set(f"game:{game_id}", game_data)
        
        return final_results
    
    async def find_player_game(self, player_id: str) -> Optional[Dict]:
        """Find active game for a player"""
        # This is a simplified implementation
        # In production, you might want to maintain a player-game mapping
        waiting_games = await self.redis.get("waiting_games") or []
        
        for game_id in waiting_games:
            game_data = await self.get_game(game_id)
            if game_data and player_id in game_data.get("players", []):
                return {"game_id": game_id, "status": "waiting"}
        
        # Check active games (this would need a more efficient implementation)
        # For now, return None
        return None 