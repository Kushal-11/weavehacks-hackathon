import React from 'react';

const HowToPlayPage = () => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-[#17191f] px-4">
    <div className="max-w-2xl w-full mt-16 bg-[#23272f] rounded-2xl shadow-lg p-10">
      <h1 className="text-4xl font-extrabold text-yellow-400 mb-6 text-center drop-shadow">How to Play Meme War</h1>
      <ol className="list-decimal list-inside text-lg text-white space-y-6">
        <li>
          <span className="font-bold text-yellow-300">Sign In or Enter Your Name:</span>
          <br />
          Start by signing in with Google or entering your name to join the game lobby.
        </li>
        <li>
          <span className="font-bold text-yellow-300">Invite Your Friends:</span>
          <br />
          Share your unique <span className="font-mono bg-gray-800 px-2 py-1 rounded text-yellow-200">invite code</span> with friends so they can join your lobby. The game works best with 2 or more players!
        </li>
        <li>
          <span className="font-bold text-yellow-300">Start the Game:</span>
          <br />
          Once everyone is in the lobby, click <span className="font-semibold text-yellow-200">Start Game</span> to begin the meme battle.
        </li>
        <li>
          <span className="font-bold text-yellow-300">Template Selection:</span>
          <br />
          Choose a meme template from the gallery. Get creative—this is your canvas!
        </li>
        <li>
          <span className="font-bold text-yellow-300">Create Your Meme:</span>
          <br />
          Add your funniest, wittiest, or most clever text to the meme. Use the chatbot for inspiration or to add a twist!
        </li>
        <li>
          <span className="font-bold text-yellow-300">Submit & Judge:</span>
          <br />
          Submit your meme. All players can view and vote on each other's creations. The best meme wins the round!
        </li>
        <li>
          <span className="font-bold text-yellow-300">Climb the Leaderboard:</span>
          <br />
          Earn points for every meme that gets upvoted. See who becomes the Meme War champion!
        </li>
      </ol>
      <div className="mt-8 text-center text-lg text-gray-300">
        <span className="inline-block bg-yellow-400 text-[#17191f] font-bold px-4 py-2 rounded-full shadow">Tip: The more creative and relatable your meme, the more votes you'll get!</span>
      </div>
    </div>
  </div>
);

export default HowToPlayPage; 