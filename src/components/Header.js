import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = ({ user }) => {
  const location = useLocation();

  const getInitial = (name) => name ? name.charAt(0).toUpperCase() : '?';

  const isHome = location.pathname === '/';

  return (
    <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#293542] px-10 py-3">
      <div className="flex items-center gap-4 text-white">
        <Link to="/">
          <img src="/memewar-logo.png" alt="Meme War Logo" className="h-10 w-auto" style={{maxHeight: 40}} />
        </Link>
      </div>
      <div className="flex flex-1 justify-end gap-8">
        <div className="flex items-center gap-9">
          <Link 
            to="/signin" 
            className={`text-sm font-medium leading-normal ${
              location.pathname === '/signin' ? 'text-[#e8b4b7]' : 'text-white'
            }`}
          >
            Play Game
          </Link>
          {!isHome && (
            <Link 
              to="/leaderboard" 
              className={`text-sm font-medium leading-normal ${
                location.pathname === '/leaderboard' ? 'text-[#e8b4b7]' : 'text-white'
              }`}
            >
              Leaderboard
            </Link>
          )}
          <Link 
            to="/how-to-play" 
            className={`text-sm font-medium leading-normal ${
              location.pathname === '/how-to-play' ? 'text-[#e8b4b7]' : 'text-white'
            }`}
          >
            How to Play
          </Link>
        </div>
        {/* User avatar or initials */}
        {user ? (
          user.photo ? (
            <img src={user.photo} alt="avatar" className="h-10 w-10 rounded-full object-cover ml-4" />
          ) : (
            <div className="bg-[#293542] text-white flex items-center justify-center rounded-full h-10 w-10 ml-4 text-lg font-bold">
              {getInitial(user.name)}
            </div>
          )
        ) : (
          <div className="bg-[#293542] text-white flex items-center justify-center rounded-full h-10 w-10 ml-4 text-lg font-bold">
            ?
          </div>
        )}
      </div>
    </header>
  );
};

export default Header; 