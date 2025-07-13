import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RoundPage = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/play');
    }, 3000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#101624]">
      <h1 className="text-4xl font-bold text-white mb-8">Get Ready!</h1>
      <p className="text-white text-lg">The round is starting...</p>
    </div>
  );
};

export default RoundPage; 