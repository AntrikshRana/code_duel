import React, { useState, useEffect } from 'react';
import { Users, Swords, Radio, ShieldAlert, Sparkles, Activity } from 'lucide-react';
import { api } from '../services/api';

export default function OnlinePresenceBar() {
  const [stats, setStats] = useState({
    online_users: 1,
    in_battles: 0,
    in_queue: 0,
    total_registered: 1
  });

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 6000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const data = await api.getOnlineStats();
      if (data) setStats(data);
    } catch (e) {
      // ignore
    }
  };

  return (
    <footer style={{
      position: 'sticky',
      bottom: 0,
      zIndex: 90,
      background: 'rgba(7, 9, 14, 0.92)',
      backdropFilter: 'blur(16px)',
      borderTop: '1px solid var(--border-subtle)',
      padding: '0.55rem 2rem'
    }}>
      <div style={{
        maxWidth: '1440px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.75rem',
        fontSize: '0.8rem'
      }}>
        {/* Left: Online Status Indicator */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            background: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: 'var(--radius-full)',
            padding: '0.25rem 0.75rem',
            color: '#34d399',
            fontWeight: 700
          }}>
            <span style={{
              width: '7px',
              height: '7px',
              borderRadius: '50%',
              background: '#34d399',
              boxShadow: '0 0 10px #34d399',
              display: 'inline-block'
            }} className="animate-pulse-subtle" />
            <span>{stats.online_users} {stats.online_users === 1 ? 'Gladiator' : 'Gladiators'} Online</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}>
            <Swords size={14} color="var(--accent-rose)" />
            <span><strong style={{ color: '#ffffff' }}>{stats.in_battles}</strong> in active clashes</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}>
            <Activity size={14} color="var(--accent-cyan)" />
            <span><strong style={{ color: '#ffffff' }}>{stats.in_queue}</strong> in matchmaking queue</span>
          </div>
        </div>

        {/* Right: Server Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-dim)', fontSize: '0.75rem' }}>
          <span>Code Duel Global Arena</span>
          <span style={{ color: 'var(--border-subtle)' }}>•</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <Users size={12} />
            {stats.total_registered} Registered Coders
          </span>
        </div>
      </div>
    </footer>
  );
}
