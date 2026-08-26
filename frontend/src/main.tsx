import { useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowRight,
  Check,
  ChevronLeft,
  FileText,
  Globe2,
  Landmark,
  Send,
  Sparkles,
  WalletCards,
  RotateCcw,
  ShieldCheck,
  Upload,
  X,
} from 'lucide-react';
import './styles.css';

type TimelineStep = {
  key: string;
  label: string;
  state: 'complete' | 'current' | 'upcoming';
};

type Source = {
  title: string;
  url: string;
  section: string;
  excerpt: string;
};

type Analysis = {
  title: string;
  what_happened: string;
  what_to_do: string[];
  why: string;
  source?: Source | null;
  timeline: TimelineStep[];
  reasonCode?: string;
};

type ClaimType = 'withdrawal' | 'transfer';
type Journey = 'general' | ClaimType;

type ResolutionPlan = {
  title: string;
  summary: string;
  steps: string[];
  guidanceLabel: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

const issuesByClaimType: Record<ClaimType, [string, string][]> = {
  withdrawal: [
    ['kyc', 'KYC verification'],
    ['bank', 'Bank verification'],
    ['service', 'Missing service info'],
    ['conflict', 'Information conflict'],
    ['ready', 'No blocking issue'],
  ],
  transfer: [
    ['transfer_service', 'Missing previous-employment info'],
    ['transfer_conflict', 'Transfer information mismatch'],
    ['transfer_ready', 'Transfer ready to proceed'],
  ],
};

const local: Record<string, Omit<Analysis, 'timeline'>> = {
  kyc: {
    title: 'KYC verification needs attention',
    what_happened:
      'Your claim cannot move forward because required verification information is incomplete.',
    what_to_do: [
      'Review your KYC information, complete any missing verification, then return to continue your claim.',
    ],
    why: "NIVA's deterministic workflow check found that KYC verification is incomplete.",
    source: {
      title: 'EPFO Member e-Sewa',
      url: 'https://unifiedportal-mem.epfindia.gov.in/memberinterface/',
      section: 'KYC',
      excerpt:
        'KYC details should be completed and approved before a member continues their claim workflow.',
    },
  },

  bank: {
    title: 'Bank verification needs attention',
    what_happened:
      'Your claim is paused because the bank verification did not complete.',
    what_to_do: [
      'Review the bank details and verification status, correct what is needed, then continue your claim.',
    ],
    why: "NIVA's deterministic workflow check found a bank verification issue.",
    source: {
      title: 'EPFO Member e-Sewa',
      url: 'https://unifiedportal-mem.epfindia.gov.in/memberinterface/',
      section: 'Bank details',
      excerpt:
        'Review the bank details and their verification status in the member portal.',
    },
  },

  service: {
    title: 'Service information is missing',
    what_happened:
      'Your employment service information is incomplete, so the claim cannot be checked yet.',
    what_to_do: [
      'Ask your previous employer to review the missing service information, then return to your claim.',
    ],
    why: "NIVA's deterministic workflow check found missing service information.",
    source: null,
  },

  conflict: {
    title: 'Some information does not match',
    what_happened:
      'Your claim details and service record contain conflicting information.',
    what_to_do: [
      'Review the conflicting information with your employer and correct it before continuing.',
    ],
    why: "NIVA's deterministic workflow check found conflicting information.",
    source: null,
  },

  ready: {
    title: "You're ready to continue",
    what_happened:
      'We did not find a blocking issue in this synthetic case.',
    what_to_do: ['Continue to submit your claim and track its processing.'],
    why: "NIVA's deterministic workflow check found no blocking issue.",
    source: null,
  },
};

const defaultTimeline = (key: string): TimelineStep[] => {
  const labels = [
    'Understand claim',
    'Check eligibility',
    'Resolve KYC',
    'Verify bank',
    'Submit claim',
    'Track processing',
    'Payment',
  ];

  const currentIndex =
    key === 'kyc'
      ? 2
      : key === 'bank'
        ? 3
        : key === 'service'
          ? 1
          : key === 'conflict'
            ? 1
            : key === 'ready'
              ? 4
              : 2;

  return labels.map((label, index): TimelineStep => {
    let state: TimelineStep['state'];

    if (index < currentIndex) {
      state = 'complete';
    } else if (index === currentIndex) {
      state = 'current';
    } else {
      state = 'upcoming';
    }

    return {
      key: label,
      label,
      state,
    };
  });
};

function infer(text: string) {
  const t = text.toLowerCase();

  if (t.includes('transfer') || t.includes('previous employer') || t.includes('old employer')) {
    if (t.includes('mismatch') || t.includes('conflict') || t.includes('does not match')) {
      return 'transfer_conflict';
    }
    if (t.includes('ready') || t.includes('complete')) {
      return 'transfer_ready';
    }
    return 'transfer_service';
  }

  if (t.includes('bank')) {
    return 'bank';
  }

  if (t.includes('service') || t.includes('employment')) {
    return 'service';
  }

  if (t.includes('conflict') || t.includes('mismatch')) {
    return 'conflict';
  }

  if (t.includes('ready')) {
    return 'ready';
  }

  return 'kyc';
}

function titleFor(reasonCode?: string) {
  const titles: Record<string, string> = {
    KYC_INCOMPLETE: 'KYC verification needs attention',
    BANK_VERIFICATION_FAILED: 'Bank verification needs attention',
    SERVICE_INFORMATION_MISSING: 'Service information is missing',
    INFORMATION_CONFLICT: 'Information does not match',
    READY_TO_CONTINUE: 'Claim appears ready',
    TRANSFER_SERVICE_MISSING: 'Transfer service information is unavailable',
    TRANSFER_INFORMATION_CONFLICT: 'Transfer details do not match',
    TRANSFER_READY: 'Transfer appears ready',
  };

  return titles[reasonCode || ''] || 'PF request needs attention';
}

function resolutionPlan(analysis: Analysis): ResolutionPlan {
  const plans: Record<string, ResolutionPlan> = {
    KYC_INCOMPLETE: {
      title: 'Resolve your KYC issue',
      summary: 'NIVA found that KYC verification is the current blocker.',
      steps: ['Review which KYC information needs verification.', 'Complete or correct the required details through the appropriate EPFO process.', 'Return to NIVA and check the claim again.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    BANK_VERIFICATION_FAILED: {
      title: 'Resolve bank verification',
      summary: 'NIVA found that bank verification needs attention before the claim can continue.',
      steps: ['Review the bank account details linked to the PF account.', 'Correct or update the details if required.', 'Verify the updated information before continuing with the claim.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    SERVICE_INFORMATION_MISSING: {
      title: 'Resolve missing service information',
      summary: 'NIVA found that employment or service information is incomplete.',
      steps: ['Review employment and service details.', 'Identify the missing or incorrect information.', 'Complete the correction through the appropriate employer or EPFO process.', 'Return and analyze the claim again.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    INFORMATION_CONFLICT: {
      title: 'Resolve the information mismatch',
      summary: 'NIVA found information that does not match the available records.',
      steps: ['Review the information that may not match.', 'Check personal, employment, and PF account details.', 'Correct the mismatch before continuing.', 'Return to NIVA and re-check the issue.'],
      guidanceLabel: 'View official EPFO guidance',
    },
    TRANSFER_SERVICE_MISSING: {
      title: 'Resolve missing transfer information',
      summary: 'NIVA found missing details related to previous employment.',
      steps: ['Review previous employment information.', 'Check the relevant previous and current PF account details.', 'Correct or complete missing information.', 'Re-check the transfer.'],
      guidanceLabel: 'View official transfer guidance',
    },
    TRANSFER_INFORMATION_CONFLICT: {
      title: 'Resolve the transfer information mismatch',
      summary: 'NIVA found a difference between previous and current employment records.',
      steps: ['Compare previous and current employment details.', 'Check PF account information for inconsistencies.', 'Correct the conflicting information before submitting the transfer again.'],
      guidanceLabel: 'View official transfer guidance',
    },
    TRANSFER_READY: {
      title: 'Your transfer appears ready to proceed',
      summary: 'NIVA found no blocking issue in the available transfer information.',
      steps: ['Review the transfer details once more.', 'Continue only with the latest status shown on the official EPFO portal.', 'Return to NIVA if a new issue appears.'],
      guidanceLabel: 'View official transfer guidance',
    },
    READY_TO_CONTINUE: {
      title: 'Your claim appears ready to continue',
      summary: 'NIVA found no blocking issue in the available claim information.',
      steps: ['Review the claim details once more.', 'Continue with the latest status shown on the official EPFO portal.', 'Return to NIVA if a new issue appears.'],
      guidanceLabel: 'View official EPFO guidance',
    },
  };

  return plans[analysis.reasonCode ?? ''] ?? {
    title: analysis.title,
    summary: analysis.what_happened,
    steps: analysis.what_to_do,
    guidanceLabel: 'View official guidance',
  };
}

function App() {
  const [screen, setScreen] = useState<
    'landing' | 'describe' | 'processing' | 'result' | 'resolution'
  >('landing');

  const [claimType, setClaimType] = useState<ClaimType>('withdrawal');
  const [journey, setJourney] = useState<Journey>('general');
  const [issue, setIssue] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState('');
  const [locale, setLocale] = useState('EN');

  const begin = (nextJourney: Journey) => {
    const isGeneral = nextJourney === 'general';
    const nextClaimType = isGeneral ? 'withdrawal' : nextJourney;

    setJourney(nextJourney);
    setClaimType(nextClaimType);
    setIssue(isGeneral ? '' : nextClaimType === 'transfer' ? 'transfer_service' : 'kyc');
    setDescription('');
    setFile(null);
    setError('');
    setScreen('describe');
  };

  async function analyze() {
    setError('');
    setScreen('processing');

    const scenario = issue || infer(description);

    try {
      const created = await fetch(`${API_BASE_URL}/cases`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario,
          claim_type: claimType,
          language: locale.toLowerCase(),
        }),
      });

      if (!created.ok) {
        throw new Error('Failed to create case');
      }

      const { case_id } = await created.json();

      if (file) {
        const form = new FormData();
        form.append('file', file);

        const upload = await fetch(
          `${API_BASE_URL}/cases/${case_id}/documents`,
          {
            method: 'POST',
            body: form,
          }
        );

        if (!upload.ok) {
          throw new Error('Failed to upload document');
        }
      }

      const res = await fetch(
        `${API_BASE_URL}/cases/${case_id}/analyze`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description,
          }),
        }
      );

      if (!res.ok) {
        throw new Error('Failed to analyze case');
      }

      const body = await res.json();

      /*
       * Normalize source information from the backend.
       *
       * Depending on the API response schema, retrieved source metadata
       * may appear as:
       *   explanation.source
       *   explanation.source_references[0]
       *   body.source
       *   body.source_references[0]
       *
       * NIVA's frontend uses a single `source` field.
       */
      const explanation = body.explanation ?? {};

      const source: Source | null =
        explanation.source ??
        explanation.source_references?.[0] ??
        body.source ??
        body.source_references?.[0] ??
        null;

      setAnalysis({
        ...explanation,
        title: explanation.title ?? titleFor(body.result?.reason_code),
        source,
        timeline: body.timeline ?? [],
        reasonCode: body.result?.reason_code,
      });
    } catch {
      const chosen = local[scenario] || local.kyc;

      setAnalysis({
        ...chosen,
        timeline: defaultTimeline(scenario),
      });

      setError(
        'Demo mode / Backend unavailable — this result is local synthetic preview only.'
      );
    }

    setTimeout(() => setScreen('result'), 650);
  }

  const back = () => {
    setScreen(screen === 'describe' ? 'landing' : 'describe');
  };

  const startOver = () => {
    setIssue(journey === 'general' ? '' : claimType === 'transfer' ? 'transfer_service' : 'kyc');
    setDescription('');
    setFile(null);
    setError('');
    setAnalysis(null);
    setScreen('describe');
  };

  const tryAnotherDemo = () => {
    setJourney('general');
    setClaimType('withdrawal');
    setIssue('');
    setDescription('');
    setFile(null);
    setError('');
    setAnalysis(null);
    setScreen('landing');
  };

  return (
    <main>
      <header>
        <button
          className="brand"
          onClick={() => setScreen('landing')}
          aria-label="Go to NIVA home"
        >
          <span>N</span>
          <b>NIVA</b>
        </button>

        <div className="header-actions">
          <label className="text-button">
            <Globe2 size={17} />

            <select
              value={locale}
              onChange={(e) => setLocale(e.target.value)}
              aria-label="Language"
            >
              <option value="EN">EN</option>
              <option value="HI">हिंदी</option>
              <option value="KN">ಕನ್ನಡ</option>
            </select>
          </label>

          <button className="demo">
            <span />
            Demo mode
          </button>
        </div>
      </header>

      <div className="notice">
        <ShieldCheck size={15} />
        Prototype — uses synthetic data. Not an official EPFO service.
      </div>

      {screen === 'landing' && (
        <section className="landing">
          <div className="landing-copy">
            <p className="eyebrow"><Sparkles size={14} /> YOUR PF JOURNEY, EXPLAINED</p>

          <h1>
            PF clarity,
            <br />
            when you <i>need it.</i>
          </h1>

          <p className="lead">
            Tell NIVA what happened. We identify the workflow, explain the issue in plain language, and show the next practical step.
          </p>
          </div>

          <div className="journey-choices">
            <button className="niva-card" onClick={() => begin('general')}>
              <span className="journey-icon"><Sparkles size={22} /></span>
              <span className="journey-kicker">NIVA ANALYSIS</span>
              <b>Tell NIVA what happened</b>
              <small>Describe your PF issue in your own words. NIVA will identify what may be blocking your journey and show the next practical step.</small>
              <span className="journey-cta">Start with my issue <ArrowRight size={17} /></span>
            </button>

            <div className="guided-choices">
            <button className="journey-card withdrawal" onClick={() => begin('withdrawal')}>
              <span className="journey-icon"><WalletCards size={22} /></span>
              <span className="journey-kicker">PF WITHDRAWAL</span>
              <b>I want to withdraw my PF</b>
              <small>Understand a blocked claim, verification issue, or the next step to submit.</small>
              <span className="journey-cta">Explore withdrawal <ArrowRight size={17} /></span>
            </button>

            <button className="journey-card transfer" onClick={() => begin('transfer')}>
              <span className="journey-icon"><Landmark size={22} /></span>
              <span className="journey-kicker">PF TRANSFER</span>
              <b>I want to transfer my PF</b>
              <small>Check previous-employment details and move your PF account with confidence.</small>
              <span className="journey-cta">Explore transfer <ArrowRight size={17} /></span>
            </button>
            </div>
          </div>

          <p className="trust">
            <ShieldCheck size={16} />
            Built for clarity. No real personal data needed.
          </p>
        </section>
      )}

      {screen === 'describe' && (
        <section className="flow">
          <button className="back" onClick={back}>
            <ChevronLeft size={18} />
            Back
          </button>

          <p className="step">STEP 1 OF 2</p>

          {journey === 'general' ? (
            <div className="workflow-badge general">
              <Sparkles size={18} />
              <span>NIVA will identify the relevant PF workflow</span>
            </div>
          ) : (
            <div className={`workflow-badge ${claimType}`}>
              {claimType === 'withdrawal' ? <WalletCards size={18} /> : <Landmark size={18} />}
              <span>Exploring a PF {claimType} request</span>
            </div>
          )}

          <h1>
            {journey === 'general' ? <>Tell NIVA what<br />happened.</> : <>What needs<br />attention?</>}
          </h1>

          <p className="sub">
            {journey === 'general'
              ? 'Describe your issue in plain language. NIVA will use the existing deterministic analysis to find the relevant next step.'
              : 'Select a demo situation below, then add any context in your own words.'}
          </p>

          {journey !== 'general' && <div className="issues">
            {issuesByClaimType[claimType].map(([key, label]) => (
              <button
                key={key}
                className={issue === key ? 'selected' : ''}
                onClick={() => setIssue(key)}
              >
                <span className="radio" />
                {label}
              </button>
            ))}
          </div>}

          <label htmlFor="description">
            What happened? <em>{journey === 'general' ? 'Describe the issue in your own words' : 'Optional — helps NIVA explain it clearly'}</em>
          </label>

          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={journey === 'general' ? 'Example: My PF claim was rejected because my bank details could not be verified.' : claimType === 'transfer' ? 'Example: My previous employer service details are missing for my PF transfer.' : 'Example: My withdrawal claim was rejected because KYC is incomplete.'}
            maxLength={3000}
          />

          <div className="upload">
            <input
              id="file"
              type="file"
              accept="application/pdf,.pdf"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
              }}
            />

            <label htmlFor="file">
              <Upload size={19} />

              <span>
                {file ? file.name : 'Add a synthetic notice'}

                <small>
                  {file
                    ? 'Ready to analyse'
                    : 'Text-based PDF · synthetic data only'}
                </small>
              </span>
            </label>

            {file && (
              <button
                onClick={() => setFile(null)}
                aria-label="Remove file"
              >
                <X size={17} />
              </button>
            )}
          </div>

          <button className="primary continue" onClick={analyze}>
            {journey === 'general' ? 'Let NIVA analyse this' : `Analyse my ${claimType} request`}
            <Send size={17} />
          </button>

          <p className="privacy">
            Please do not upload Aadhaar, PAN, UAN, bank details,
            OTPs, or any real personal data.
          </p>
        </section>
      )}

      {screen === 'processing' && (
        <section className="processing" aria-live="polite">
          <div className="pulse">
            <FileText size={32} />
          </div>

          <p className="eyebrow">
            ANALYSING SYNTHETIC INFORMATION
          </p>

          <h1>
            Understanding
            <br />
            your claim…
          </h1>

          <p>We’re checking the information you provided.</p>

          <div className="processing-line">
            <span />
          </div>
        </section>
      )}

      {screen === 'result' && analysis && (
        <section className="result">
          <button className="back" onClick={startOver}>
            <ChevronLeft size={18} />
            Start over
          </button>

          {error && <p className="demo-error">{error}</p>}

          <p className="eyebrow">ANALYSIS COMPLETE{journey === 'general' ? '' : ` · ${claimType.toUpperCase()} REQUEST`}</p>

          <div className="result-head">
            <div className="success-mark">
              <Check size={24} />
            </div>

            <div>
              <span>{analysis.reasonCode?.includes('READY') ? 'YOUR REQUEST IS CLEAR TO CONTINUE' : 'WHAT NIVA FOUND'}</span>
              <h1>{analysis.title}</h1>
            </div>
          </div>

          <article>
            <p className="article-label">WHAT HAPPENED?</p>
            <p>{analysis.what_happened}</p>
          </article>

          <article className="action">
            <p className="article-label">WHAT DO I DO?</p>
            <ol>
              {analysis.what_to_do.map((action) => <li key={action}>{action}</li>)}
            </ol>

            <button className="action-button" onClick={() => setScreen('resolution')}>
              I understand my next step
              <ArrowRight size={18} />
            </button>
          </article>

          <article>
            <p className="article-label">WHY?</p>

            <p>{analysis.why}</p>

            {analysis.source ? (
              <div className="source-card">
                <div className="source-card-header">
                  <div>
                    <p className="source-label">OFFICIAL GUIDANCE</p>

                    <h3>{analysis.source.title}</h3>

                    <span className="source-section">
                      {analysis.source.section}
                    </span>
                  </div>
                </div>

                {analysis.source.excerpt && (
                  <p className="source-excerpt">
                    {analysis.source.excerpt}
                  </p>
                )}

                <a
                  href={analysis.source.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  View official guidance
                  <ArrowRight size={14} />
                </a>
              </div>
            ) : (
              <small>
                Our local knowledge base does not contain sufficient
                source guidance for this issue.
              </small>
            )}
          </article>

          <div className="journey">
            <p className="article-label">YOUR JOURNEY</p>

            {analysis.timeline.map((step) => (
              <div
                className={`timeline ${step.state}`}
                key={step.key}
              >
                <span>
                  {step.state === 'complete' ? (
                    <Check size={14} />
                  ) : step.state === 'current' ? (
                    '•'
                  ) : (
                    '○'
                  )}
                </span>

                <b>{step.label}</b>

                {step.state === 'current' && (
                  <em>YOU ARE HERE</em>
                )}
              </div>
            ))}
          </div>

          <button
            className="outline"
            onClick={tryAnotherDemo}
          >
            <RotateCcw size={17} />
            Try another demo
          </button>
        </section>
      )}

      {screen === 'resolution' && analysis && (() => {
        const plan = resolutionPlan(analysis);

        return (
          <section className="resolution">
            <button className="back" onClick={() => setScreen('result')}>
              <ChevronLeft size={18} />
              Back to analysis
            </button>

            <p className="eyebrow">YOUR RESOLUTION PLAN</p>

            <div className="resolution-head">
              <div className="success-mark"><Check size={24} /></div>
              <div>
                <span>NIVA RECOMMENDS</span>
                <h1>{plan.title}</h1>
              </div>
            </div>

            <article>
              <p className="article-label">WHAT TO DO NEXT</p>
              <p>{plan.summary}</p>
            </article>

            <article className="resolution-steps">
              <p className="article-label">YOUR ACTION PLAN</p>
              <ol>
                {plan.steps.map((step) => <li key={step}>{step}</li>)}
              </ol>
            </article>

            {analysis.source ? (
              <a className="primary resolution-guidance" href={analysis.source.url} target="_blank" rel="noreferrer">
                {plan.guidanceLabel}
                <ArrowRight size={18} />
              </a>
            ) : (
              <p className="resolution-note">Official guidance remains available on the analysis screen when a relevant source is retrieved.</p>
            )}

            <button className="outline" onClick={tryAnotherDemo}>
              <RotateCcw size={17} />
              Analyze another issue
            </button>
          </section>
        );
      })()}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
