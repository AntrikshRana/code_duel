import React from 'react';
import { Swords, Code2, Trophy, Flame, User, LogOut, Sparkles } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, user, onOpenAuth, onLogout }) {
  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      background: 'rgba(13, 17, 26, 0.85)',
      backdropFilter: 'blur(16px)',
      borderBottom: '1px solid var(--border-subtle)',
      padding: '0.75rem 2rem'
    }}>
      <div style={{
        maxWidth: '1440px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '1rem'
      }}>
        {/* Brand */}
        <div 
          onClick={() => setActiveTab('lobby')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            cursor: 'pointer',
            userSelect: 'none'
          }}
        >
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #f43f5e, #8b5cf6)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(244, 63, 94, 0.4)'
          }}>
            <Swords size={22} color="#ffffff" />
          </div>
          <div>
            <div style={{
              fontFamily: 'var(--font-display)',
              fontSize: '1.35rem',
              fontWeight: 800,
              letterSpacing: '-0.02em',
              background: 'linear-gradient(90deg, #ffffff, #94a3b8)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              lineHeight: 1.1
            }}>
              CODE<span style={{ color: '#00f2fe', WebkitTextFillColor: '#00f2fe' }}>DUEL</span>
            </div>
            <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase', fontWeight: 600 }}>
              1v1 Code Arena
            </div>
          </div>
        </div>

        {/* Navigation items */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button 
            onClick={() => setActiveTab('lobby')}
            className="secondary-btn"
            style={{
              background: activeTab === 'lobby' ? 'rgba(244, 63, 94, 0.15)' : 'transparent',
              borderColor: activeTab === 'lobby' ? 'rgba(244, 63, 94, 0.4)' : 'transparent',
              color: activeTab === 'lobby' ? '#f43f5e' : 'var(--text-muted)'
            }}
          >
            <Swords size={18} />
            <span>1v1 Arena</span>
          </button>

          <button 
            onClick={() => setActiveTab('problems')}
            className="secondary-btn"
            style={{
              background: activeTab === 'problems' ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
              borderColor: activeTab === 'problems' ? 'rgba(0, 242, 254, 0.4)' : 'transparent',
              color: activeTab === 'problems' ? '#00f2fe' : 'var(--text-muted)'
            }}
          >
            <Code2 size={18} />
            <span>Problem Library</span>
          </button>

          <button 
            onClick={() => setActiveTab('leaderboard')}
            className="secondary-btn"
            style={{
              background: activeTab === 'leaderboard' ? 'rgba(251, 191, 36, 0.15)' : 'transparent',
              borderColor: activeTab === 'leaderboard' ? 'rgba(251, 191, 36, 0.4)' : 'transparent',
              color: activeTab === 'leaderboard' ? '#fbbf24' : 'var(--text-muted)'
            }}
          >
            <Trophy size={18} />
            <span>Leaderboard</span>
          </button>
        </nav>

        {/* User state / Auth */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                background: 'rgba(20, 27, 42, 0.8)',
                padding: '0.4rem 0.9rem',
                borderRadius: 'var(--radius-full)',
                border: '1px solid var(--border-subtle)'
              }}>
                <div style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #3b82f6, #00f2fe)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.8rem',
                  color: '#07090e'
                }}>
                  {user.username.charAt(0).toUpperCase()}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{user.username}</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', marginTop: '1px' }}>
                    <span style={{ fontSize: '0.7rem', color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                      <Flame size={12} fill="#fbbf24" />
                      {user.profile?.rating ?? 0} pts
                    </span>
                    {(user.profile?.current_streak ?? 0) > 0 && (
                      <span 
                        title={`Current Win Streak: ${user.profile.current_streak}`}
                        style={{ 
                          fontSize: '0.65rem', 
                          fontWeight: 700, 
                          color: '#f87171', 
                          background: 'rgba(239, 68, 68, 0.2)', 
                          border: '1px solid rgba(239, 68, 68, 0.4)',
                          padding: '0.05rem 0.35rem', 
                          borderRadius: '4px',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '2px'
                        }}
                      >
                        🔥 {user.profile.current_streak}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <button 
                onClick={onLogout}
                className="secondary-btn"
                title="Logout"
                style={{ padding: '0.5rem', borderRadius: '50%' }}
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <button onClick={onOpenAuth} className="glow-btn">
              <Sparkles size={16} />
              <span>Enter Arena</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
