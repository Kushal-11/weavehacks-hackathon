import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const EMOJIS = ['😂', '🔥', '😎', '🎉', '🤣', '🤩', '🥳', '😜'];
const EMOJI_COUNT = 16;

function getRandomEmoji() {
  return EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
}

function getRandomLeft() {
  return Math.random() * 100; // percent
}

function getRandomDuration() {
  return 3 + Math.random() * 3; // 3s to 6s
}

const HomePage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Prevent scroll on home page
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, []);

  // Generate emoji configs for animation
  const emojis = Array.from({ length: EMOJI_COUNT }).map((_, i) => {
    return {
      key: i + '-' + Math.random(),
      emoji: getRandomEmoji(),
      left: getRandomLeft(),
      duration: getRandomDuration(),
      delay: Math.random() * 3,
      size: 28 + Math.random() * 24,
    };
  });

  return (
    <div className="min-h-screen h-screen flex flex-col items-center justify-center bg-[#101624] relative overflow-hidden">
      {/* Animated falling emojis */}
      <style>{`
        @keyframes fall {
          0% { top: -60px; opacity: 0; }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { top: 100vh; opacity: 0; }
        }
      `}</style>
      {emojis.map(({ key, emoji, left, duration, delay, size }) => (
        <span
          key={key}
          style={{
            position: 'absolute',
            left: `${left}%`,
            top: '-60px', // Start well above the visible area
            fontSize: `${size}px`,
            animation: `fall ${duration}s linear ${delay}s infinite`,
            pointerEvents: 'none',
            zIndex: 1,
          }}
        >
          {emoji}
        </span>
      ))}
      {/* Main content */}
      <div className="flex flex-col items-center z-10">
        <h1 className="text-6xl md:text-7xl font-extrabold text-white drop-shadow-lg mb-2 tracking-tight" style={{textShadow: '2px 2px 0 #e8b4b7, 4px 4px 0 #293542'}}>
          MEME WAR
        </h1>
        <p className="text-gray-300 mb-8 text-lg">The ultimate meme battle begins here!</p>
        <button
          className="bg-yellow-400 hover:bg-yellow-300 text-[#101624] font-bold py-3 px-10 rounded-full text-xl shadow-lg transition-all duration-200"
          onClick={() => navigate('/lobby')}
        >
          PLAY
        </button>
      </div>
    </div>
  );
};

export default HomePage; 