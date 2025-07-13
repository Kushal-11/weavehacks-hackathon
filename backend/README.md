# MemeWars Backend

A Python backend for the MemeWars real-time multiplayer meme battle game, built with FastAPI, Socket.io, and CrewAI.

## 🏗️ Architecture

- **FastAPI**: REST API endpoints
- **Socket.io**: Real-time multiplayer communication
- **CrewAI**: AI agents for theme generation, meme creation, and judging
- **Redis**: Real-time game state and caching
- **PostgreSQL**: Persistent data storage
- **External APIs**: Exa.ai, Imgflip, Weights & Biases

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis server
- PostgreSQL database
- API keys for external services

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and database configuration
   ```

4. **Start the server**
   ```bash
   python -m app.main
   ```

The server will start on `http://localhost:8000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Keys
EXA_API_KEY=your_exa_api_key_here
WANDB_API_KEY=your_wandb_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://user:password@localhost/memewars

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000"]

# Game Settings
ROUND_DURATION=90
ROUNDS_PER_GAME=3
```

### Database Setup

1. **Redis**
   ```bash
   # Install Redis (Ubuntu/Debian)
   sudo apt-get install redis-server
   
   # Start Redis
   sudo systemctl start redis-server
   ```

2. **PostgreSQL**
   ```bash
   # Install PostgreSQL (Ubuntu/Debian)
   sudo apt-get install postgresql postgresql-contrib
   
   # Create database
   sudo -u postgres createdb memewars
   ```

## 🤖 AI Agents

The backend uses CrewAI agents for various game functions:

### Theme Generation
- **ThemeGeneratorAgent**: Generates engaging meme themes using trending topics
- **ThemeContextAgent**: Provides cultural context for themes

### Meme Creation
- **TemplateSuggestorAgent**: Suggests relevant meme templates
- **CaptionWriterAgent**: Generates caption suggestions
- **QualityCheckerAgent**: Validates meme quality and appropriateness

### Judging
- **HumorJudgeAgent**: Scores memes on humor quality
- **RelevanceJudgeAgent**: Evaluates theme relevance
- **OriginalityJudgeAgent**: Assesses creativity and uniqueness

## 🌐 API Endpoints

### REST API

- `GET /health` - Health check
- `POST /api/game/create` - Create new game session
- `GET /api/templates/search` - Search meme templates
- `GET /api/game/{game_id}/status` - Get game status
- `POST /api/meme/validate` - Validate meme before submission

### Socket.io Events

#### Client → Server
- `join_matchmaking` - Join matchmaking queue
- `request_templates` - Request meme templates for theme
- `get_template_context` - Get context for selected template
- `generate_captions` - Generate caption suggestions
- `submit_meme` - Submit completed meme

#### Server → Client
- `connected` - Connection established
- `game_matched` - Game matched with opponent
- `waiting_for_opponent` - Waiting for opponent to join
- `round_started` - New round started
- `templates_suggested` - Template suggestions received
- `captions_generated` - Caption suggestions received
- `judging_started` - AI judging in progress
- `round_results` - Round results announced
- `game_completed` - Game finished with final results

## 🎮 Game Flow

1. **Matchmaking**: Players join matchmaking queue
2. **Theme Generation**: AI generates themes for the game
3. **Template Selection**: Players choose meme templates
4. **Caption Creation**: AI suggests captions, players create memes
5. **Submission**: Players submit their memes
6. **Judging**: AI judges memes on humor, relevance, and originality
7. **Results**: Round results are announced
8. **Next Round**: Process repeats for 3 rounds
9. **Final Results**: Overall winner is determined

## 🛠️ Development

### Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── socket_handler.py       # Socket.io event handlers
│   ├── agents/                 # CrewAI agent definitions
│   ├── services/               # Business logic
│   ├── models/                 # Data models
│   ├── tools/                  # External API tools
│   ├── database/              # Database setup
│   └── config.py              # Configuration
├── requirements.txt
├── env.example
└── README.md
```

### Running Tests

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

### Code Quality

```bash
# Run linting
flake8 app/

# Run type checking
mypy app/
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t memewars-backend .

# Run container
docker run -p 8000:8000 memewars-backend
```

### Production

1. Set `DEBUG=false` in environment
2. Configure production database URLs
3. Set up proper CORS origins
4. Use production-grade Redis and PostgreSQL
5. Set up monitoring and logging

## 📊 Monitoring

The backend includes:
- Health check endpoint
- Comprehensive logging
- Error tracking
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 