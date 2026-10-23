import React, { useState } from 'react';
import { X, Sparkles, User, Lock, Mail, ArrowRight, LogIn, UserPlus, Eye, EyeOff, Zap, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [suggestedRegister, setSuggestedRegister] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuggestedRegister(null);
    setLoading(true);

    const cleanUsername = username.trim();
    const cleanPassword = password.trim();

    if (!cleanUsername) {
      setError('Please enter a username.');
      setLoading(false);
      return;
    }
    if (!cleanPassword || cleanPassword.length < 6) {
      setError('Password must be at least 6 characters long.');
      setLoading(false);
      return;
    }

    try {
      if (isRegister) {
        const res = await api.register(cleanUsername, email.trim(), cleanPassword);
        onAuthSuccess(res.user);
        onClose();
      } else {
        const res = await api.login(cleanUsername, cleanPassword);
        onAuthSuccess(res.user);
        onClose();
      }
    } catch (err) {
      const code = err.data?.code;
      const msg = err.message || '';

      if (code === 'USER_NOT_FOUND' || msg.toLowerCase().includes('no account found') || msg.toLowerCase().includes('no active account')) {
        setSuggestedRegister(cleanUsername);
        setError(`No account found for "${cleanUsername}". Would you like to create one now?`);
      } else if (code === 'INVALID_PASSWORD' || msg.toLowerCase().includes('incorrect password')) {
        setError('Incorrect password for this username. Please double-check and try again.');
      } else {
        setError(msg || 'Authentication failed. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleQuickRegisterFromPrompt = async () => {
    if (!suggestedRegister || !password) {
      setIsRegister(true);
      setError('');
      setSuggestedRegister(null);
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await api.register(suggestedRegister, email.trim(), password.trim());
      onAuthSuccess(res.user);
      onClose();
    } catch (err) {
      setIsRegister(true);
      setError(err.message || 'Registration failed. Please try a different username.');
    } finally {
      setLoading(false);
    }
  };

  const handleGuestLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.guestLogin(username.trim());
      onAuthSuccess(res.user);
      onClose();
    } catch (err) {
      setError(err.message || 'Guest login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoAccount = () => {
    setIsRegister(false);
    setUsername('demo_coder');
    setPassword('password123');
    setError('');
    setSuggestedRegister(null);
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 1000,
      background: 'rgba(5, 8, 15, 0.88)',
      backdropFilter: 'blur(10px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem',
      animation: 'fadeIn 0.2s ease-out'
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '430px',
        padding: '2rem',
        position: 'relative',
        border: '1px solid rgba(255, 255, 255, 0.12)',
        borderRadius: '16px',
        boxShadow: '0 24px 60px rgba(0, 0, 0, 0.7)'
      }}>
        {/* Close Button */}
        <button 
          onClick={onClose}
          aria-label="Close auth modal"
          style={{
            position: 'absolute',
            top: '1.25rem',
            right: '1.25rem',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '0.4rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.15s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.color = '#fff'}
          onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
        >
          <X size={18} />
        </button>

        {/* Tab Switcher */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '0.4rem',
          background: 'rgba(15, 20, 32, 0.8)',
          padding: '0.35rem',
          borderRadius: '10px',
          border: '1px solid var(--border-subtle)',
          marginBottom: '1.5rem'
        }}>
          <button
            type="button"
            onClick={() => { setIsRegister(false); setError(''); setSuggestedRegister(null); }}
            style={{
              background: !isRegister ? 'var(--grad-primary)' : 'transparent',
              color: !isRegister ? '#07090e' : 'var(--text-muted)',
              border: 'none',
              padding: '0.6rem',
              borderRadius: '7px',
              fontWeight: 700,
              fontSize: '0.88rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.45rem',
              transition: 'all 0.2s ease'
            }}
          >
            <LogIn size={15} />
            <span>Sign In</span>
          </button>

          <button
            type="button"
            onClick={() => { setIsRegister(true); setError(''); setSuggestedRegister(null); }}
            style={{
              background: isRegister ? 'var(--grad-primary)' : 'transparent',
              color: isRegister ? '#07090e' : 'var(--text-muted)',
              border: 'none',
              padding: '0.6rem',
              borderRadius: '7px',
              fontWeight: 700,
              fontSize: '0.88rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.45rem',
              transition: 'all 0.2s ease'
            }}
          >
            <UserPlus size={15} />
            <span>Create Account</span>
          </button>
        </div>

        {/* Header Title */}
        <div style={{ textAlign: 'center', marginBottom: '1.3rem' }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.45rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
            {isRegister ? 'Create Your Coder Profile' : 'Sign in to CodeDuel'}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.3rem', lineHeight: 1.4 }}>
            {isRegister ? 'Pick a username & password to join battles and save ratings.' : 'Welcome back! Enter your handle and password below.'}
          </p>
        </div>

        {/* Error / Suggestion Banner */}
        {error && (
          <div style={{
            background: suggestedRegister ? 'rgba(0, 242, 254, 0.08)' : 'rgba(244, 63, 94, 0.12)',
            border: suggestedRegister ? '1px solid rgba(0, 242, 254, 0.35)' : '1px solid rgba(244, 63, 94, 0.35)',
            color: suggestedRegister ? '#00f2fe' : '#f87171',
            padding: '0.8rem 1rem',
            borderRadius: '10px',
            fontSize: '0.84rem',
            marginBottom: '1.25rem',
            lineHeight: 1.45
          }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
              <ShieldAlert size={16} style={{ marginTop: '0.15rem', flexShrink: 0 }} />
              <div style={{ flex: 1 }}>
                <div>{error}</div>
                {suggestedRegister && (
                  <button
                    type="button"
                    onClick={handleQuickRegisterFromPrompt}
                    style={{
                      marginTop: '0.5rem',
                      background: 'var(--grad-primary)',
                      border: 'none',
                      color: '#07090e',
                      padding: '0.35rem 0.8rem',
                      borderRadius: '6px',
                      fontSize: '0.8rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.35rem'
                    }}
                  >
                    <span>Create "{suggestedRegister}" Account</span>
                    <ArrowRight size={13} />
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem', fontWeight: 600 }}>
              Username {isRegister ? '' : 'or Email'}
            </label>
            <div style={{ position: 'relative' }}>
              <User size={16} style={{ position: 'absolute', left: '0.9rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
              <input 
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder={isRegister ? 'e.g. alex_coder' : 'username or email'}
                style={{
                  width: '100%',
                  background: 'rgba(15, 20, 32, 0.85)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '9px',
                  padding: '0.7rem 0.9rem 0.7rem 2.5rem',
                  color: 'var(--text-main)',
                  fontSize: '0.92rem',
                  outline: 'none',
                  transition: 'border-color 0.15s ease'
                }}
                onFocus={(e) => e.target.style.borderColor = 'rgba(0, 242, 254, 0.5)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--border-subtle)'}
              />
            </div>
          </div>

          {isRegister && (
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem', fontWeight: 600 }}>
                Email <span style={{ color: 'var(--text-dim)', fontWeight: 400 }}>(optional)</span>
              </label>
              <div style={{ position: 'relative' }}>
                <Mail size={16} style={{ position: 'absolute', left: '0.9rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
                <input 
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="yourname@gmail.com"
                  style={{
                    width: '100%',
                    background: 'rgba(15, 20, 32, 0.85)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '9px',
                    padding: '0.7rem 0.9rem 0.7rem 2.5rem',
                    color: 'var(--text-main)',
                    fontSize: '0.92rem',
                    outline: 'none',
                    transition: 'border-color 0.15s ease'
                  }}
                  onFocus={(e) => e.target.style.borderColor = 'rgba(0, 242, 254, 0.5)'}
                  onBlur={(e) => e.target.style.borderColor = 'var(--border-subtle)'}
                />
              </div>
            </div>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem', fontWeight: 600 }}>
              Password <span style={{ color: 'var(--text-dim)', fontWeight: 400 }}>(min. 6 characters)</span>
            </label>
            <div style={{ position: 'relative' }}>
              <Lock size={16} style={{ position: 'absolute', left: '0.9rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
              <input 
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{
                  width: '100%',
                  background: 'rgba(15, 20, 32, 0.85)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '9px',
                  padding: '0.7rem 2.5rem 0.7rem 2.5rem',
                  color: 'var(--text-main)',
                  fontSize: '0.92rem',
                  outline: 'none',
                  transition: 'border-color 0.15s ease'
                }}
                onFocus={(e) => e.target.style.borderColor = 'rgba(0, 242, 254, 0.5)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--border-subtle)'}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '0.8rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-dim)',
                  cursor: 'pointer',
                  padding: '0.2rem',
                  display: 'flex',
                  alignItems: 'center'
                }}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="glow-btn"
            style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem', padding: '0.75rem' }}
          >
            <span>{loading ? 'Authenticating...' : (isRegister ? 'Register & Start Dueling' : 'Sign In')}</span>
            <ArrowRight size={16} />
          </button>
        </form>

        {/* Helpful Alternatives: Demo / Guest */}
        <div style={{ marginTop: '1.5rem', paddingTop: '1.2rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={fillDemoAccount}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-muted)',
                fontSize: '0.78rem',
                cursor: 'pointer',
                textDecoration: 'underline',
                padding: '0.2rem'
              }}
            >
              Fill demo account (<code style={{ color: '#00f2fe' }}>demo_coder</code>)
            </button>

            <button
              type="button"
              onClick={handleGuestLogin}
              disabled={loading}
              style={{
                background: 'rgba(0, 242, 254, 0.1)',
                border: '1px solid rgba(0, 242, 254, 0.25)',
                color: '#00f2fe',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer',
                borderRadius: '6px',
                padding: '0.35rem 0.75rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.35rem'
              }}
            >
              <Zap size={13} />
              <span>Instant Guest Mode</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
