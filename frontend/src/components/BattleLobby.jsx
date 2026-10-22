import React, { useState, useEffect } from 'react';
import { Swords, Plus, LogIn, Users, Flame, Zap, Trophy, Shield, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export default function BattleLobby({ user, onEnterBattle, onOpenAuth }) {
  const [activeBattles, setActiveBattles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roomCodeInput, setRoomCodeInput] = useState('');
  const [joinError, setJoinError] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchActiveBattles();
    const interval = setInterval(fetchActiveBattles, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchActiveBattles = async () => {
    try {
      const data = await api.getActiveBattles();
      setActiveBattles(data);
    } catch (err) {
      console.error("Failed to load active battles", err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickMatch = async () => {
    if (!user) {
      onOpenAuth();
      return;
    }
    setActionLoading(true);
    setJoinError('');

    try {
      // Check if there is an active battle waiting for player 2
      const waiting = activeBattles.find(b => b.status === 'WAITING' && b.player1 !== user.id);
      if (waiting) {
        const joined = await api.joinBattle(waiting.room_code);
        onEnterBattle(joined.room_code);
      } else {
        // Create new room
        const created = await api.createBattle();
        onEnterBattle(created.room_code);
      }
    } catch (err) {
      setJoinError(err.message || 'Failed to initialize match.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCreateRoom = async () => {
    if (!user) {
      onOpenAuth();
      return;
    }
    setActionLoading(true);
    setJoinError('');
    try {
      const created = await api.createBattle();
      onEnterBattle(created.room_code);
    } catch (err) {
      setJoinError(err.message || 'Failed to create battle room.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleJoinWithCode = async (e) => {
    e.preventDefault();
    if (!user) {
      onOpenAuth();
      return;
    }
    if (!roomCodeInput.trim()) return;

    setActionLoading(true);
    setJoinError('');
    try {
      const joined = await api.joinBattle(roomCodeInput.trim().toUpperCase());
      onEnterBattle(joined.room_code);
    } catch (err) {
      setJoinError(err.message || 'Room not found or already full.');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '2rem auto', padding: '0 1.5rem' }}>
      {/* Hero Battle Banner */}
      <div className="glass-panel" style={{
        padding: '3rem 2.5rem',
        borderRadius: 'var(--radius-lg)',
        marginBottom: '2.5rem',
        position: 'relative',
        overflow: 'hidden',
        border: '1px solid rgba(244, 63, 94, 0.25)',
        background: 'linear-gradient(135deg, rgba(20, 27, 42, 0.9) 0%, rgba(30, 15, 30, 0.8) 100%)'
      }}>
        <div style={{ maxWidth: '650px', position: 'relative', zIndex: 2 }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            background: 'rgba(244, 63, 94, 0.15)',
            color: '#f43f5e',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            borderRadius: 'var(--radius-full)',
            padding: '0.35rem 0.9rem',
            fontSize: '0.78rem',
            fontWeight: 700,
            letterSpacing: '0.05em',
            marginBottom: '1rem',
            textTransform: 'uppercase'
          }}>
            <Zap size={14} />
            Real-Time Competitive Matchmaking
          </div>

          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2.8rem', fontWeight: 900, letterSpacing: '-0.02em', lineHeight: 1.1, marginBottom: '1rem' }}>
            DUEL CODERS IN <br />
            <span style={{
              background: 'linear-gradient(90deg, #f43f5e, #a855f7, #00f2fe)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              REAL-TIME 1v1 BATTLES
            </span>
          </h1>

          <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', lineHeight: 1.6, marginBottom: '1.75rem' }}>
            Both coders receive the exact same challenge simultaneously. The first player whose solution passes all automated test cases wins the duel and gains rating points.
          </p>

          {/* Action Row */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <button 
              onClick={handleQuickMatch}
              disabled={actionLoading}
              className="battle-btn"
              style={{ fontSize: '1rem', padding: '0.8rem 1.75rem' }}
            >
              <Swords size={20} />
              <span>{actionLoading ? 'Searching Arena...' : 'Quick 1v1 Match'}</span>
            </button>

            <button 
              onClick={handleCreateRoom}
              disabled={actionLoading}
              className="secondary-btn"
              style={{ fontSize: '0.95rem', padding: '0.8rem 1.4rem' }}
            >
              <Plus size={18} />
              <span>Create Custom Room</span>
            </button>
          </div>

          {joinError && (
            <div style={{ marginTop: '1rem', color: '#f87171', fontSize: '0.85rem' }}>
              {joinError}
            </div>
          )}
        </div>

        {/* Ambient background accent */}
        <div style={{
          position: 'absolute',
          right: '-50px',
          top: '-50px',
          width: '380px',
          height: '380px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(244, 63, 94, 0.2) 0%, transparent 70%)',
          pointerEvents: 'none'
        }} />
      </div>

      {/* Join By Room Code Box */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem', alignItems: 'start' }}>
        <div className="glass-panel" style={{ padding: '1.75rem' }}>
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <LogIn size={18} color="var(--accent-cyan)" />
            Join with Room Code
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            Have a friend's room code? Enter the 6-character code below to jump directly into the room.
          </p>

          <form onSubmit={handleJoinWithCode} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <input 
              type="text"
              placeholder="e.g. 8K2M9P"
              maxLength={10}
              value={roomCodeInput}
              onChange={(e) => setRoomCodeInput(e.target.value.toUpperCase())}
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem 1rem',
                color: 'var(--text-main)',
                fontSize: '1.1rem',
                fontFamily: 'var(--font-code)',
                fontWeight: 700,
                textAlign: 'center',
                letterSpacing: '0.15em',
                outline: 'none'
              }}
            />
            <button 
              type="submit"
              disabled={actionLoading || !roomCodeInput}
              className="glow-btn"
              style={{ justifyContent: 'center' }}
            >
              <span>Join Arena</span>
            </button>
          </form>
        </div>

        {/* Active Battle Rooms List */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.35rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Users size={20} color="var(--accent-purple)" />
              Active Arena Rooms ({activeBattles.length})
            </h2>

            <button 
              onClick={fetchActiveBattles} 
              className="secondary-btn"
              title="Refresh rooms"
              style={{ padding: '0.4rem 0.6rem', fontSize: '0.75rem' }}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              <span>Refresh</span>
            </button>
          </div>

          {activeBattles.length === 0 ? (
            <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Swords size={36} color="var(--text-dim)" style={{ marginBottom: '0.75rem' }} />
              <div style={{ fontSize: '1rem', fontWeight: 600 }}>No active rooms waiting right now.</div>
              <p style={{ fontSize: '0.85rem', marginTop: '0.3rem' }}>
                Hit "Quick 1v1 Match" or "Create Custom Room" to start the first battle!
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {activeBattles.map((b) => {
                const isWaiting = b.status === 'WAITING';
                return (
                  <div 
                    key={b.id}
                    className="glass-panel"
                    style={{
                      padding: '1rem 1.25rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '1rem',
                      flexWrap: 'wrap'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.25rem' }}>
                        <span style={{ fontFamily: 'var(--font-code)', fontWeight: 700, fontSize: '0.9rem', color: 'var(--accent-cyan)' }}>
                          #{b.room_code}
                        </span>
                        <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                          {b.problem_details?.title || 'Random Challenge'}
                        </span>
                        <span className={`badge ${b.problem_details?.difficulty === 'EASY' ? 'badge-easy' : b.problem_details?.difficulty === 'HARD' ? 'badge-hard' : 'badge-medium'}`}>
                          {b.problem_details?.difficulty || 'EASY'}
                        </span>
                      </div>

                      <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: '#ffffff', fontWeight: 600 }}>{b.player1_name}</span> ({b.player1_rating} pts)
                        <span style={{ color: 'var(--text-dim)' }}>vs</span>
                        <span style={{ color: b.player2_name ? '#ffffff' : 'var(--accent-amber)', fontWeight: 600 }}>
                          {b.player2_name ? `${b.player2_name} (${b.player2_rating} pts)` : 'Waiting for opponent...'}
                        </span>
                      </div>
                    </div>

                    <div>
                      {isWaiting ? (
                        <button 
                          onClick={() => {
                            if (!user) onOpenAuth();
                            else onEnterBattle(b.room_code);
                          }}
                          className="battle-btn"
                          style={{ padding: '0.45rem 0.95rem', fontSize: '0.82rem' }}
                        >
                          <Swords size={15} />
                          <span>Enter / Challenge</span>
                        </button>
                      ) : (
                        <button 
                          onClick={() => onEnterBattle(b.room_code)}
                          className="secondary-btn"
                          style={{ padding: '0.45rem 0.95rem', fontSize: '0.82rem' }}
                        >
                          <span>Spectate / Rejoin</span>
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
