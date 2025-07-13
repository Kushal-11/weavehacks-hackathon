import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SignInPage from './pages/SignInPage';
import HomePage from './pages/HomePage';
import LobbyPage from './pages/LobbyPage';
import RoundPage from './pages/RoundPage';
import TemplatePage from './pages/TemplatePage';
import MemeCreationPage from './pages/MemeCreationPage';
import LeaderboardDecisionPage from './pages/LeaderboardDecisionPage';
import LeaderboardPage from './pages/LeaderboardPage';
import HowToPlayPage from './pages/HowToPlayPage';
import Header from './components/Header';

function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <div className="relative flex size-full min-h-screen flex-col bg-[#14191f] dark group/design-root overflow-x-hidden">
        <div className="layout-container flex h-full grow flex-col">
          <Header user={user} />
          <Routes>
            <Route path="/signin" element={<SignInPage setUser={setUser} />} />
            <Route path="/lobby" element={user ? <LobbyPage user={user} /> : <Navigate to="/signin" />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/round" element={<RoundPage />} />
            <Route path="/play" element={<TemplatePage />} />
            <Route path="/create" element={<MemeCreationPage />} />
            <Route path="/leaderbaord_decision" element={<LeaderboardDecisionPage />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
            <Route path="/how-to-play" element={<HowToPlayPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App; 