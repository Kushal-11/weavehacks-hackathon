import asyncpg
from typing import Optional, List, Dict, Any
from app.config import settings

class PostgresClient:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        """Connect to PostgreSQL"""
        self.pool = await asyncpg.create_pool(settings.POSTGRES_URL)
        
        # Create tables if they don't exist
        await self.create_tables()
    
    async def close(self):
        """Close PostgreSQL connection"""
        if self.pool:
            await self.pool.close()
    
    async def create_tables(self):
        """Create database tables"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id VARCHAR(36) PRIMARY KEY,
                    players JSONB NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    current_round INTEGER DEFAULT 1,
                    themes JSONB,
                    rounds_data JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    completed_at TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    session_id VARCHAR(100),
                    current_game VARCHAR(36),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memes (
                    id VARCHAR(36) PRIMARY KEY,
                    game_id VARCHAR(36) NOT NULL,
                    player_id VARCHAR(36) NOT NULL,
                    round_number INTEGER NOT NULL,
                    template_id VARCHAR(100) NOT NULL,
                    top_text TEXT,
                    bottom_text TEXT,
                    rendered_url TEXT,
                    scores JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
    
    async def insert_game(self, game_data: Dict[str, Any]):
        """Insert a new game"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO games (id, players, status, current_round, themes, rounds_data)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, game_data['id'], game_data['players'], game_data['status'], 
                 game_data['current_round'], game_data['themes'], game_data['rounds_data'])
    
    async def update_game(self, game_id: str, updates: Dict[str, Any]):
        """Update game data"""
        async with self.pool.acquire() as conn:
            set_clauses = []
            values = []
            param_count = 1
            
            for key, value in updates.items():
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
                param_count += 1
            
            values.append(game_id)
            query = f"UPDATE games SET {', '.join(set_clauses)} WHERE id = ${param_count}"
            await conn.execute(query, *values)
    
    async def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get game by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM games WHERE id = $1
            """, game_id)
            
            if row:
                return dict(row)
            return None
    
    async def insert_meme(self, meme_data: Dict[str, Any]):
        """Insert a new meme"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO memes (id, game_id, player_id, round_number, template_id, 
                                 top_text, bottom_text, rendered_url, scores)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, meme_data['id'], meme_data['game_id'], meme_data['player_id'],
                 meme_data['round_number'], meme_data['template_id'], meme_data['top_text'],
                 meme_data['bottom_text'], meme_data['rendered_url'], meme_data['scores'])
    
    async def get_game_memes(self, game_id: str, round_number: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get memes for a game"""
        async with self.pool.acquire() as conn:
            if round_number:
                rows = await conn.fetch("""
                    SELECT * FROM memes WHERE game_id = $1 AND round_number = $2
                """, game_id, round_number)
            else:
                rows = await conn.fetch("""
                    SELECT * FROM memes WHERE game_id = $1
                """, game_id)
            
            return [dict(row) for row in rows] 