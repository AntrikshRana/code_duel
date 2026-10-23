import React, { useState, useEffect, useRef } from 'react';
import { Swords, Plus, LogIn, Users, Flame, Zap, Trophy, Shield, RefreshCw, Radio, X, CheckCircle2, Sparkles } from 'lucide-react';
import { api } from '../services/api';

export default function BattleLobby({ user, onEnterBattle, onOpenAuth, onAuthSuccess }) {
  const [activeBattles, setActiveBattles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roomCodeInput, setRoomCodeInput] = useState('');
  const [joinError, setJoinError] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  // Matchmaking State
  const [isSearching, setIsSearching] = useState(false);
  const [searchSeconds, setSearchSeconds] = useState(0);
  const [difficultyPref, setDifficultyPref] = useState('ANY');
  const [matchedPayload, setMatchedPayload] = useState(null);

  const searchTimerRef = useRef(null);
  const pollTimerRef = useRef(null);

  useEffect(() => {
    fetchActiveBattles();
    const interval = setInterval(fetchActiveBattles, 5000);
    return () => clearInterval(interval);
  }, []);

  // Cleanup matchmaking on unmount
  useEffect(() => {
    return () => {
      if (searchTimerRef.current) clearInterval(searchTimerRef.current);
      if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    };
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

  const handlePasteCode = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        setRoomCodeInput(text.trim().toUpperCase());
      }
    } catch (err) {
      // clipboard read not permitted or empty
    }
  };

  const handleGuestQuickStart = async () => {
    setActionLoading(true);
    try {
      const res = await api.guestLogin();
      if (onAuthSuccess) onAuthSuccess(res.user);
    } catch (err) {
      onOpenAuth();
    } finally {
      setActionLoading(false);
    }
  };

  // ==========================================
  // ELO MATCHMAKING HANDLERS
  // ==========================================
  const startMatchmaking = async () => {
    if (!user) {
      onOpenAuth();
      return;
    }
    setJoinError('');
    setIsSearching(true);
    setSearchSeconds(0);
    setMatchedPayload(null);

    // Start timer counter
    searchTimerRef.current = setInterval(() => {
      setSearchSeconds(s => s + 1);
    }, 1000);

    try {
      const res = await api.joinMatchmaking(difficultyPref);
      if (res.matched) {
        // Immediate match found!
        handleMatchSuccess(res);
        return;
      }

      // No immediate opponent; poll queue every 2 seconds
      pollTimerRef.current = setInterval(async () => {
        try {
          const status = await api.checkMatchmakingStatus();
          if (status.matched) {
            handleMatchSuccess(status);
          }
        } catch (e) {
          console.error("Matchmaking poll error", e);
        }
      }, 2000);

    } catch (err) {
      setJoinError(err.message || 'Failed to enter matchmaking queue.');
      stopMatchmaking();
    }
  };

  const handleMatchSuccess = (payload) => {
    if (searchTimerRef.current) clearInterval(searchTimerRef.current);
    if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    setMatchedPayload(payload);

    // Auto-enter battle room after 2 seconds
    setTimeout(() => {
      setIsSearching(false);
      setMatchedPayload(null);
      onEnterBattle(payload.room_code);
    }, 2200);
  };

  const stopMatchmaking = async () => {
    if (searchTimerRef.current) clearInterval(searchTimerRef.current);
    if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    setIsSearching(false);
    setSearchSeconds(0);
    setMatchedPayload(null);

    try {
      await api.leaveMatchmaking();
    } catch (e) {
      // ignore
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

  const myRating = user?.profile?.rating ?? 0;
  const ratingRangeMin = Math.max(0, myRating - 100 - Math.floor(searchSeconds / 5) * 50);
  const ratingRangeMax = myRating + 100 + Math.floor(searchSeconds / 5) * 50;

  const searchMinutes = Math.floor(searchSeconds / 60);
  const searchSecs = searchSeconds % 60;
  const formattedSearchTime = `${String(searchMinutes).padStart(2, '0')}:${String(searchSecs).padStart(2, '0')}`;

  return (
    <div style={{ maxWidth: '1280px', margin: '2rem auto', padding: '0 1.5rem' }}>
      {/* Friendly Guest Onboarding Banner */}
      {!user && (
        <div style={{
          background: 'rgba(0, 242, 254, 0.07)',
          border: '1px solid rgba(0, 242, 254, 0.22)',
          borderRadius: '14px',
          padding: '1rem 1.4rem',
          marginBottom: '1.75rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem',
          flexWrap: 'wrap'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '9px',
              background: 'rgba(0, 242, 254, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#00f2fe'
            }}>
              <Sparkles size={20} />
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.98rem', color: '#fff' }}>
                Welcome to CodeDuel! Jump into a 1v1 battle now
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                Sign in to save your ranking, or try an instant guest match in one click.
              </div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <button
              onClick={onOpenAuth}
              className="secondary-btn"
              style={{ fontSize: '0.82rem', padding: '0.5rem 0.95rem' }}
            >
              Sign In / Register
            </button>
            <button
              onClick={handleGuestQuickStart}
              disabled={actionLoading}
              className="battle-btn"
              style={{ fontSize: '0.82rem', padding: '0.5rem 1rem' }}
            >
              <Zap size={14} />
              <span>Instant Guest Play</span>
            </button>
          </div>
        </div>
      )}

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
        <div style={{ maxWidth: '680px', position: 'relative', zIndex: 2 }}>

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
            ELO Competitive Matchmaking Engine
          </div>

          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2.8rem', fontWeight: 900, letterSpacing: '-0.02em', lineHeight: 1.1, marginBottom: '1rem' }}>
            FIND AN OPPONENT & <br />
            <span style={{
              background: 'linear-gradient(90deg, #f43f5e, #a855f7, #00f2fe)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              CLASH IN REAL-TIME 1v1
            </span>
          </h1>

          <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', lineHeight: 1.6, marginBottom: '1.75rem' }}>
            Queue up to be paired automatically with a coder of similar rating. 5-minute thinking phase, 15-35 min difficulty timers, and time-complexity bonus points!
          </p>

          {/* Difficulty Tier Selector */}
          <div style={{ marginBottom: '1.75rem' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.65rem' }}>
              Choose Matchmaking Difficulty Tier:
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '0.65rem' }}>
              {[
                { id: 'ANY', label: 'Any Tier', time: 'Random', color: '#00f2fe' },
                { id: 'EASY', label: 'Easy Tier', time: '15m Code', color: '#34d399' },
                { id: 'MEDIUM', label: 'Medium Tier', time: '25m Code', color: '#fbbf24' },
                { id: 'HARD', label: 'Hard Tier', time: '35m Code', color: '#f87171' }
              ].map(tier => {
                const isSelected = difficultyPref === tier.id;
                return (
                  <button
                    key={tier.id}
                    onClick={() => setDifficultyPref(tier.id)}
                    type="button"
                    style={{
                      background: isSelected ? 'rgba(20, 27, 42, 0.95)' : 'rgba(255, 255, 255, 0.03)',
                      border: isSelected ? `2px solid ${tier.color}` : '1px solid var(--border-subtle)',
                      boxShadow: isSelected ? `0 0 15px ${tier.color}40` : 'none',
                      borderRadius: 'var(--radius-sm)',
                      padding: '0.65rem 0.75rem',
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.2rem'
                    }}
                  >
                    <span style={{ fontSize: '0.85rem', fontWeight: 800, color: isSelected ? tier.color : 'var(--text-main)' }}>
                      {tier.label}
                    </span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                      ⏱️ {tier.time}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Action Row */}
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.25rem', flexWrap: 'wrap' }}>
            <div>
              <button 
                onClick={startMatchmaking}
                disabled={isSearching}
                className="battle-btn"
                style={{ fontSize: '1rem', padding: '0.85rem 1.85rem' }}
              >
                <Swords size={20} />
                <span>Enter Matchmaking Queue</span>
              </button>
              <div style={{ fontSize: '0.72rem', color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.35rem', marginTop: '0.45rem', fontWeight: 600 }}>
                🔥 Ranked Mode: Awards Rating Points & Win Streaks
              </div>
            </div>

            <div>
              <button 
                onClick={handleCreateRoom}
                disabled={isSearching || actionLoading}
                className="secondary-btn"
                style={{ fontSize: '0.95rem', padding: '0.85rem 1.4rem' }}
              >
                <Plus size={18} />
                <span>Create Custom Room</span>
              </button>
              <div style={{ fontSize: '0.72rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '0.35rem', marginTop: '0.45rem', fontWeight: 500 }}>
                🎮 Casual Practice: Unrated (No points earned)
              </div>
            </div>
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

      {/* Join By Room Code Box & Active Rooms List */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem', alignItems: 'start' }}>
        <div className="glass-panel" style={{ padding: '1.75rem' }}>
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <LogIn size={18} color="var(--accent-cyan)" />
            Join with Room Code
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            Enter a friend's 6-character room code to join their custom battle arena.
          </p>

          <form onSubmit={handleJoinWithCode} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div style={{ position: 'relative' }}>
              <input 
                type="text"
                placeholder="e.g. 8K2M9P"
                maxLength={10}
                value={roomCodeInput}
                onChange={(e) => setRoomCodeInput(e.target.value.toUpperCase())}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.75rem 4.5rem 0.75rem 1rem',
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
                type="button"
                onClick={handlePasteCode}
                title="Paste from clipboard"
                style={{
                  position: 'absolute',
                  right: '0.6rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'rgba(255, 255, 255, 0.08)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '6px',
                  color: 'var(--text-muted)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  padding: '0.35rem 0.65rem',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.color = '#fff'; e.currentTarget.style.background = 'rgba(255, 255, 255, 0.15)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)'; }}
              >
                Paste
              </button>
            </div>
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
                Hit "Enter Matchmaking Queue" to find an opponent!
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
                        {b.is_ranked ? (
                          <span style={{ fontSize: '0.65rem', fontWeight: 800, color: '#f87171', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>
                            ⚔️ RANKED
                          </span>
                        ) : (
                          <span style={{ fontSize: '0.65rem', fontWeight: 600, color: '#94a3b8', background: 'rgba(148, 163, 184, 0.15)', border: '1px solid rgba(148, 163, 184, 0.25)', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>
                            🎮 CASUAL
                          </span>
                        )}
                      </div>

                      <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: '#ffffff', fontWeight: 600 }}>{b.player1_name}</span> ({b.player1_rating} pts {b.player1_streak > 0 ? `🔥${b.player1_streak}` : ''})
                        <span style={{ color: 'var(--text-dim)' }}>vs</span>
                        <span style={{ color: b.player2_name ? '#ffffff' : 'var(--accent-amber)', fontWeight: 600 }}>
                          {b.player2_name ? `${b.player2_name} (${b.player2_rating} pts ${b.player2_streak > 0 ? `🔥${b.player2_streak}` : ''})` : 'Waiting for opponent...'}
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

      {/* ========================================== */}
      {/* ANIMATED MATCHMAKING RADAR OVERLAY MODAL */}
      {/* ========================================== */}
      {isSearching && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(7, 9, 14, 0.88)',
          backdropFilter: 'blur(16px)',
          zIndex: 3000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1.5rem'
        }}>
          <div className="glass-panel" style={{
            maxWidth: '480px',
            width: '100%',
            padding: '2.5rem',
            textAlign: 'center',
            position: 'relative',
            border: matchedPayload ? '1px solid rgba(0, 242, 254, 0.5)' : '1px solid rgba(244, 63, 94, 0.35)',
            boxShadow: matchedPayload ? 'var(--shadow-glow-cyan)' : 'var(--shadow-glow-battle)'
          }}>
            {!matchedPayload ? (
              <>
                {/* Radar sweep icon */}
                <div style={{ position: 'relative', width: '90px', height: '90px', margin: '0 auto 1.5rem auto' }}>
                  <div style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: '50%',
                    border: '2px dashed rgba(244, 63, 94, 0.4)',
                    animation: 'spin 8s linear infinite'
                  }} />
                  <div style={{
                    position: 'absolute',
                    inset: '12px',
                    borderRadius: '50%',
                    border: '2px solid rgba(0, 242, 254, 0.4)',
                    animation: 'spin 4s linear infinite reverse'
                  }} />
                  <div style={{
                    position: 'absolute',
                    inset: 0,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Radio size={36} color="var(--accent-rose)" className="animate-pulse-subtle" />
                  </div>
                </div>

                <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.7rem', fontWeight: 800, marginBottom: '0.4rem' }}>
                  Searching for Gladiator...
                </h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
                  Matching against players near your skill tier ({ratingRangeMin} - {ratingRangeMax} pts)
                </p>

                <div style={{
                  background: 'rgba(255, 255, 255, 0.04)',
                  padding: '0.85rem 1.25rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '1.75rem',
                  fontFamily: 'var(--font-code)'
                }}>
                  <div style={{ textAlign: 'left' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Queue Elapsed</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>{formattedSearchTime}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Your Rating</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fbbf24' }}>{myRating} pts</div>
                  </div>
                </div>

                <button 
                  onClick={stopMatchmaking}
                  className="secondary-btn"
                  style={{ width: '100%', justifyContent: 'center', padding: '0.7rem' }}
                >
                  <X size={16} />
                  <span>Cancel Matchmaking</span>
                </button>
              </>
            ) : (
              /* MATCH FOUND BANNER */
              <div>
                <div style={{
                  width: '72px',
                  height: '72px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #00f2fe, #3b82f6)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '1rem',
                  boxShadow: 'var(--shadow-glow-cyan)'
                }}>
                  <CheckCircle2 size={40} color="#07090e" />
                </div>

                <div style={{ color: 'var(--accent-cyan)', fontSize: '0.85rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.3rem' }}>
                  MATCH FOUND!
                </div>
                <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', fontWeight: 900, marginBottom: '0.5rem' }}>
                  Opponent Found!
                </h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
                  Preparing 1v1 arena... Connecting both gladiators now!
                </p>

                <div className="animate-spin" style={{ width: '24px', height: '24px', border: '3px solid var(--accent-cyan)', borderTopColor: 'transparent', borderRadius: '50%', margin: '0 auto' }} />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
