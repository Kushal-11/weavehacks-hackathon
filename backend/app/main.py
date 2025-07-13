from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import socketio
from app.socket_handler import SocketHandler
from app.database.redis_client import RedisClient
from app.database.postgres_client import PostgresClient
from app.config import settings

# Create FastAPI app
app = FastAPI(title="MemeWars API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.io server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.ALLOWED_ORIGINS
)

# Initialize socket handler
socket_handler = SocketHandler(sio)

# Combine FastAPI and Socket.io
socket_app = socketio.ASGIApp(sio, app)

@app.on_event("startup")
async def startup_event():
    """Initialize database connections and agents"""
    try:
        await RedisClient().connect()
        await PostgresClient().connect()
        await socket_handler.initialize_agents()
        print("✅ Backend initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing backend: {e}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup connections"""
    try:
        await RedisClient().close()
        await PostgresClient().close()
        print("✅ Backend shutdown successfully")
    except Exception as e:
        print(f"❌ Error during shutdown: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "memewars-backend",
        "version": "1.0.0"
    }

# Game management endpoints
@app.post("/api/game/create")
async def create_game(player_data: dict):
    """Create new game session"""
    try:
        from app.services.game_service import GameService
        game_service = GameService()
        result = await game_service.find_or_create_match(player_data.get("player_id"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/templates/search")
async def search_templates(query: str, theme: str = ""):
    """Search for custom meme templates using Exa.ai"""
    try:
        from app.tools.exa_tool import ExaSearchTool
        from app.tools.imgflip_tool import ImgflipTool
        
        # Use Exa.ai for searching meme templates with images
        exa_tool = ExaSearchTool()
        exa_templates = await exa_tool.search_meme_templates_with_images(query)
        
        # Also get Imgflip templates as fallback
        imgflip_tool = ImgflipTool()
        imgflip_templates = await imgflip_tool.search_templates(query)
        
        # Combine and format templates
        all_templates = []
        
        # Add Exa.ai templates
        for template in exa_templates:
            all_templates.append({
                "id": template["id"],
                "name": template["name"],
                "url": template["url"],
                "image_url": template["image_url"],
                "description": template["description"],
                "source": "exa_search"
            })
        
        # Add Imgflip templates
        for template in imgflip_templates:
            all_templates.append({
                "id": template.get("id", str(hash(template.get("url", "")))),
                "name": template.get("name", "Meme Template"),
                "url": template.get("url", ""),
                "image_url": template.get("url", ""),
                "description": f"Meme template: {template.get('name', '')}",
                "source": "imgflip"
            })
        
        return {
            "templates": all_templates,
            "query": query,
            "theme": theme,
            "total": len(all_templates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/{game_id}/status")
async def get_game_status(game_id: str):
    """Get game status"""
    try:
        from app.services.game_service import GameService
        game_service = GameService()
        status = await game_service.get_game_status(game_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/meme/validate")
async def validate_meme(meme_data: dict):
    """Pre-submission meme validation"""
    try:
        from app.services.meme_service import MemeService
        meme_service = MemeService()
        validation = await meme_service.validate_meme(meme_data)
        return validation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:socket_app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    ) 