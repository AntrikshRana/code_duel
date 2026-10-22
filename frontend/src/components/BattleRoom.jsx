import React, { useState, useEffect, useRef } from 'react';
import Editor from '@monaco-editor/react';
import confetti from 'canvas-confetti';
import { Swords, Clock, Send, Trophy, ArrowLeft, Terminal, Shield, CheckCircle2, XCircle, AlertCircle, Sparkles, Copy, Check } from 'lucide-react';
import { api } from '../services/api';
import { BattleSocket } from '../services/websocket';

export default function BattleRoom({ roomCode, user, onLeave }) {
  const [battle, setBattle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);
  
  // Realtime opponent stats
  const [opponentProgress, setOpponentProgress] = useState({
    status: 'idle',
    testCasesPassed: 0,
    totalTestCases: 0
  });

  const [timeLeft, setTimeLeft] = useState(900); // 15 mins
  const [copiedCode, setCopiedCode] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  
  const socketRef = useRef(null);
  const timerRef = useRef(null);

  useEffect(() => {
    fetchBattleData();

    // Setup WebSocket
    socketRef.current = new BattleSocket(
      roomCode,
      (msg) => handleSocketMessage(msg),
      (status) => setWsConnected(status === 'connected')
    );

    return () => {
      if (socketRef.current) socketRef.current.close();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [roomCode]);

  // Countdown timer
  useEffect(() => {
    if (battle?.status === 'IN_PROGRESS' || battle?.status === 'COUNTDOWN') {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [battle?.status]);

  const fetchBattleData = async () => {
    try {
      const data = await api.getBattle(roomCode);
      setBattle(data);
      if (data.problem_details) {
        if (language === 'python') setCode(data.problem_details.starter_code_python);
        else if (language === 'cpp') setCode(data.problem_details.starter_code_cpp);
        else if (language === 'javascript') setCode(data.problem_details.starter_code_javascript);
      }
      if (data.status === 'COMPLETED' && data.winner_name === user?.username) {
        triggerVictoryConfetti();
      }
    } catch (err) {
      console.error("Failed to load battle data", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSocketMessage = (data) => {
    const { action, payload } = data;

    if (action === 'player_joined') {
      fetchBattleData();
    } else if (action === 'code_progress') {
      if (payload.username !== user?.username) {
        setOpponentProgress({
          status: payload.status,
          testCasesPassed: payload.passed || 0,
          totalTestCases: payload.total || 0
        });
      }
    } else if (action === 'battle_won') {
      fetchBattleData();
      if (payload.winner === user?.username) {
        triggerVictoryConfetti();
      }
    }
  };

  const triggerVictoryConfetti = () => {
    confetti({
      particleCount: 120,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  const handleCopyRoomCode = () => {
    navigator.clipboard.writeText(roomCode);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleEditorChange = (val) => {
    setCode(val || '');
    // Broadcast progress debounce
    if (socketRef.current && user) {
      socketRef.current.send('code_progress', {
        username: user.username,
        status: 'coding'
      });
    }
  };

  const handleSubmit = async () => {
    if (!battle || !battle.problem) return;
    setSubmitting(true);
    setSubmissionResult(null);

    try {
      const res = await api.submitCode({
        problem: battle.problem,
        battle: battle.id,
        language,
        code
      });
      setSubmissionResult(res);

      // Notify opponent via websocket
      if (socketRef.current && user) {
        socketRef.current.send('code_progress', {
          username: user.username,
          status: res.verdict === 'ACCEPTED' ? 'solved' : 'submitted',
          passed: res.test_cases_passed,
          total: res.total_test_cases
        });

        if (res.verdict === 'ACCEPTED') {
          socketRef.current.send('battle_won', {
            winner: user.username
          });
          triggerVictoryConfetti();
        }
      }

      // Re-fetch updated battle state
      fetchBattleData();
    } catch (err) {
      setSubmissionResult({
        verdict: 'RUNTIME_ERROR',
        error_output: err.message || 'Submission error.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading || !battle) {
    return (
      <div style={{ textAlign: 'center', padding: '6rem 0', color: 'var(--text-muted)' }}>
        <div className="animate-spin" style={{ display: 'inline-block', width: '32px', height: '32px', border: '3px solid rgba(244, 63, 94, 0.2)', borderTopColor: '#f43f5e', borderRadius: '50%', marginBottom: '1rem' }} />
        <div>Connecting to Battle Room #{roomCode}...</div>
      </div>
    );
  }

  const isPlayer1 = user?.username === battle.player1_name;
  const isPlayer2 = user?.username === battle.player2_name;
  const myRating = isPlayer1 ? battle.player1_rating : battle.player2_rating;
  const oppName = isPlayer1 ? battle.player2_name : battle.player1_name;
  const oppRating = isPlayer1 ? battle.player2_rating : battle.player1_rating;

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  const isCompleted = battle.status === 'COMPLETED';
  const isWinner = battle.winner_name === user?.username;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 75px)', background: 'var(--bg-darker)' }}>
      {/* Top 1v1 Battle Status Bar */}
      <div style={{
        padding: '0.65rem 1.5rem',
        background: 'var(--bg-dark)',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        {/* Left: Leave & Room code */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <button onClick={onLeave} className="secondary-btn" style={{ padding: '0.4rem 0.75rem', fontSize: '0.82rem' }}>
            <ArrowLeft size={16} />
            <span>Leave</span>
          </button>

          <div 
            onClick={handleCopyRoomCode}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: 'rgba(255, 255, 255, 0.05)',
              padding: '0.35rem 0.65rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              cursor: 'pointer',
              fontSize: '0.82rem',
              fontFamily: 'var(--font-code)'
            }}
            title="Click to copy room code"
          >
            <span style={{ color: 'var(--text-muted)' }}>ROOM:</span>
            <span style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>#{roomCode}</span>
            {copiedCode ? <Check size={14} color="#34d399" /> : <Copy size={14} color="var(--text-dim)" />}
          </div>
        </div>

        {/* Center: 1v1 Matchup Head-to-Head */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          {/* Player 1 (You) */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', textAlign: 'right' }}>
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#38bdf8' }}>
                {user?.username || 'You'} (You)
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                {myRating || 1200} pts
              </div>
            </div>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #00f2fe, #3b82f6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '0.85rem',
              color: '#07090e'
            }}>
              {(user?.username || 'Y').charAt(0).toUpperCase()}
            </div>
          </div>

          {/* VS & Timer */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontFamily: 'var(--font-code)',
              fontWeight: 800,
              fontSize: '1.25rem',
              color: timeLeft < 180 ? '#f87171' : '#ffffff'
            }}>
              <Clock size={16} color={timeLeft < 180 ? '#f87171' : 'var(--accent-cyan)'} />
              {formattedTime}
            </div>
            <div style={{ fontSize: '0.65rem', color: 'var(--accent-rose)', fontWeight: 800, letterSpacing: '0.1em' }}>
              1v1 CLASH
            </div>
          </div>

          {/* Player 2 (Opponent) */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              background: oppName ? 'linear-gradient(135deg, #f43f5e, #a855f7)' : 'rgba(255, 255, 255, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '0.85rem',
              color: '#ffffff'
            }}>
              {oppName ? oppName.charAt(0).toUpperCase() : '?'}
            </div>
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: oppName ? '#f43f5e' : 'var(--accent-amber)' }}>
                {oppName || 'Waiting for Challenger...'}
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                {oppName ? `${oppRating || 1200} pts` : 'Share room code to invite'}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Submit Button */}
        <div>
          <button 
            onClick={handleSubmit}
            disabled={submitting || isCompleted || !oppName}
            className="glow-btn"
            style={{ padding: '0.45rem 1.25rem', fontSize: '0.85rem' }}
          >
            {submitting ? (
              <>
                <div className="animate-spin" style={{ width: '14px', height: '14px', border: '2px solid #000', borderTopColor: 'transparent', borderRadius: '50%' }} />
                <span>Evaluating...</span>
              </>
            ) : (
              <>
                <Send size={15} />
                <span>Submit Solution</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Opponent Live Status Bar */}
      {oppName && (
        <div style={{
          background: 'rgba(20, 27, 42, 0.8)',
          padding: '0.4rem 1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          fontSize: '0.78rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          color: 'var(--text-muted)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#34d399', display: 'inline-block' }} />
            <span>Opponent status: <strong style={{ color: '#ffffff' }}>{opponentProgress.status === 'coding' ? 'Typing solution...' : opponentProgress.status === 'submitted' ? `Tested (${opponentProgress.testCasesPassed}/${opponentProgress.totalTestCases} passed)` : 'Observing challenge...'}</strong></span>
          </div>

          <div style={{ color: 'var(--text-dim)' }}>
            WebSocket: {wsConnected ? <span style={{ color: '#34d399' }}>Live Realtime</span> : <span style={{ color: '#f59e0b' }}>Reconnecting...</span>}
          </div>
        </div>
      )}

      {/* Main Dual Pane Arena */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.25fr', flex: 1, overflow: 'hidden' }}>
        {/* Left: Problem details */}
        <div style={{ overflowY: 'auto', padding: '1.5rem', borderRight: '1px solid var(--border-subtle)' }}>
          <div style={{ marginBottom: '1.25rem' }}>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.35rem', fontWeight: 800, marginBottom: '0.4rem' }}>
              {battle.problem_details?.title}
            </h2>
            <div style={{ color: '#cbd5e1', lineHeight: 1.6, fontSize: '0.9rem', whiteSpace: 'pre-wrap' }}>
              {battle.problem_details?.description}
            </div>
          </div>

          {battle.problem_details?.constraints && (
            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.35rem', textTransform: 'uppercase' }}>
                Constraints
              </div>
              <pre style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '6px', fontSize: '0.8rem', color: 'var(--accent-amber)', fontFamily: 'var(--font-code)' }}>
                {battle.problem_details.constraints}
              </pre>
            </div>
          )}

          {battle.problem_details?.sample_tests && (
            <div>
              <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                Sample Tests
              </div>
              {battle.problem_details.sample_tests.map((st, i) => (
                <div key={st.id} style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '6px', marginBottom: '0.65rem' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700, marginBottom: '0.3rem' }}>EXAMPLE #{i + 1}</div>
                  <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '0.35rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', color: '#93c5fd', fontFamily: 'var(--font-code)' }}>{st.input_data}</pre>
                  <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '0.35rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', color: '#86efac', fontFamily: 'var(--font-code)', marginTop: '0.3rem' }}>{st.expected_output}</pre>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right: Monaco Editor + Output Drawer */}
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
          {/* Editor */}
          <div style={{ flex: 1, position: 'relative' }}>
            <Editor
              height="100%"
              theme="vs-dark"
              language={language === 'cpp' ? 'cpp' : language === 'javascript' ? 'javascript' : 'python'}
              value={code}
              onChange={handleEditorChange}
              options={{
                fontSize: 14,
                fontFamily: 'JetBrains Mono',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                automaticLayout: true,
                padding: { top: 12, bottom: 12 }
              }}
            />
          </div>

          {/* Result Console */}
          <div style={{ height: '180px', borderTop: '1px solid var(--border-subtle)', background: 'var(--bg-surface)', padding: '0.75rem 1rem', overflowY: 'auto', fontFamily: 'var(--font-code)', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.35rem' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                Your Verdict:
              </span>
              {submissionResult && (
                <span style={{
                  color: submissionResult.verdict === 'ACCEPTED' ? '#34d399' : '#f87171',
                  fontWeight: 700
                }}>
                  {submissionResult.verdict} ({submissionResult.test_cases_passed}/{submissionResult.total_test_cases})
                </span>
              )}
            </div>

            {submissionResult ? (
              <div style={{ color: submissionResult.verdict === 'ACCEPTED' ? '#86efac' : '#fca5a5', whiteSpace: 'pre-wrap' }}>
                {submissionResult.error_output || (submissionResult.verdict === 'ACCEPTED' ? 'Solution accepted! All tests cleared!' : '')}
              </div>
            ) : (
              <div style={{ color: 'var(--text-dim)', fontStyle: 'italic' }}>
                Submit when ready. The fastest accepted solution takes the match!
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Duel Completed Modal */}
      {isCompleted && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(7, 9, 14, 0.9)',
          backdropFilter: 'blur(16px)',
          zIndex: 2000,
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
            border: isWinner ? '1px solid rgba(0, 242, 254, 0.4)' : '1px solid rgba(244, 63, 94, 0.4)',
            boxShadow: isWinner ? 'var(--shadow-glow-cyan)' : 'var(--shadow-glow-battle)'
          }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: isWinner ? 'linear-gradient(135deg, #00f2fe, #4facfe)' : 'linear-gradient(135deg, #f43f5e, #a855f7)',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
              boxShadow: isWinner ? 'var(--shadow-glow-cyan)' : 'var(--shadow-glow-battle)'
            }}>
              <Trophy size={32} color={isWinner ? '#07090e' : '#ffffff'} />
            </div>

            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', fontWeight: 900, marginBottom: '0.5rem' }}>
              {isWinner ? 'VICTORY ACHILLES!' : 'DEFEAT'}
            </h2>

            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
              {isWinner ? (
                <>
                  Congratulations! You solved <strong style={{ color: '#ffffff' }}>{battle.problem_details?.title}</strong> first.
                </>
              ) : (
                <>
                  <strong style={{ color: '#f43f5e' }}>{battle.winner_name}</strong> submitted the winning accepted solution first.
                </>
              )}
            </p>

            <div style={{
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '1rem',
              marginBottom: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-around'
            }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Rating Adjustment</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: isWinner ? '#34d399' : '#f87171' }}>
                  {isWinner ? '+25 pts' : '-15 pts'}
                </div>
              </div>
              <div style={{ width: '1px', height: '32px', background: 'var(--border-subtle)' }} />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Battle Status</div>
                <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                  COMPLETED
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
              <button onClick={onLeave} className="glow-btn" style={{ padding: '0.65rem 1.75rem' }}>
                <span>Return to Lobby</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
