import React, { useState } from 'react';
import { auth, provider } from '../firebase';
import { signInWithPopup } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';

const SignInPage = ({ setUser }) => {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleGoogleSignIn = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      setUser({
        name: result.user.displayName,
        email: result.user.email,
        uid: result.user.uid,
        photo: result.user.photoURL,
      });
      navigate('/lobby');
    } catch (error) {
      alert('Sign in failed');
    }
  };

  const handleManualSignIn = (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Please enter your name.');
      return;
    }
    setUser({ name: name.trim() });
    navigate('/lobby');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#101624]">
      <h1 className="text-4xl font-bold text-white mb-8">Sign In</h1>
      <form onSubmit={handleManualSignIn} className="flex flex-col items-center mb-6 w-full max-w-xs">
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={e => { setName(e.target.value); setError(''); }}
          className="mb-2 px-4 py-2 rounded text-lg w-full"
        />
        {error && <span className="text-red-400 text-sm mb-2">{error}</span>}
        <button
          type="submit"
          className="bg-yellow-400 hover:bg-yellow-300 text-[#101624] font-bold py-2 px-6 rounded-full text-lg shadow-lg transition-all duration-200 w-full"
        >
          Continue
        </button>
      </form>
      <div className="text-white mb-2">or</div>
      <button
        className="bg-white text-black font-bold py-3 px-10 rounded-full text-xl shadow-lg transition-all duration-200"
        onClick={handleGoogleSignIn}
      >
        Sign in with Google
      </button>
    </div>
  );
};

export default SignInPage; 