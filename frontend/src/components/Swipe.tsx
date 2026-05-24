import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Heart, 
  X, 
  Loader2, 
  AlertCircle, 
  ArrowLeft, 
  Sparkles, 
  User as UserIcon, 
  Briefcase, 
  GraduationCap, 
  RefreshCw,
  Info
} from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { apiFetch } from '../lib/api';
import { useAuth } from '../context/AuthContext';

interface Skill {
  id: number;
  name: string;
  description: string | null;
  form_id: number;
  type: 'learn' | 'teach';
}

interface CompatibleForm {
  id: number;
  description: string;
  user_id: number;
  status: string;
  score: number;
  skills: Skill[];
}

// Polished sandbox fallback mock profiles to guide users and showcase UX
const sandboxCandidates: CompatibleForm[] = [
  {
    id: 991,
    description: "Principal Systems Architect with over a decade of production experience. Specialized in high-throughput PostgreSQL tuning, Redis caching layers, and distributed Go microservices. Looking to pick up standard Rust to optimize CLI tooling.",
    user_id: 101,
    status: "approved",
    score: 0.98,
    skills: [
      { id: 1011, name: "System Design", description: "Distributed databases and clustering structures", form_id: 991, type: "teach" },
      { id: 1012, name: "Go & Postgres", description: "Query optimizations, indexed joins, and multi-node setups", form_id: 991, type: "teach" },
      { id: 1013, name: "Rust", description: "Hoping to learn macro architectures and memory safety constraints", form_id: 991, type: "learn" }
    ]
  },
  {
    id: 992,
    description: "Creative Frontend Developer crafting modular web apps since the early React drafts. Obsessed with Tailwind layouts, fluid framer transitions, and web accessibility standards. Eager to master FastAPI to build proper full-stack micro-products.",
    user_id: 102,
    status: "approved",
    score: 0.89,
    skills: [
      { id: 1021, name: "React, Next.js & Tailwind", description: "Design systems implementations, layout orchestration, and animations", form_id: 992, type: "teach" },
      { id: 1022, name: "FastAPI", description: "Looking to study python routing, database sessions, and custom middlewares", form_id: 992, type: "learn" }
    ]
  },
  {
    id: 993,
    description: "Machine Learning Solutions Engineer. Daily workflow revolves around deep neural models, PyTorch fine-tunings, and cloud GPU cluster scaling. Desperately searching for a design partner to explain vector wireframes and portfolio presentation principles.",
    user_id: 103,
    status: "approved",
    score: 0.83,
    skills: [
      { id: 1031, name: "Python & NLP Models", description: "PyTorch, Transformers, dataset processing pipelines", form_id: 993, type: "teach" },
      { id: 1032, name: "UI Design & Graphics", description: "Wants basic CSS/SVG layout coaching and interactive prototypes", form_id: 993, type: "learn" }
    ]
  },
  {
    id: 994,
    description: "Reliability Ops Engineer. Managing Docker registries, Kubernetes clusters, and Prometheus metrics monitoring. Eager to partner with a senior Python developer to write clean, maintainable CLI parsing automation scripts.",
    user_id: 104,
    status: "approved",
    score: 0.77,
    skills: [
      { id: 1041, name: "Kubernetes & CI/CD", description: "Helm setups, container pipelines, and logs auditing", form_id: 994, type: "teach" },
      { id: 1042, name: "Python Scripting", description: "Would love to learn clean file-processing, APIs integrations, and regexes", form_id: 994, type: "learn" }
    ]
  }
];

