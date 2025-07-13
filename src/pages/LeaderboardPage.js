import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

const LeaderboardPage = () => {
  const location = useLocation();
  const result = location.state?.result;
  const [selectedMeme, setSelectedMeme] = useState(null);
  const [votes, setVotes] = useState({});

  // Mock data for leaderboard
  const leaderboardData = [
    {
      id: 1,
      user: 'MemeLord',
      meme: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAhO4KPxfi6_akUjfhNgR9wUUnUHUmUp5BeEvPgrkyQjoi1p3jRx6WcQdMQWvK7yK9cQBUdJI_jLUeuUolcLHYcQdtO2t-akkVSaRSHF41DDDGJLLIYREzsoxxQeyi90CVUTHumnmVK-UAUiITKqcNtjWqjjoxzTyZHgWylWOdiydZIgDlc9GybiJO_DxXSphpV1PZOUoo2JIMVubl-knlWURunjXkFNb_ToXKuwrFJ4VkpQGROQTn8rm-_j8dg3FNHGzJhCuY843o',
      topText: 'When the code finally works',
      bottomText: 'But you have no idea why',
      score: 1250,
      votes: 89
    },
    {
      id: 2,
      user: 'TechHumor',
      meme: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBQXppkarvpy6MuP5vtvJOW6HO923zdc9LcFWceqLrZqTWbIUKcZGB27_NZJskPmQpDyX4Lx9JY3u7p7GjROT2mM6iavxY86JHhpJbVy0zkSc9qAlhUM4ZVz-Bx4CQb02wTSgxtkFi5Sn114cqjd0c2IymVxpDXm2GbecCWx0GJLPnp2faXcxHJK-fZCup_Xg35FDHVqtBvy0xXB1kq0LHca4FlqBOds05TYVeYYKW-Xv6JL-uglWotPW8-_MDLZiQeqoH4ad8FLScA',
      topText: 'Debugging in production',
      bottomText: 'Like a boss',
      score: 980,
      votes: 67
    },
    {
      id: 3,
      user: 'CodeMaster',
      meme: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC3BZPG4liv7QNgdX0QHNIKK84Syk16ynsgJP8lFVqX5e1-xybVUnzZHYoL51I7buO6Uu-nEfnTlFP5_tziGSRTDcEbTh4L_kcusRnwyddxyT4zp9vzvMKiE8QHcqRJrDYyX-ywRmnFnjPxhJoUwZjoz5EVwrQ6dG_r-BJq96_lpvAgILXEYK25yV0eEBB4mN3tZHPIusQLJec4-Ah2MVY0eI5B6eZQmDh9xuFxbaWBoXd_g6GLbDGY79j6Z3vpGuv--a90ankUXWNF',
      topText: 'Git commit message',
      bottomText: 'Fixed stuff',
      score: 750,
      votes: 45
    }
  ];

  const handleVote = (memeId, voteType) => {
    setVotes(prev => ({
      ...prev,
      [memeId]: voteType
    }));
  };

  const handleJudgeMeme = (meme) => {
    setSelectedMeme(meme);
  };

  return (
    <div className="gap-1 px-6 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[920px] flex-1">
        {result && (
          <div className={`text-3xl font-bold mb-6 text-center ${result === 'win' ? 'text-green-400' : 'text-red-400'}`}>
            {result === 'win' ? '🎉 You win!' : '😢 You lose!'}
          </div>
        )}
        <div className="flex flex-wrap justify-between gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Leaderboard
          </p>
        </div>
        {/* Top Memes Section */}
        <div className="px-4 py-3">
          <h2 className="text-white text-xl font-bold mb-4">Top Memes</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {leaderboardData.map((meme, index) => (
              <div key={meme.id} className="bg-[#362b2c] rounded-xl p-4">
                <div className="relative">
                  <div
                    className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg mb-3"
                    style={{ backgroundImage: `url("${meme.meme}")` }}
                  ></div>
                  <div className="absolute top-2 right-2 bg-[#e8b4b7] text-[#171212] px-2 py-1 rounded-full text-xs font-bold">
                    #{index + 1}
                  </div>
                </div>
                <div className="text-white">
                  <p className="font-bold text-sm">{meme.user}</p>
                  <p className="text-xs text-[#b4a2a3] mb-2">Score: {meme.score}</p>
                  <div className="flex justify-between items-center">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleVote(meme.id, 'up')}
                        className={`px-3 py-1 rounded text-xs font-medium ${
                          votes[meme.id] === 'up' 
                            ? 'bg-green-500 text-white' 
                            : 'bg-[#4f4040] text-white'
                        }`}
                      >
                        👍 {meme.votes}
                      </button>
                      <button
                        onClick={() => handleVote(meme.id, 'down')}
                        className={`px-3 py-1 rounded text-xs font-medium ${
                          votes[meme.id] === 'down' 
                            ? 'bg-red-500 text-white' 
                            : 'bg-[#4f4040] text-white'
                        }`}
                      >
                        👎
                      </button>
                    </div>
                    <button
                      onClick={() => handleJudgeMeme(meme)}
                      className="px-3 py-1 bg-[#e8b4b7] text-[#171212] rounded text-xs font-medium"
                    >
                      Judge
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Judge Panel */}
      {selectedMeme && (
        <div className="layout-content-container flex flex-col w-[360px]">
          <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Judge Meme
          </h2>
          <div className="px-4 py-3">
            <div
              className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-xl mb-4"
              style={{ backgroundImage: `url("${selectedMeme.meme}")` }}
            ></div>
            <div className="text-white mb-4">
              <p className="font-bold">{selectedMeme.user}</p>
              <p className="text-sm text-[#b4a2a3]">"{selectedMeme.topText}"</p>
              <p className="text-sm text-[#b4a2a3]">"{selectedMeme.bottomText}"</p>
            </div>
            <div className="flex flex-col gap-3">
              <button className="w-full py-3 bg-green-500 text-white rounded-xl font-medium">
                Approve ✅
              </button>
              <button className="w-full py-3 bg-red-500 text-white rounded-xl font-medium">
                Reject ❌
              </button>
              <button 
                onClick={() => setSelectedMeme(null)}
                className="w-full py-3 bg-[#4f4040] text-white rounded-xl font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LeaderboardPage; 