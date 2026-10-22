import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Send, RotateCcw, Clock, Cpu, CheckCircle2, XCircle, AlertTriangle, ArrowLeft, Terminal, FileCode2 } from 'lucide-react';
import { api } from '../services/api';

export default function CodeWorkspace({ problemId, onBack, onDuelThis }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);
  const [activeConsoleTab, setActiveConsoleTab] = useState('output');

  useEffect(() => {
    fetchProblemDetails();
  }, [problemId]);

  const fetchProblemDetails = async () => {
    try {
      setLoading(true);
      const data = await api.getProblemDetail(problemId);
      setProblem(data);
      // set default starter code
      updateStarterCode(data, language);
    } catch (err) {
      console.error("Failed to load problem", err);
    } finally {
      setLoading(false);
    }
  };

  const updateStarterCode = (prob, lang) => {
    if (!prob) return;
    if (lang === 'python') setCode(prob.starter_code_python);
    else if (lang === 'cpp') setCode(prob.starter_code_cpp);
    else if (lang === 'javascript') setCode(prob.starter_code_javascript);
  };

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    if (problem) {
      updateStarterCode(problem, newLang);
    }
  };

  const handleReset = () => {
    if (problem) {
      updateStarterCode(problem, language);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setSubmissionResult(null);
    setActiveConsoleTab('output');

    try {
      const res = await api.submitCode({
        problem: problem.id,
        language,
        code
      });
      setSubmissionResult(res);
    } catch (err) {
      setSubmissionResult({
        verdict: 'RUNTIME_ERROR',
        error_output: err.message || 'Submission failed. Please make sure you are logged in.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading || !problem) {
    return (
      <div style={{ textAlign: 'center', padding: '6rem 0', color: 'var(--text-muted)' }}>
        <div className="animate-spin" style={{ display: 'inline-block', width: '32px', height: '32px', border: '3px solid rgba(0, 242, 254, 0.2)', borderTopColor: '#00f2fe', borderRadius: '50%', marginBottom: '1rem' }} />
        <div>Preparing workspace environment...</div>
      </div>
    );
  }

  const badgeClass = problem.difficulty === 'EASY' ? 'badge-easy' : problem.difficulty === 'MEDIUM' ? 'badge-medium' : 'badge-hard';

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: 'calc(100vh - 75px)',
      background: 'var(--bg-darker)'
    }}>
      {/* Top action bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.65rem 1.5rem',
        background: 'var(--bg-dark)',
        borderBottom: '1px solid var(--border-subtle)',
        gap: '1rem',
        flexWrap: 'wrap'
      }}>
        {/* Left: back & problem title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button onClick={onBack} className="secondary-btn" style={{ padding: '0.45rem 0.75rem', fontSize: '0.85rem' }}>
            <ArrowLeft size={16} />
            <span>Library</span>
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <span style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '1.1rem' }}>
              {problem.title}
            </span>
            <span className={`badge ${badgeClass}`}>{problem.difficulty}</span>
          </div>
        </div>

        {/* Center: Language selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'var(--bg-surface)', padding: '0.2rem 0.5rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <FileCode2 size={16} color="var(--accent-cyan)" />
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-main)',
                fontSize: '0.85rem',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              <option value="python" style={{ background: '#141b2a' }}>Python 3</option>
              <option value="cpp" style={{ background: '#141b2a' }}>C++ 17</option>
              <option value="javascript" style={{ background: '#141b2a' }}>JavaScript (Node)</option>
            </select>
          </div>

          <button onClick={handleReset} className="secondary-btn" title="Reset starter code" style={{ padding: '0.45rem 0.65rem' }}>
            <RotateCcw size={15} />
          </button>
        </div>

        {/* Right: Submit & Duel buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <button 
            onClick={() => onDuelThis(problem.id)}
            className="battle-btn"
            style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
          >
            <span>Duel on This</span>
          </button>

          <button 
            onClick={handleSubmit} 
            disabled={submitting}
            className="glow-btn"
            style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}
          >
            {submitting ? (
              <>
                <div className="animate-spin" style={{ width: '14px', height: '14px', border: '2px solid #000', borderTopColor: 'transparent', borderRadius: '50%' }} />
                <span>Evaluating...</span>
              </>
            ) : (
              <>
                <Send size={16} />
                <span>Submit Solution</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Split Body */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', flex: 1, overflow: 'hidden' }}>
        {/* Left Pane: Description & Test cases */}
        <div style={{
          overflowY: 'auto',
          padding: '1.75rem',
          borderRight: '1px solid var(--border-subtle)',
          background: 'rgba(13, 17, 26, 0.4)'
        }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.35rem', fontWeight: 800, marginBottom: '0.5rem' }}>
              Description
            </h2>
            <div style={{ color: '#cbd5e1', lineHeight: 1.7, fontSize: '0.92rem', whiteSpace: 'pre-wrap' }}>
              {problem.description}
            </div>
          </div>

          {problem.constraints && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Constraints
              </h3>
              <pre style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.85rem',
                fontSize: '0.82rem',
                color: 'var(--accent-amber)',
                fontFamily: 'var(--font-code)'
              }}>
                {problem.constraints}
              </pre>
            </div>
          )}

          {/* Sample Test Cases */}
          {problem.sample_tests && problem.sample_tests.length > 0 && (
            <div>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Sample Test Cases
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                {problem.sample_tests.map((sample, idx) => (
                  <div key={sample.id} style={{
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '0.85rem'
                  }}>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', fontWeight: 700, marginBottom: '0.5rem' }}>
                      EXAMPLE #{idx + 1}
                    </div>
                    <div style={{ marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.2rem' }}>Input:</span>
                      <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '0.4rem 0.6rem', borderRadius: '4px', fontSize: '0.82rem', fontFamily: 'var(--font-code)', color: '#93c5fd' }}>
                        {sample.input_data}
                      </pre>
                    </div>
                    <div>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.2rem' }}>Expected Output:</span>
                      <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '0.4rem 0.6rem', borderRadius: '4px', fontSize: '0.82rem', fontFamily: 'var(--font-code)', color: '#86efac' }}>
                        {sample.expected_output}
                      </pre>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Pane: Monaco Code Editor + Output Drawer */}
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
          {/* Editor Container */}
          <div style={{ flex: 1, minHeight: '320px', position: 'relative' }}>
            <Editor
              height="100%"
              theme="vs-dark"
              language={language === 'cpp' ? 'cpp' : language === 'javascript' ? 'javascript' : 'python'}
              value={code}
              onChange={(val) => setCode(val || '')}
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

          {/* Console / Output Drawer */}
          <div style={{
            height: '240px',
            borderTop: '1px solid var(--border-subtle)',
            background: 'var(--bg-surface)',
            display: 'flex',
            flexDirection: 'column'
          }}>
            {/* Drawer Tabs */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0.4rem 1rem',
              background: 'rgba(13, 17, 26, 0.9)',
              borderBottom: '1px solid var(--border-subtle)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Terminal size={15} color="var(--accent-cyan)" />
                <span style={{ fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Execution Verdict & Output
                </span>
              </div>

              {submissionResult && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <span style={{
                    fontSize: '0.8rem',
                    fontWeight: 700,
                    color: submissionResult.verdict === 'ACCEPTED' ? '#34d399' : '#f87171',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.35rem'
                  }}>
                    {submissionResult.verdict === 'ACCEPTED' ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                    {submissionResult.verdict}
                  </span>
                  {submissionResult.total_test_cases > 0 && (
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Passed: {submissionResult.test_cases_passed} / {submissionResult.total_test_cases}
                    </span>
                  )}
                  {submissionResult.execution_time_ms !== undefined && (
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                      {submissionResult.execution_time_ms} ms
                    </span>
                  )}
                </div>
              )}
            </div>

            {/* Drawer Content */}
            <div style={{
              flex: 1,
              overflowY: 'auto',
              padding: '0.85rem 1rem',
              fontFamily: 'var(--font-code)',
              fontSize: '0.85rem'
            }}>
              {submitting ? (
                <div style={{ color: 'var(--accent-cyan)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div className="animate-spin" style={{ width: '14px', height: '14px', border: '2px solid var(--accent-cyan)', borderTopColor: 'transparent', borderRadius: '50%' }} />
                  <span>Running solution through sandbox evaluation...</span>
                </div>
              ) : submissionResult ? (
                <div>
                  <div style={{
                    color: submissionResult.verdict === 'ACCEPTED' ? '#86efac' : '#fca5a5',
                    whiteSpace: 'pre-wrap',
                    lineHeight: 1.5
                  }}>
                    {submissionResult.error_output || (submissionResult.verdict === 'ACCEPTED' ? 'All test cases passed cleanly!' : 'Evaluation concluded.')}
                  </div>
                </div>
              ) : (
                <div style={{ color: 'var(--text-dim)', fontStyle: 'italic' }}>
                  Click "Submit Solution" to run your code against automated test cases.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