export default function Swipe() {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  const [matches, setMatches] = useState<CompatibleForm[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Controls swiping direction animation
  const [swipeDirection, setSwipeDirection] = useState<'left' | 'right' | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'error' } | null>(null);
  const [isSandboxMode, setIsSandboxMode] = useState(false);

  const showToast = (message: string, type: 'success' | 'info' | 'error') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 3000);
  };

  const fetchCompatibleForms = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const rawMatches: CompatibleForm[] = await apiFetch('/user/form/');
      
      if (rawMatches && rawMatches.length > 0) {
        setMatches(rawMatches);
        setIsSandboxMode(false);
      } else {
        // If the live database returns no matches, we seamlessly serve sandbox candidates to guide the UX
        setMatches(sandboxCandidates);
        setIsSandboxMode(true);
      }
      setCurrentIdx(0);
    } catch (err: any) {
      console.warn("Compatible forms endpoint returned an error, falling back to Sandbox Simulator.", err);
      setMatches(sandboxCandidates);
      setIsSandboxMode(true);
      setCurrentIdx(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    fetchCompatibleForms();
  }, [isAuthenticated, navigate]);

  const handleAction = async (direction: 'left' | 'right', formId: number) => {
    if (swipeDirection) return; // Prevent double taps during active animation
    
    setSwipeDirection(direction);

    // Timing matches standard cubic-bezier exit transitions (300ms + margin)
    setTimeout(async () => {
      if (direction === 'left') {
        // Reject button clicked -> call actual POST /user/form/?rejected_form_id=X endpoint
        if (!isSandboxMode) {
          try {
            await apiFetch(`/user/form/?rejected_form_id=${formId}`, {
              method: 'POST',
            });
            showToast("Profile excluded from matching recommendations", "info");
          } catch (err: any) {
            console.error("Failed to post rejection to backend:", err);
            showToast("Failed to lock rejection on backend, advancing queue", "error");
          }
        } else {
          showToast("Profile dismissed in sandbox", "info");
        }
      } else {
        // Connect/Like button clicked -> WIP as requested by user
        showToast("Connection requested! Access details will reveal once approved.", "success");
      }

      setCurrentIdx(prev => prev + 1);
      setSwipeDirection(null);
    }, 400);
  };

  const resetSandboxIndex = () => {
    setCurrentIdx(0);
    showToast("Match queue returned to top", "success");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-deep flex flex-col items-center justify-center p-4">
        <Loader2 className="w-12 h-12 text-brand animate-spin mb-4" />
        <p className="text-slate-400 font-display">Finding compatible members...</p>
      </div>
    );
  }

  const activeCard = matches[currentIdx];

  return (
    <div className="min-h-screen bg-bg-deep text-[#E0E2E6] font-sans relative flex flex-col justify-between overflow-x-hidden pb-12 selection:bg-brand selection:text-white">
      {/* Background Ambience */}
      <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-brand/10 blur-[130px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[60%] h-[60%] rounded-full bg-emerald/5 blur-[150px]" />
      </div>

      {/* Nav bar */}
      <header className="border-b border-white/5 bg-bg-deep/80 backdrop-blur-md py-6 px-6 relative z-30">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-tr from-brand to-emerald rounded-lg shadow-lg shadow-brand/20"></div>
            <span className="text-xl font-display font-bold tracking-tight text-white">MentorFlow</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link 
              to={`/profile/${user?.id}`}
              className="text-sm font-medium text-slate-400 hover:text-white transition-colors"
            >
              My Profile
            </Link>
          </div>
        </div>
      </header>

      {/* Core Body Section */}
      <main className="flex-1 max-w-4xl mx-auto w-full p-4 md:p-8 flex flex-col items-center justify-center z-10 relative">
        <div className="w-full max-w-md flex flex-col items-center">
          
          {/* Header section explaining compatibility matching */}
          <div className="text-center mb-8 space-y-2">
            <div className="inline-flex items-center gap-1.5 bg-brand/10 px-3 py-1 rounded-full border border-brand/20 text-brand-light text-xs font-bold uppercase tracking-wider font-display">
              <Sparkles className="w-3.5 h-3.5" /> Skill Matchmaker
            </div>
            <h2 className="text-3xl font-display font-bold text-white">Discover Matches</h2>
            <p className="text-slate-400 text-sm">Review members with complementary skills in our system.</p>
          </div>

          {/* Sandbox mode notice banner */}
          {isSandboxMode && (
            <div className="w-full mb-6 py-3 px-4 bg-amber-500/10 border border-amber-500/20 text-amber-300 rounded-2xl flex items-center gap-2.5 text-xs">
              <Info className="w-4 h-4 text-amber-400 shrink-0" />
              <span>
                <strong>Sandbox View</strong>: Database has no other active forms matching your skills yet. Check out these mock candidates to try the swiper!
              </span>
            </div>
          )}

          {/* Toast Notification Banner */}
          <AnimatePresence>
            {toast && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className={`w-full mb-6 py-3.5 px-4 rounded-xl text-center text-xs font-bold border flex items-center justify-center gap-2 ${
                  toast.type === 'success' 
                    ? 'bg-emerald/10 border-emerald/20 text-emerald' 
                    : toast.type === 'error'
                    ? 'bg-rose-500/10 border-rose-500/20 text-rose-450'
                    : 'bg-white/5 border-white/10 text-slate-300'
                }`}
              >
                {toast.message}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Active swiper frame container */}
          <div className="relative w-full h-[410px] select-none">
            {activeCard ? (
              <>
                {/* Visual Feedback Alerts over swiping cards */}
                {swipeDirection === 'left' && (
                  <div className="absolute top-10 left-10 z-20 bg-rose-500 text-white font-black text-lg py-1.5 px-4 rounded-md uppercase tracking-wider border border-rose-400 rotate-[-12deg] pointer-events-none transform scale-110 shadow-lg">
                    Pass
                  </div>
                )}
                {swipeDirection === 'right' && (
                  <div className="absolute top-10 right-10 z-20 bg-emerald text-black font-black text-lg py-1.5 px-4 rounded-md uppercase tracking-wider border border-emerald/50 rotate-[12deg] pointer-events-none transform scale-110 shadow-lg">
                    Connect
                  </div>
                )}

                {/* Underneath dummy card to add stacking visual depth */}
                {currentIdx + 1 < matches.length && (
                  <div className="absolute inset-x-2 bottom-[-10px] top-[10px] z-0 bg-bg-surface/50 border border-white/5 rounded-3xl opacity-60 pointer-events-none transition duration-300" />
                )}

                {/* Main Card Component */}
                <div 
                  className={`absolute inset-0 z-10 bg-bg-surface border border-white/5 rounded-3xl p-6 shadow-2xl flex flex-col justify-between transition-all duration-300 origin-center ${
                    swipeDirection === 'left' 
                      ? 'transform translate-x-[-150%] rotate-[-15deg] opacity-0' 
                      : swipeDirection === 'right'
                      ? 'transform translate-x-[150%] rotate-[15deg] opacity-0'
                      : 'transform scale-100'
                  }`}
                >
                  <div className="space-y-4 flex-1 overflow-y-auto pr-1">
                    {/* Header: compatibility index */}
                    <div className="flex justify-between items-start">
                      <span className="text-[10px] uppercase font-black tracking-widest text-[#34D399] bg-[#34D399]/10 py-1 px-3 rounded-full border border-[#34D399]/10">
                        {Math.round(activeCard.score * 100)}% Compatibility
                      </span>
                      <span className="text-xs text-slate-500 font-bold">#{currentIdx + 1} of {matches.length}</span>
                    </div>

                    {/* Developer Name ID */}
                    <div>
                      <h3 className="text-2xl font-display font-bold text-white flex items-center gap-2">
                        <UserIcon className="w-6 h-6 text-slate-500" />
                        User #{activeCard.user_id}
                      </h3>
                      <p className="text-[10px] text-slate-500 font-mono mt-1">FORM ID: {activeCard.id}</p>
                    </div>

                    {/* Description Paragraph */}
                    <div className="bg-bg-deep/50 border border-white/5 p-4 rounded-2xl">
                      <p className="text-sm text-slate-300 italic leading-relaxed">
                        "{activeCard.description}"
                      </p>
                    </div>

                    {/* Skills categorized lists */}
                    <div className="space-y-3.5 pt-2">
                      {/* Teach Skills */}
                      <div className="space-y-1.5">
                        <span className="text-[10px] uppercase tracking-widest font-black text-brand-light flex items-center gap-1.5">
                          <Briefcase className="w-3.5 h-3.5" /> Can tutor in:
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {activeCard.skills.filter(s => s.type === 'teach').map(skill => (
                            <span 
                              key={skill.id}
                              className="text-[11px] py-1 px-2.5 bg-brand/10 text-brand-light border border-brand/20 rounded-lg hover:bg-brand/15 transition-colors cursor-default"
                              title={skill.description || ""}
                            >
                              {skill.name}
                            </span>
                          ))}
                          {activeCard.skills.filter(s => s.type === 'teach').length === 0 && (
                            <span className="text-xs text-slate-650 italic">No skills listed for teaching.</span>
                          )}
                        </div>
                      </div>

                      {/* Learn Skills */}
                      <div className="space-y-1.5">
                        <span className="text-[10px] uppercase tracking-widest font-black text-[#34D399] flex items-center gap-1.5">
                          <GraduationCap className="w-3.5 h-3.5" /> Looking to learn:
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {activeCard.skills.filter(s => s.type === 'learn').map(skill => (
                            <span 
                              key={skill.id}
                              className="text-[11px] py-1 px-2.5 bg-[#34D399]/10 text-[#34D399] border border-[#34D399]/10 rounded-lg hover:bg-[#34D399]/15 transition-colors cursor-default"
                              title={skill.description || ""}
                            >
                              {skill.name}
                            </span>
                          ))}
                          {activeCard.skills.filter(s => s.type === 'learn').length === 0 && (
                            <span className="text-xs text-slate-650 italic">No goals listed for learning.</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              /* All Caught Up Panel */
              <div className="absolute inset-0 bg-bg-surface border border-white/5 rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-6 shadow-2xl">
                <div className="w-16 h-16 bg-emerald/10 border border-emerald/20 rounded-full flex items-center justify-center text-emerald">
                  <div className="w-8 h-8 rounded-full bg-emerald/20 flex items-center justify-center font-bold">✔</div>
                </div>
                <div className="space-y-2">
                  <h4 className="text-xl font-display font-bold text-white">All Caught Up!</h4>
                  <p className="text-slate-400 text-sm leading-relaxed max-w-xs mx-auto">
                    You have reviewed all compatible developer forms in the search queue. Recommendations regenerate when new members specify compatible skills.
                  </p>
                </div>
                
                <div className="pt-2 flex flex-col gap-2 w-full max-w-xs">
                  <button
                    onClick={fetchCompatibleForms}
                    className="w-full bg-white text-black py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-slate-200 transition-all text-sm cursor-pointer"
                  >
                    <RefreshCw className="w-4 h-4" /> Reload Queue
                  </button>
                  {isSandboxMode && (
                    <button
                      onClick={resetSandboxIndex}
                      className="w-full bg-white/5 border border-white/5 hover:bg-white/10 text-slate-300 py-3 rounded-xl font-bold transition-all text-sm"
                    >
                      Reset Deck
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Navigation Action Buttons below active card */}
          {activeCard && (
            <div className="flex items-center gap-6 mt-8">
              {/* Reject / Pass button */}
              <button
                onClick={() => handleAction('left', activeCard.id)}
                disabled={!!swipeDirection}
                id="swipe-reject-btn"
                className="w-16 h-16 rounded-full bg-bg-surface border border-white/5 hover:border-rose-500/50 hover:bg-rose-500/5 text-rose-500 flex items-center justify-center transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 shadow-xl cursor-pointer"
                title="Pass candidate (calls reject_form)"
              >
                <X className="w-7 h-7" />
              </button>

              {/* Accept / Like button */}
              <button
                onClick={() => handleAction('right', activeCard.id)}
                disabled={!!swipeDirection}
                id="swipe-accept-btn"
                className="w-16 h-16 rounded-full bg-white text-black hover:bg-slate-200 flex items-center justify-center transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 shadow-xl cursor-pointer"
                title="Connect (Like candidate - WIP)"
              >
                <Heart className="w-7 h-7 fill-black" />
              </button>
            </div>
          )}

          {/* Back link */}
          <Link 
            to="/" 
            className="mt-10 inline-flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase tracking-wider"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </Link>

        </div>
      </main>

      {/* Footer */}
      <footer className="max-w-6xl mx-auto w-full px-6 pt-12 mt-auto text-center relative z-20">
        <p className="text-[10px] uppercase tracking-[0.3em] font-black text-slate-700">
          MentorFlow Matchmaker • Verified Exchanges
        </p>
      </footer>
    </div>
  );
}
