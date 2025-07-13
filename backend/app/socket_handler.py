import socketio
from typing import Dict, List
import asyncio
import json
from app.services.game_service import GameService
from app.services.meme_service import MemeService
from app.agents.theme_agents import ThemeGeneratorAgent, ThemeContextAgent
from app.agents.meme_agents import TemplateSuggestorAgent, CaptionWriterAgent
from app.agents.judge_agents import HumorJudgeAgent, RelevanceJudgeAgent, OriginalityJudgeAgent

class SocketHandler:
    def __init__(self, sio: socketio.AsyncServer):
        self.sio = sio
        self.game_service = GameService()
        self.meme_service = MemeService()
        self.active_games: Dict[str, Dict] = {}
        self.player_sessions: Dict[str, str] = {}  # session_id -> player_id
        
        # Initialize agents
        self.theme_generator = ThemeGeneratorAgent()
        self.theme_context = ThemeContextAgent()
        self.humor_judge = HumorJudgeAgent()
        self.relevance_judge = RelevanceJudgeAgent()
        self.originality_judge = OriginalityJudgeAgent()
        
        # Register event handlers
        self.register_handlers()
    
    async def initialize_agents(self):
        """Initialize CrewAI crews"""
        print("🤖 Initializing AI agents...")
        # Agents are already initialized in __init__
        print("✅ AI agents initialized")
    
    def register_handlers(self):
        """Register all socket event handlers"""
        
        @self.sio.event
        async def connect(sid, environ, auth):
            """Handle client connection"""
            print(f"🔌 Client {sid} connected")
            await self.sio.emit("connected", {"status": "success"}, room=sid)
        
        @self.sio.event 
        async def disconnect(sid):
            """Handle client disconnection"""
            if sid in self.player_sessions:
                player_id = self.player_sessions[sid]
                await self.handle_player_disconnect(player_id, sid)
            print(f"🔌 Client {sid} disconnected")
        
        @self.sio.event
        async def join_matchmaking(sid, data):
            """Player joins matchmaking queue"""
            try:
                player_id = data.get("player_id")
                self.player_sessions[sid] = player_id
                
                print(f"🎮 Player {player_id} joining matchmaking")
                
                # Try to match with waiting player
                matched_game = await self.game_service.find_or_create_match(player_id)
                
                if matched_game["status"] == "matched":
                    # Notify both players
                    game_id = matched_game["game_id"]
                    await self.sio.emit("game_matched", {
                        "game_id": game_id,
                        "opponent": matched_game["opponent"],
                        "your_player_number": matched_game["player_number"]
                    }, room=sid)
                    
                    # Start theme generation
                    await self.start_theme_generation(game_id)
                else:
                    await self.sio.emit("waiting_for_opponent", {}, room=sid)
                    
            except Exception as e:
                print(f"❌ Error in join_matchmaking: {e}")
                await self.sio.emit("error", {"message": "Matchmaking failed"}, room=sid)
        
        @self.sio.event
        async def request_templates(sid, data):
            """Player requests meme templates for theme"""
            try:
                player_id = self.player_sessions[sid]
                theme = data.get("theme")
                player_style = data.get("style", "general")
                
                print(f"🎨 Player {player_id} requesting templates for theme: {theme}")
                
                # Create template suggestor agent
                template_agent = TemplateSuggestorAgent()
                templates = await template_agent.suggest_templates(theme, player_style)
                
                await self.sio.emit("templates_suggested", {
                    "templates": templates,
                    "theme": theme
                }, room=sid)
                
            except Exception as e:
                print(f"❌ Error in request_templates: {e}")
                await self.sio.emit("error", {"message": "Template request failed"}, room=sid)
        
        @self.sio.event
        async def get_template_context(sid, data):
            """Get context for selected template"""
            try:
                player_id = self.player_sessions[sid]
                template_id = data.get("template_id")
                theme = data.get("theme")
                
                print(f"📖 Player {player_id} requesting context for template {template_id}")
                
                # Get template details from Imgflip
                from app.tools.imgflip_tool import ImgflipTool
                imgflip_tool = ImgflipTool()
                template = await imgflip_tool.get_template_by_id(template_id)
                
                context = {
                    "template": template,
                    "theme": theme,
                    "usage_tips": self._generate_usage_tips(template, theme)
                }
                
                await self.sio.emit("template_context_received", context, room=sid)
                
            except Exception as e:
                print(f"❌ Error in get_template_context: {e}")
                await self.sio.emit("error", {"message": "Context request failed"}, room=sid)
        
        @self.sio.event
        async def generate_captions(sid, data):
            """Generate caption suggestions"""
            try:
                player_id = self.player_sessions[sid]
                template_id = data.get("template_id")
                theme = data.get("theme") 
                tone = data.get("tone", "sarcastic")
                
                print(f"✍️ Player {player_id} requesting captions for template {template_id}")
                
                # Get template context
                from app.tools.imgflip_tool import ImgflipTool
                imgflip_tool = ImgflipTool()
                template = await imgflip_tool.get_template_by_id(template_id)
                
                # Create caption writer agent
                caption_agent = CaptionWriterAgent()
                template_context = f"Template: {template.get('name', '')} - {template.get('url', '')}"
                captions = await caption_agent.generate_captions(template_context, theme, tone)
                
                await self.sio.emit("captions_generated", {
                    "captions": captions,
                    "template_id": template_id,
                    "theme": theme
                }, room=sid)
                
            except Exception as e:
                print(f"❌ Error in generate_captions: {e}")
                await self.sio.emit("error", {"message": "Caption generation failed"}, room=sid)
        
        @self.sio.event
        async def submit_meme(sid, data):
            """Player submits completed meme"""
            try:
                player_id = self.player_sessions[sid]
                game_id = data.get("game_id")
                meme_data = data.get("meme_data")
                
                print(f"📤 Player {player_id} submitting meme for game {game_id}")
                
                # Validate and store meme
                validation = await self.meme_service.validate_meme(meme_data)
                
                if validation["is_valid"]:
                    # Store meme
                    meme_id = await self.meme_service.store_meme(meme_data)
                    
                    # Submit to game
                    meme_data["meme_id"] = meme_id
                    await self.game_service.submit_player_meme(game_id, player_id, meme_data)
                    
                    # Check if both players submitted
                    game_status = await self.game_service.get_game_status(game_id)
                    
                    if game_status["both_submitted"]:
                        # Start judging process
                        await self.start_judging_process(game_id)
                    else:
                        # Notify waiting for opponent
                        await self.sio.emit("waiting_for_opponent_submission", {}, room=sid)
                else:
                    await self.sio.emit("meme_validation_failed", {
                        "error": "Meme does not meet quality standards",
                        "issues": validation["issues"],
                        "suggestions": validation["suggestions"]
                    }, room=sid)
                    
            except Exception as e:
                print(f"❌ Error in submit_meme: {e}")
                await self.sio.emit("error", {"message": "Meme submission failed"}, room=sid)
    
    async def start_theme_generation(self, game_id: str):
        """Generate themes for new game"""
        try:
            print(f"🎯 Generating themes for game {game_id}")
            
            # Generate themes
            themes = await self.theme_generator.generate_themes()
            
            # Enrich themes with context
            enriched_themes = []
            for theme in themes:
                enriched_theme = await self.theme_context.enrich_theme_context(theme)
                enriched_themes.append(enriched_theme)
            
            # Store themes and start first round
            await self.game_service.set_game_themes(game_id, enriched_themes)
            await self.start_round(game_id, 1, enriched_themes[0])
            
        except Exception as e:
            print(f"❌ Error in start_theme_generation: {e}")
    
    async def start_round(self, game_id: str, round_number: int, theme: Dict):
        """Start a new round"""
        try:
            print(f"🎮 Starting round {round_number} for game {game_id}")
            
            game_data = await self.game_service.get_game(game_id)
            player_sessions = [sid for sid, pid in self.player_sessions.items() 
                              if pid in game_data["players"]]
            
            # Notify all players in game
            for session_id in player_sessions:
                await self.sio.emit("round_started", {
                    "round_number": round_number,
                    "theme": theme["name"],
                    "theme_context": theme.get("context", []),
                    "timer": 90  # 90 seconds per round
                }, room=session_id)
                
        except Exception as e:
            print(f"❌ Error in start_round: {e}")
    
    async def start_judging_process(self, game_id: str):
        """Start AI judging of submitted memes"""
        try:
            print(f"⚖️ Starting judging process for game {game_id}")
            
            memes = await self.game_service.get_round_memes(game_id)
            
            # Notify players judging started
            game_data = await self.game_service.get_game(game_id)
            player_sessions = [sid for sid, pid in self.player_sessions.items() 
                              if pid in game_data["players"]]
            
            for session_id in player_sessions:
                await self.sio.emit("judging_started", {}, room=session_id)
            
            # Run judging for each meme
            results = []
            for meme in memes:
                meme_result = await self._judge_meme(meme, game_data.get("themes", []))
                results.append(meme_result)
            
            # Calculate round results
            round_results = {
                "round": await self.game_service.get_current_round(game_id),
                "memes": results,
                "winner": self._determine_round_winner(results)
            }
            
            # Store results
            await self.game_service.store_round_results(game_id, round_results)
            
            # Notify players of results
            for session_id in player_sessions:
                await self.sio.emit("round_results", round_results, room=session_id)
            
            # Check if game is complete or start next round
            current_round = await self.game_service.get_current_round(game_id)
            if current_round > 3:
                await self.end_game(game_id)
            else:
                # Start next round after delay
                await asyncio.sleep(5)
                themes = await self.game_service.get_game_themes(game_id)
                await self.start_round(game_id, current_round, themes[current_round - 1])
                
        except Exception as e:
            print(f"❌ Error in start_judging_process: {e}")
    
    async def _judge_meme(self, meme: Dict, themes: List[Dict]) -> Dict:
        """Judge a single meme"""
        try:
            current_theme = themes[meme.get("round", 1) - 1] if themes else {"name": "Unknown"}
            
            # Get scores from all judges
            humor_score = await self.humor_judge.score_humor(meme)
            relevance_score = await self.relevance_judge.score_relevance(meme, current_theme["name"])
            originality_score = await self.originality_judge.score_originality(meme, [])  # No other memes for comparison
            
            # Calculate total score
            total_score = (
                humor_score["total_score"] * 0.4 +
                relevance_score["total_score"] * 0.4 +
                originality_score["total_score"] * 0.2
            )
            
            return {
                "meme_id": meme.get("meme_id"),
                "player_id": meme.get("player_id"),
                "total_score": total_score,
                "humor_score": humor_score,
                "relevance_score": relevance_score,
                "originality_score": originality_score,
                "feedback": {
                    "humor": humor_score["feedback"],
                    "relevance": relevance_score["feedback"],
                    "originality": originality_score["feedback"]
                }
            }
            
        except Exception as e:
            print(f"❌ Error judging meme: {e}")
            return {
                "meme_id": meme.get("meme_id"),
                "player_id": meme.get("player_id"),
                "total_score": 0,
                "error": str(e)
            }
    
    def _determine_round_winner(self, results: List[Dict]) -> str:
        """Determine the winner of a round"""
        if not results:
            return None
        
        winner = max(results, key=lambda x: x.get("total_score", 0))
        return winner.get("player_id")
    
    async def end_game(self, game_id: str):
        """End game and show final results"""
        try:
            print(f"🏁 Ending game {game_id}")
            
            final_results = await self.game_service.calculate_final_results(game_id)
            
            game_data = await self.game_service.get_game(game_id)
            player_sessions = [sid for sid, pid in self.player_sessions.items() 
                              if pid in game_data["players"]]
            
            for session_id in player_sessions:
                await self.sio.emit("game_completed", final_results, room=session_id)
                
        except Exception as e:
            print(f"❌ Error in end_game: {e}")
    
    async def handle_player_disconnect(self, player_id: str, session_id: str):
        """Handle player disconnection"""
        try:
            # Find active game for player
            active_game = await self.game_service.find_player_game(player_id)
            
            if active_game:
                # Notify opponent
                game_data = await self.game_service.get_game(active_game["game_id"])
                opponent_id = [p for p in game_data["players"] if p != player_id][0]
                opponent_session = [sid for sid, pid in self.player_sessions.items() 
                                  if pid == opponent_id]
                
                if opponent_session:
                    await self.sio.emit("opponent_disconnected", {}, room=opponent_session[0])
            
            # Cleanup
            del self.player_sessions[session_id]
            
        except Exception as e:
            print(f"❌ Error handling player disconnect: {e}")
    
    def _generate_usage_tips(self, template: Dict, theme: str) -> List[str]:
        """Generate usage tips for a template"""
        tips = []
        
        if template:
            template_name = template.get("name", "").lower()
            
            if "reaction" in template_name:
                tips.append("This template works great for expressing reactions to the theme")
            elif "comparison" in template_name:
                tips.append("Perfect for comparing different aspects of the theme")
            elif "progression" in template_name:
                tips.append("Great for showing how the theme evolves or changes")
            else:
                tips.append("This template can be used to create engaging content about the theme")
        
        tips.append("Keep your text concise and impactful")
        tips.append("Consider the cultural context of the theme")
        
        return tips 