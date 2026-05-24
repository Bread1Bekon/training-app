import { motion } from "motion/react";
import { 
  Users, 
  BookOpen, 
  MessageSquare, 
  Zap, 
  Target, 
  ArrowRight, 
  CheckCircle2, 
  Search, 
  Globe
} from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function Landing() {
  const { isAuthenticated, logout, user } = useAuth();

  return (
    <div className="min-h-screen bg-bg-deep text-[#E0E2E6] font-sans selection:bg-brand selection:text-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-bg-deep/80 backdrop-blur-md border-b border-border-subtle">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            <Link to="/" className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-tr from-brand to-emerald rounded-lg shadow-lg shadow-brand/20"></div>
              <span className="text-xl font-display font-bold tracking-tight text-white">MentorFlow</span>
            </Link>
            <div className="hidden md:flex items-center gap-10 text-sm font-medium text-slate-400">
              <a href="#features" className="hover:text-white transition-colors">Features</a>
              <a href="#how-it-works" className="hover:text-white transition-colors">How it Works</a>
            </div>
            <div className="flex items-center gap-6">
              {isAuthenticated ? (
                <>
                  <span className="text-sm text-slate-400 hidden sm:block">Hello, <span className="text-white font-bold">{user?.name}</span></span>
                  <button onClick={logout} className="text-sm font-medium text-slate-400 hover:text-white transition-colors px-2">Sign Out</button>
                  <Link to="/swipe" className="text-sm font-medium text-brand-light hover:text-white transition-colors px-2">
                    Find Matches
                  </Link>
                  <Link to={`/profile/${user?.id}`} className="bg-white text-black text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-slate-200 transition-all">
                    My Profile
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-sm font-medium text-slate-400 hover:text-white transition-colors px-2">Sign In</Link>
                  <Link to="/register" className="bg-white text-black text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-slate-200 transition-all">
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-20">
        {/* Hero Section */}
        <section className="relative py-24 lg:py-40 overflow-hidden">
          {/* Background Decorative Elements */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 overflow-hidden pointer-events-none">
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-brand/10 rounded-full blur-[140px]" />
            <div className="absolute bottom-[20%] right-[-10%] w-[40%] h-[40%] bg-emerald/5 rounded-full blur-[120px]" />
          </div>

          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-4xl mx-auto">
              <motion.h1 
                className="text-6xl lg:text-8xl font-display font-bold text-white tracking-tighter leading-[1.05] mb-8"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
              >
                Bridge the gap with <br/>
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-light via-white to-emerald">refined mentorship.</span>
              </motion.h1>

              <motion.p 
                className="text-xl lg:text-2xl text-slate-400 leading-relaxed mb-14 max-w-2xl mx-auto"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                Find your perfect mentor match or share your expertise with a global community of learners. Optimized for growth and networking.
              </motion.p>


            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-transparent">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-3 gap-6"
              variants={staggerContainer}
              initial="initial"
              whileInView="animate"
              viewport={{ once: true }}
            >
              {[
                {
                  icon: Zap,
                  title: "Instant matchmaking",
                  description: "Find alike minds who look for skills that you can teach or get an expert in a field that you are interested in.",
                  color: "bg-brand/10 text-brand-light"
                },
                {
                  icon: ShieldCheck,
                  title: "Safe Haven",
                  description: "Look for verified accounts to get experience from people with real-life experience.",
                  color: "bg-emerald/10 text-emerald",
                  iconAlt: CheckCircle2
                },
                {
                  icon: Database,
                  title: "Networking",
                  description: "Use built-in messenger and video calls to organize meet-ups or create whole communities using group chats.",
                  color: "bg-orange-500/10 text-orange-400",
                  iconAlt: Globe
                }
              ].map((feature, idx) => (
                <motion.div 
                  key={idx}
                  variants={fadeIn}
                  className="p-8 rounded-3xl border border-white/5 bg-bg-surface hover:border-white/10 hover:shadow-2xl transition-all group"
                >
                  <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-6`}>
                    {feature.iconAlt ? <feature.iconAlt className="w-6 h-6" /> : <feature.icon className="w-6 h-6" />}
                  </div>
                  <h3 className="text-xl font-display font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-slate-400 leading-relaxed text-sm">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* How it Works / Split Section */}
        <section id="how-it-works" className="py-24 border-y border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <div className="inline-block px-3 py-1 rounded-full bg-brand/10 text-brand-light text-xs font-bold uppercase tracking-wider mb-6">
                  Architecture
                </div>
                <h2 className="text-4xl lg:text-6xl font-display font-bold text-white mb-8 leading-tight tracking-tight">
                  A workshop that grows <br/> with your team.
                </h2>
                <div className="space-y-8">
                  {[
                    "Create your profile with specialized skills and goals.",
                    "Browse our verified directory of experts or become one.",
                    "Schedule regular syncs and participate in workshops.",
                    "Exchange experience and knowledge worldwide."
                  ].map((text, i) => (
                    <div key={i} className="flex gap-5">
                      <div className="flex-shrink-0 w-6 h-6 rounded-full border border-brand/40 flex items-center justify-center text-brand-light font-bold text-xs">
                        {i + 1}
                      </div>
                      <p className="text-lg text-slate-400">{text}</p>
                    </div>
                  ))}
                </div>
              </motion.div>

              <motion.div 
                className="relative"
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <div className="relative z-10 bg-bg-surface p-10 rounded-[2.5rem] shadow-3xl border border-white/10">
                  <div className="flex items-center gap-4 mb-10">
                    <div className="w-12 h-12 rounded-xl bg-bg-deep flex items-center justify-center border border-white/5"><Search className="w-6 h-6 text-slate-600" /></div>
                    <div className="flex-1 h-3 bg-bg-deep rounded-full relative overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-r from-brand to-emerald w-1/3 rounded-full"></div>
                    </div>
                  </div>
                  <div className="space-y-5">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="flex items-center gap-4 p-5 rounded-2xl bg-bg-deep/50 border border-white/5">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-slate-700 to-slate-800" />
                        <div className="flex-1 space-y-2">
                          <div className="w-1/2 h-2 bg-slate-800 rounded-full" />
                          <div className="w-1/3 h-2 bg-slate-900 rounded-full" />
                        </div>
                        <div className="w-16 h-8 rounded-full bg-white/5 border border-white/5" />
                      </div>
                    ))}
                  </div>
                  <div className="mt-10 p-8 rounded-2xl bg-gradient-to-br from-brand to-emerald text-white flex items-center justify-between shadow-2xl">
                    <div>
                      <p className="text-[10px] opacity-70 uppercase font-black tracking-[0.2em] mb-2">Sync Connection</p>
                      <p className="text-2xl font-display font-bold">New match verified</p>
                    </div>
                    <div className="w-14 h-14 rounded-full bg-white text-bg-deep flex items-center justify-center shadow-lg">
                      <CheckCircle2 className="w-7 h-7" />
                    </div>
                  </div>
                </div>
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-brand/20 blur-[80px] -z-10" />
                <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-emerald/20 blur-[80px] -z-10" />
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-32 relative overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
            <h2 className="text-5xl lg:text-8xl font-display font-bold text-white mb-10 tracking-tighter">Ready to scale your <br/> learning potential?</h2>
            <p className="text-slate-400 text-xl lg:text-2xl mb-14 max-w-2xl mx-auto">
              Join a community of experts committed to growth. No fees for individuals during our inaugural workshop phase.
            </p>
            <div className="flex flex-wrap justify-center gap-6">
              {isAuthenticated ? (
                <>
                  <Link to="/swipe" className="bg-white text-black px-12 py-5 rounded-full font-bold text-lg hover:bg-slate-200 transition-all flex items-center justify-center gap-2">
                    Find matches <ArrowRight className="w-6 h-6" />
                  </Link>
                  <Link to={`/profile/${user?.id}`} className="bg-white/5 border border-white/10 text-white px-12 py-5 rounded-full font-bold text-lg hover:bg-white/10 transition-all flex items-center justify-center">
                    My Profile
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/register" className="bg-white text-black px-12 py-5 rounded-full font-bold text-lg hover:bg-slate-200 transition-all flex items-center justify-center gap-2">
                    Join MentorFlow <ArrowRight className="w-6 h-6" />
                  </Link>
                  <button className="bg-white/5 border border-white/10 text-white px-12 py-5 rounded-full font-bold text-lg hover:bg-white/10 transition-all">
                    Explore Workshops
                  </button>
                </>
              )}
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-bg-deep py-20 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-10 text-[10px] uppercase tracking-[0.3em] font-black text-slate-600">
            <div>© 2026 MentorFlow Systems</div>
            <div className="flex gap-12">
              <a href="#" className="hover:text-white transition-colors">Twitter (X)</a>
              <a href="#" className="hover:text-white transition-colors">Discord</a>
              <a href="#" className="hover:text-white transition-colors">LinkedIn</a>
            </div>
            <div>Built for High Performance</div>
          </div>
        </div>
      </footer>
    </div>
  );
}

const Database = (props: any) => (
  <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582-4-8 4s-8-1.79-8-4"/></svg>
);

const ShieldCheck = (props: any) => (
  <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
);
