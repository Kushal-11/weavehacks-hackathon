import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const MemeCreationPage = () => {
  const [topText, setTopText] = useState('');
  const [bottomText, setBottomText] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [chatMessage, setChatMessage] = useState('');
  const [selectedPersonality, setSelectedPersonality] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { sender: 'Bot', message: 'Welcome to MemeWar! How can I assist you today?' }
  ]);
  
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.selectedTemplate) {
      setSelectedTemplate(location.state.selectedTemplate);
    }
  }, [location.state]);

  const handleSubmitMeme = () => {
    // Simulate win/lose for demo
    const result = Math.random() > 0.5 ? 'win' : 'lose';
    navigate('/leaderboard', { state: { result } });
  };

  const handleSendMessage = () => {
    if (chatMessage.trim()) {
      const newMessage = { sender: 'User', message: chatMessage };
      setChatHistory([...chatHistory, newMessage]);
      setChatMessage('');
      
      // Simulate bot response
      setTimeout(() => {
        const botResponse = { sender: 'Bot', message: 'Thanks for your message! I\'m here to help with your meme creation.' };
        setChatHistory(prev => [...prev, botResponse]);
      }, 1000);
    }
  };

  return (
    <div className="gap-1 px-6 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[920px] flex-1">
        <div className="flex flex-wrap justify-between gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Meme Creation
          </p>
        </div>
        <div className="flex w-full grow bg-[#171212] @container p-4">
          <div className="w-full gap-1 overflow-hidden bg-[#171212] @[480px]:gap-2 aspect-[3/2] rounded-xl flex">
            <div
              className="w-full bg-center bg-no-repeat bg-cover aspect-auto rounded-none flex-1"
              style={{ 
                backgroundImage: selectedTemplate ? `url("${selectedTemplate}")` : 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAhO4KPxfi6_akUjfhNgR9wUUnUHUmUp5BeEvPgrkyQjoi1p3jRx6WcQdMQWvK7yK9cQBUdJI_jLUeuUolcLHYcQdtO2t-akkVSaRSHF41DDDGJLLIYREzsoxxQeyi90CVUTHumnmVK-UAUiITKqcNtjWqjjoxzTyZHgWylWOdiydZIgDlc9GybiJO_DxXSphpV1PZOUoo2JIMVubl-knlWURunjXkFNb_ToXKuwrFJ4VkpQGROQTn8rm-_j8dg3FNHGzJhCuY843o")'
              }}
            ></div>
          </div>
        </div>
        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
          <label className="flex flex-col min-w-40 flex-1">
            <input
              placeholder="Top Text"
              className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#362b2c] focus:border-none h-14 placeholder:text-[#b4a2a3] p-4 text-base font-normal leading-normal"
              value={topText}
              onChange={(e) => setTopText(e.target.value)}
            />
          </label>
        </div>
        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
          <label className="flex flex-col min-w-40 flex-1">
            <input
              placeholder="Bottom Text"
              className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#362b2c] focus:border-none h-14 placeholder:text-[#b4a2a3] p-4 text-base font-normal leading-normal"
              value={bottomText}
              onChange={(e) => setBottomText(e.target.value)}
            />
          </label>
        </div>
        <div className="flex px-4 py-3 justify-end">
          <button
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#e8b4b7] text-[#171212] text-sm font-bold leading-normal tracking-[0.015em]"
            onClick={handleSubmitMeme}
          >
            <span className="truncate">Submit Meme</span>
          </button>
        </div>
      </div>
      <div className="layout-content-container flex flex-col w-[360px]">
        <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
          Chatbot
        </h2>
        <div className="flex flex-col gap-3 p-4 max-h-64 overflow-y-auto">
          {chatHistory.map((chat, index) => (
            <div key={index} className="flex items-end gap-3">
              <div
                className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 shrink-0"
                style={{
                  backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAOTT755ypGQi10EH2xe9rdVY9oHbXvk9CF3NKQv5yr50cyLzaTccSvNreR3J-JimxPbO0oLhjXgovM-ghTSrUonhpOhe3A9HVLN8veIRRbFLQ0fKeE1pPkuOiU-fYxfwToRSnqs54aOznkX71I1KauaMWGHrIG6Eu7-q-KE4Msgaarf0h8DiFGxapYDZESRExY4roVFH5nJryB4QwLvzD9_0gozPhFkC9OjvmIKBaDIw6B64f5RudPaLMt4TP8gPtKe65BmbqGUkk")'
                }}
              ></div>
              <div className="flex flex-1 flex-col gap-1 items-start">
                <p className="text-[#b4a2a3] text-[13px] font-normal leading-normal max-w-[360px]">
                  {chat.sender}
                </p>
                <p className="text-base font-normal leading-normal flex max-w-[360px] rounded-xl px-4 py-3 bg-[#362b2c] text-white">
                  {chat.message}
                </p>
              </div>
            </div>
          ))}
        </div>
        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
          <label className="flex flex-col min-w-40 flex-1">
            <textarea
              placeholder="Type your message..."
              className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#362b2c] focus:border-none min-h-36 placeholder:text-[#b4a2a3] p-4 text-base font-normal leading-normal"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            ></textarea>
          </label>
        </div>
        <div className="flex px-4 py-3 justify-end">
          <button
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#e8b4b7] text-[#171212] text-sm font-bold leading-normal tracking-[0.015em]"
            onClick={handleSendMessage}
          >
            <span className="truncate">Send</span>
          </button>
        </div>
        <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
          Personality
        </h2>
        <div className="flex flex-wrap gap-3 p-4">
          {['Funny', 'Serious', 'Sarcastic'].map((personality) => (
            <label
              key={personality}
              className={`text-sm font-medium leading-normal flex items-center justify-center rounded-xl border px-4 h-11 text-white relative cursor-pointer ${
                selectedPersonality === personality 
                  ? 'border-[3px] px-3.5 border-[#e8b4b7]' 
                  : 'border-[#4f4040]'
              }`}
            >
              {personality}
              <input 
                type="radio" 
                className="invisible absolute" 
                name="personality" 
                value={personality}
                checked={selectedPersonality === personality}
                onChange={(e) => setSelectedPersonality(e.target.value)}
              />
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MemeCreationPage; 