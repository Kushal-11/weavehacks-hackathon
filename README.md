# Memewars

A meme generation and judging game with multiple agents and optional multiplayer sync.

## Project Structure
- `agents/` - Different bot and agent scripts
- `exa/` - Utilities
- `weave_logger/` - Logging utilities
- `firebase/` - Multiplayer sync (optional)
- `meme_engine/` - Meme generation engine
- `main_crew.py` - Main entry point
- `src/` - React frontend application

## Frontend Setup

The React frontend is now connected and working! Here's how to get started:

### Prerequisites
- Node.js (version 14 or higher)
- npm or yarn

### Installation
1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Features

### Template Page (`/`)
- Browse and search meme templates
- Click on any template to start creating a meme
- Responsive grid layout

### Meme Creation Page (`/create`)
- Edit top and bottom text for your meme
- Interactive chatbot with personality selection
- Submit memes to the leaderboard

### Leaderboard Page (`/leaderboard`)
- View top memes with scores and votes
- Judge memes with approve/reject functionality
- Vote on memes with thumbs up/down

## Backend Integration

The React app is ready to connect with your Python backend. You can:
1. Replace mock data with API calls to your Python agents
2. Connect the chatbot to your AI agents
3. Integrate with Firebase for real-time updates

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation) 