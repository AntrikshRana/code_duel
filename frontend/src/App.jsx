import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import ProblemLibrary from './components/ProblemLibrary';
import CodeWorkspace from './components/CodeWorkspace';
import BattleLobby from './components/BattleLobby';
import BattleRoom from './components/BattleRoom';
import Leaderboard from './components/Leaderboard';
import OnlinePresenceBar from './components/OnlinePresenceBar';
import { api, getCurrentUserStored, removeAuthToken, setCurrentUserStored } from './services/api';

export default function App() {
  const [user, setUser] = useState(getCurrentUserStored());
  const [activeTab, setActiveTab] = useState('lobby');
  const [selectedProblemId, setSelectedProblemId] = useState(null);
  const [currentBattleRoomCode, setCurrentBattleRoomCode] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  useEffect(() => {
    // Attempt re-validating user profile on load
    const token = localStorage.getItem('codeduel_token');
    if (token) {
      api.getMe()
        .then(u => {
          setUser(u);
          setCurrentUserStored(u);
        })
        .catch(() => {
          removeAuthToken();
          setUser(null);
        });
    }
  }, []);

  const handleLogout = () => {
    removeAuthToken();
    localStorage.removeItem('codeduel_user');
    setUser(null);
    if (activeTab === 'battle') {
      setActiveTab('lobby');
    }
  };

  const handleSelectProblem = (probId) => {
    setSelectedProblemId(probId);
    setActiveTab('workspace');
  };

  const handleDuelProblem = async (probId) => {
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    try {
      const created = await api.createBattle(probId);
      setCurrentBattleRoomCode(created.room_code);
      setActiveTab('battle');
    } catch (err) {
      alert("Failed to initialize duel room: " + err.message);
    }
  };

  const handleEnterBattle = (roomCode) => {
    setCurrentBattleRoomCode(roomCode);
    setActiveTab('battle');
  };

  const handleLeaveBattle = () => {
    setCurrentBattleRoomCode(null);
    setActiveTab('lobby');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar 
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onOpenAuth={() => setIsAuthModalOpen(true)}
        onLogout={handleLogout}
      />

      <main style={{ flex: 1 }}>
        {activeTab === 'lobby' && (
          <BattleLobby 
            user={user}
            onEnterBattle={handleEnterBattle}
            onOpenAuth={() => setIsAuthModalOpen(true)}
            onAuthSuccess={(userData) => setUser(userData)}
          />
        )}

        {activeTab === 'problems' && (
          <ProblemLibrary 
            onSelectProblem={handleSelectProblem}
            onDuelProblem={handleDuelProblem}
          />
        )}

        {activeTab === 'workspace' && selectedProblemId && (
          <CodeWorkspace 
            problemId={selectedProblemId}
            onBack={() => setActiveTab('problems')}
            onDuelThis={(probId) => handleDuelProblem(probId)}
          />
        )}

        {activeTab === 'battle' && currentBattleRoomCode && (
          <BattleRoom 
            roomCode={currentBattleRoomCode}
            user={user}
            onLeave={handleLeaveBattle}
          />
        )}

        {activeTab === 'leaderboard' && (
          <Leaderboard />
        )}
      </main>

      {/* Realtime Live Online Presence Bottom Bar */}
      <OnlinePresenceBar />

      <AuthModal 
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onAuthSuccess={(userData) => setUser(userData)}
      />
    </div>
  );
}
