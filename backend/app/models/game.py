from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class GameStatus(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"

class GameModel(BaseModel):
    id: str
    players: List[str]  # player IDs
    status: GameStatus
    current_round: int
    themes: List[Dict]
    rounds_data: List[Dict]
    created_at: datetime
    completed_at: Optional[datetime] = None

class PlayerModel(BaseModel):
    id: str
    name: str
    session_id: Optional[str] = None
    current_game: Optional[str] = None

class MemeModel(BaseModel):
    id: str
    game_id: str
    player_id: str
    round_number: int
    template_id: str
    top_text: str
    bottom_text: str
    rendered_url: str
    scores: Optional[Dict] = None
    created_at: datetime 