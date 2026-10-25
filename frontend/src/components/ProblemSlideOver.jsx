import { useEffect } from 'react';
import { BookOpen, X } from 'lucide-react';

export default function ProblemSlideOver({ problem, isOpen, onToggle, onClose }) {
  useEffect(() => {
    if (!isOpen) return undefined;

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') onClose();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!problem) return null;

  const samples = problem.sample_tests || [];
  const difficultyClass = problem.difficulty === 'EASY'
    ? 'badge-easy'
    : problem.difficulty === 'HARD' ? 'badge-hard' : 'badge-medium';

  return (
    <>
      <button
        type="button"
        className="problem-launcher"
        onClick={onToggle}
        aria-label="Open problem details"
      >
        <BookOpen size={16} />
        <span>Problem</span>
        <span className="problem-launcher-title">{problem.title}</span>
      </button>

      <div className={`problem-overlay${isOpen ? ' is-open' : ''}`} aria-hidden={!isOpen}>
        <button
          type="button"
          className="problem-scrim"
          onClick={onClose}
          tabIndex={isOpen ? 0 : -1}
          aria-label="Close problem details"
        />
        <aside
          className="problem-drawer"
          role="dialog"
          aria-modal="true"
          aria-label="Problem details"
          aria-hidden={!isOpen}
        >
          <div className="problem-drawer-header">
            <div className="problem-drawer-icon"><BookOpen size={18} /></div>
            <div>
              <span className="problem-eyebrow">Challenge brief</span>
              <h2>{problem.title}</h2>
            </div>
            <button
              type="button"
              className="problem-close"
              onClick={onClose}
              aria-label="Close problem details"
              tabIndex={isOpen ? 0 : -1}
            >
              <X size={18} />
            </button>
          </div>

          <div className="problem-drawer-content">
            <span className={`badge ${difficultyClass}`}>{problem.difficulty}</span>

            <section className="problem-section">
              <h3>Overview</h3>
              <p className="problem-description">{problem.description}</p>
            </section>

            {problem.constraints && (
              <section className="problem-section">
                <h3>Constraints</h3>
                <pre className="problem-constraints">{problem.constraints}</pre>
              </section>
            )}

            {samples.length > 0 && (
              <section className="problem-section">
                <h3>Sample tests <span>{samples.length} visible</span></h3>
                <div className="problem-samples">
                  {samples.map((sample, index) => (
                    <article className="problem-sample" key={sample.id ?? index}>
                      <h4>Example {String(index + 1).padStart(2, '0')}</h4>
                      <div className="problem-sample-value">
                        <span>Input</span>
                        <pre>{sample.input_data}</pre>
                      </div>
                      <div className="problem-sample-value">
                        <span>Expected output</span>
                        <pre>{sample.expected_output}</pre>
                      </div>
                    </article>
                  ))}
                </div>
                <p className="problem-footnote">Hidden tests are evaluated securely on the server.</p>
              </section>
            )}
          </div>
        </aside>
      </div>
    </>
  );
}
