import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function generateInviteCode() {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
}

const LobbyPage = ({ user }) => {
  const [inviteCode, setInviteCode] = useState('');
  const [copied, setCopied] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setInviteCode(generateInviteCode());
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText(inviteCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 1000);
  };

  const getInitial = (name) => name ? name.charAt(0).toUpperCase() : '?';

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white" style={{ fontFamily: 'Inter, sans-serif' }}>
      <header className="border-b border-gray-700 p-4 flex justify-end items-center">
        <span className="text-gray-400 text-sm">Waiting Room / Lobby</span>
      </header>
      <main className="flex-grow flex flex-col items-center justify-center space-y-8">
        <div className="flex items-center space-x-4">
          {user?.photo ? (
            <img src={user.photo} alt="avatar" className="h-12 w-12 rounded-full object-cover" />
          ) : (
            <span className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-gray-700 text-xl font-bold">
              {getInitial(user?.name)}
            </span>
          )}
          <span className="text-2xl font-semibold">{user?.name || 'User'}</span>
        </div>
        <div className="text-center">
          <p className="text-lg text-gray-400">invite code</p>
          <div className="mt-2 flex items-center bg-gray-800 border border-gray-600 rounded-lg p-3">
            <span className="text-xl font-mono tracking-widest">{inviteCode}</span>
            <button className="ml-4 text-gray-400 hover:text-white" onClick={handleCopy} title="Copy invite code">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M16 1a1 1 0 0 1 1 1v2h2a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3h-2v2a1 1 0 0 1-1 1H5a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3h2V2a1 1 0 0 1 1-1h8Zm3 6h-2v10h2a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1Zm-4-4H9v18h6V3ZM5 5a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h2V5H5Z"/></svg>
            </button>
            {copied && <span className="ml-2 text-green-400 text-xs">Copied!</span>}
          </div>
        </div>
        <div className="text-center">
          <p className="text-xl">Player 1/2</p>
          <p className="text-gray-400 mt-1">waiting for another player...</p>
        </div>
        <button
          className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-12 rounded-lg text-xl border border-gray-500"
          onClick={() => navigate('/round')}
        >
          Start Game
        </button>
      </main>
    </div>
  );
};

export default LobbyPage; 