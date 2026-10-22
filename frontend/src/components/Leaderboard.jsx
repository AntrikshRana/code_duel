import React, { useState, useEffect } from 'react';
import { Trophy, Medal, Flame, Swords, Shield, Award } from 'lucide-react';
import { api } from '../services/api';

export default function Leaderboard() {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const data = await api.getLeaderboard();
      setLeaders(data);
    } catch (err) {
      console.error("Failed to fetch leaderboard", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1080px', margin: '2rem auto', padding: '0 1.5rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(251, 191, 36, 0.15)',
          color: '#fbbf24',
          border: '1px solid rgba(251, 191, 36, 0.3)',
          borderRadius: 'var(--radius-full)',
          padding: '0.35rem 0.9rem',
          fontSize: '0.78rem',
          fontWeight: 700,
          textTransform: 'uppercase',
          marginBottom: '0.75rem'
        }}>
          <Trophy size={15} />
          Hall of Gladiators
        </div>

        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '2.6rem', fontWeight: 900, letterSpacing: '-0.02em' }}>
          GLOBAL <span style={{ color: '#fbbf24' }}>LEADERBOARD</span>
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.35rem' }}>
          Ranked by competitive rating points earned through real-time head-to-head 1v1 battles.
        </p>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-muted)' }}>
          <div className="animate-spin" style={{ display: 'inline-block', width: '32px', height: '32px', border: '3px solid rgba(251, 191, 36, 0.2)', borderTopColor: '#fbbf24', borderRadius: '50%', marginBottom: '1rem' }} />
          <div>Retrieving rankings...</div>
        </div>
      ) : (
        <div className="glass-panel" style={{ overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '80px 1fr 140px 140px 120px',
            padding: '1rem 1.5rem',
            background: 'var(--bg-dark)',
            borderBottom: '1px solid var(--border-subtle)',
            fontSize: '0.78rem',
            fontWeight: 700,
            color: 'var(--text-dim)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            <div>Rank</div>
            <div>Gladiator</div>
            <div style={{ textAlign: 'center' }}>Rating</div>
            <div style={{ textAlign: 'center' }}>Win Rate</div>
            <div style={{ textAlign: 'right' }}>W / L</div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {leaders.map((p, index) => {
              const rank = index + 1;
              const isTop3 = rank <= 3;
              const rankColor = rank === 1 ? '#fbbf24' : rank === 2 ? '#e2e8f0' : rank === 3 ? '#b45309' : 'var(--text-dim)';

              return (
                <div 
                  key={p.username}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '80px 1fr 140px 140px 120px',
                    padding: '1.1rem 1.5rem',
                    alignItems: 'center',
                    borderBottom: index < leaders.length - 1 ? '1px solid rgba(255, 255, 255, 0.04)' : 'none',
                    background: isTop3 ? 'rgba(255, 255, 255, 0.015)' : 'transparent',
                    transition: 'background 0.15s ease'
                  }}
                >
                  {/* Rank */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    {rank === 1 ? (
                      <Medal size={20} color="#fbbf24" />
                    ) : rank === 2 ? (
                      <Medal size={20} color="#e2e8f0" />
                    ) : rank === 3 ? (
                      <Medal size={20} color="#b45309" />
                    ) : (
                      <span style={{ fontFamily: 'var(--font-code)', fontWeight: 700, color: rankColor, fontSize: '0.95rem' }}>
                        #{rank}
                      </span>
                    )}
                  </div>

                  {/* Username & Avatar */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                    <div style={{
                      width: '36px',
                      height: '36px',
                      borderRadius: '50%',
                      background: isTop3 ? 'linear-gradient(135deg, #f59e0b, #ef4444)' : 'rgba(255, 255, 255, 0.08)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      color: '#ffffff'
                    }}>
                      {p.username.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem', color: isTop3 ? '#ffffff' : 'var(--text-main)' }}>
                        {p.username}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>
                        {p.bio || 'Duel Arena Veteran'}
                      </div>
                    </div>
                  </div>

                  {/* Rating */}
                  <div style={{ textAlign: 'center' }}>
                    <span style={{
                      fontFamily: 'var(--font-code)',
                      fontWeight: 800,
                      fontSize: '1.05rem',
                      color: '#fbbf24',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.3rem'
                    }}>
                      <Flame size={15} fill="#fbbf24" />
                      {p.rating}
                    </span>
                  </div>

                  {/* Win Rate */}
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
                    <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#34d399' }}>
                      {p.win_rate}%
                    </span>
                    <div style={{ width: '60px', height: '4px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                      <div style={{ width: `${p.win_rate}%`, height: '100%', background: '#34d399' }} />
                    </div>
                  </div>

                  {/* Win / Loss counts */}
                  <div style={{ textAlign: 'right', fontFamily: 'var(--font-code)', fontSize: '0.85rem' }}>
                    <span style={{ color: '#34d399', fontWeight: 700 }}>{p.wins}W</span>
                    <span style={{ color: 'var(--text-dim)', margin: '0 0.35rem' }}>/</span>
                    <span style={{ color: '#f87171', fontWeight: 700 }}>{p.losses}L</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
