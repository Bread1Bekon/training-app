import React, { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import { 
  User as UserIcon, 
  Mail, 
  Shield, 
  Briefcase, 
  GraduationCap, 
  Heart,
  Loader2,
  AlertCircle,
  ArrowLeft,
  Settings,
  Globe,
  CheckCircle2,
  X
} from 'lucide-react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { apiFetch } from '../lib/api';
import { SkillType, UserType, useAuth } from '../context/AuthContext';

interface Skill {
  id: number;
  name: string;
  description: string | null;
  form_id: number;
  type: SkillType;
}

interface Form {
  id: number;
  description: string;
  user_id: number;
  status: string;
  skills: Skill[];
}

interface UserProfile {
  user: {
    id: number;
    name: string;
    email: string;
    access_level: UserType;
  };
  form: Form;
}

export default function Profile() {
  const { userId } = useParams<{ userId: string }>();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { user: currentUser } = useAuth();
  const [modifyingStatus, setModifyingStatus] = useState(false);
  const [modMessage, setModMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const handleModerateForm = async (newStatus: 'approved' | 'rejected') => {
    if (!profile) return;
    try {
      setModifyingStatus(true);
      setModMessage(null);

      await apiFetch(`/user/form/${profile.user.id}/?form_id=${profile.form.id}&new_form_status=${newStatus}`, {
        method: 'POST',
      });

      // Update profile locally too
      setProfile(prev => {
        if (!prev) return null;
        return {
          ...prev,
          form: {
            ...prev.form,
            status: newStatus
          }
        };
      });

      setModMessage({
        text: `Form status updated to ${newStatus}!`,
        type: 'success'
      });
    } catch (err: any) {
      setModMessage({
        text: err.message || 'Failed to update status.',
        type: 'error'
      });
    } finally {
      setModifyingStatus(false);
    }
  };

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await apiFetch(`/user/${userId}`);
        setProfile(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [userId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-deep flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-brand animate-spin" />
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="min-h-screen bg-bg-deep flex flex-col items-center justify-center p-4 text-center">
        <AlertCircle className="w-16 h-16 text-rose-500 mb-6" />
        <h2 className="text-2xl font-display font-bold text-white mb-2">Something went wrong</h2>
        <p className="text-slate-400 mb-8">{error || 'Could not find the requested profile.'}</p>
        <button
          onClick={() => navigate(-1)}
          className="bg-white/5 border border-white/10 text-white px-8 py-3 rounded-full font-bold hover:bg-white/10 transition-all flex items-center gap-2"
        >
          <ArrowLeft className="w-5 h-5" /> Go Back
        </button>
      </div>
    );
  }

  const learnSkills = profile.form ? profile.form.skills.filter(s => s.type === SkillType.LEARN) : [];
  const teachSkills = profile.form ? profile.form.skills.filter(s => s.type === SkillType.TEACH) : [];

  return (
    <div className="min-h-screen bg-bg-deep text-[#E0E2E6] font-sans pb-20">
      {/* Profile Header */}
      <div className="relative h-64 bg-gradient-to-r from-brand/20 via-bg-deep to-emerald/20 border-b border-white/5">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full relative">
          <Link
            to="/"
            className="absolute top-8 left-4 sm:left-8 w-10 h-10 rounded-full bg-white/5 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>

          <div className="absolute -bottom-16 left-4 sm:left-8 flex flex-col sm:flex-row items-end gap-6">
            <div className="w-32 h-32 rounded-3xl bg-bg-surface border-4 border-bg-deep flex items-center justify-center shadow-3xl">
              <UserIcon className="w-16 h-16 text-slate-700" />
            </div>
            <div className="mb-2 space-y-1">
              <h1 className="text-4xl font-display font-bold text-white tracking-tight">{profile.user.name}</h1>
              <div className="flex flex-wrap items-center gap-4 text-slate-400 text-sm font-medium">
                <span className="flex items-center gap-1.5"><Mail className="w-4 h-4" /> {profile.user.email}</span>
                <span className="flex items-center gap-1.5"><Shield className="w-4 h-4 text-brand-light" /> {profile.user.access_level}</span>
                <span className="flex items-center gap-1.5"><Globe className="w-4 h-4 text-emerald" /> Global Member</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-24">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-12">
            {/* About */}
            <section className="bg-bg-surface/50 border border-white/5 rounded-[2.5rem] p-8 lg:p-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-brand/10 rounded-xl flex items-center justify-center text-brand-light">
                  <Briefcase className="w-5 h-5" />
                </div>
                <h2 className="text-2xl font-display font-bold text-white">About Me</h2>
              </div>
              <p className="text-lg text-slate-400 leading-relaxed italic">
                {profile.form ? `"${profile.form.description}"` : "This user has not submitted their profile details yet."}
              </p>
            </section>

            {/* Skills Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Teaching */}
              <section className="space-y-6">
                <div className="flex items-center gap-3 px-2">
                  <div className="w-8 h-8 bg-brand/10 rounded-lg flex items-center justify-center text-brand-light">
                    <Heart className="w-4 h-4" />
                  </div>
                  <h3 className="text-xl font-display font-bold text-white">Want to Teach</h3>
                </div>
                <div className="space-y-4">
                  {teachSkills.length > 0 ? teachSkills.map(skill => (
                    <motion.div
                      key={skill.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-6 bg-bg-surface border border-brand/10 rounded-3xl"
                    >
                      <h4 className="font-bold text-white mb-2">{skill.name}</h4>
                      {skill.description && (
                        <p className="text-sm text-slate-500 leading-relaxed">{skill.description}</p>
                      )}
                    </motion.div>
                  )) : (
                    <div className="p-8 rounded-3xl border border-dashed border-white/5 text-center text-slate-600 text-sm">
                      No teaching skills listed yet.
                    </div>
                  )}
                </div>
              </section>

              {/* Learning */}
              <section className="space-y-6">
                <div className="flex items-center gap-3 px-2">
                  <div className="w-8 h-8 bg-emerald/10 rounded-lg flex items-center justify-center text-emerald">
                    <GraduationCap className="w-4 h-4" />
                  </div>
                  <h3 className="text-xl font-display font-bold text-white">Want to Learn</h3>
                </div>
                <div className="space-y-4">
                  {learnSkills.length > 0 ? learnSkills.map(skill => (
                    <motion.div
                      key={skill.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-6 bg-bg-surface border border-emerald/10 rounded-3xl"
                    >
                      <h4 className="font-bold text-white mb-2">{skill.name}</h4>
                      {skill.description && (
                        <p className="text-sm text-slate-500 leading-relaxed">{skill.description}</p>
                      )}
                    </motion.div>
                  )) : (
                    <div className="p-8 rounded-3xl border border-dashed border-white/5 text-center text-slate-600 text-sm">
                      No learning goals listed yet.
                    </div>
                  )}
                </div>
              </section>
            </div>
          </div>

          {/* Sidebar */}
          <aside className="space-y-8">
            <div className="bg-bg-surface border border-white/5 rounded-[2.5rem] p-8">
              <h3 className="text-xl font-display font-bold text-white mb-6">Stats & Activity</h3>
              <div className="space-y-6">
                <div className="flex items-center justify-between py-3 border-b border-white/5">
                  <span className="text-slate-500 text-sm">Skills listed</span>
                  <span className="text-white font-bold">{profile.form ? profile.form.skills.length : 0}</span>
                </div>
                <div className="flex items-center justify-between py-3 border-b border-white/5">
                  <span className="text-slate-500 text-sm">Member since</span>
                  <span className="text-white font-bold">2026</span>
                </div>
                <div className="flex items-center justify-between py-3 border-b border-white/5">
                  <span className="text-slate-500 text-sm">Trust Score</span>
                  <span className="text-emerald font-bold">99%</span>
                </div>
              </div>
              <button className="w-full mt-8 bg-brand text-white py-4 rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-brand-light transition-all shadow-xl shadow-brand/20">
                Connect Now
              </button>
            </div>

            {currentUser?.access_level === UserType.MODERATOR && profile.form && (
              <div className="bg-bg-surface border border-brand/20 rounded-[2.5rem] p-8 space-y-6">
                <div>
                  <h3 className="text-xl font-display font-bold text-white flex items-center gap-2">
                    <Shield className="w-5 h-5 text-brand" /> Moderator Actions
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">
                    As a moderator, you can approve or reject this user's profile form. These actions trigger live WebSocket alerts.
                  </p>
                </div>

                <div className="flex items-center justify-between p-4 bg-bg-deep rounded-2xl border border-white/5">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Current Status</span>
                  <span className={`text-xs font-black uppercase tracking-widest py-1 px-3.5 rounded-full ${
                    profile.form.status === 'approved'
                      ? 'bg-emerald/10 text-emerald border border-emerald/20'
                      : profile.form.status === 'rejected'
                      ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                      : 'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                  }`}>
                    {profile.form.status}
                  </span>
                </div>

                {modMessage && (
                  <div className={`p-4 rounded-2xl text-xs font-bold border ${
                    modMessage.type === 'success'
                      ? 'bg-emerald/10 border-emerald/20 text-emerald'
                      : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                  }`}>
                    {modMessage.text}
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => handleModerateForm('approved')}
                    disabled={modifyingStatus || profile.form.status === 'approved'}
                    className="py-3.5 px-4 bg-emerald text-black rounded-xl font-bold hover:bg-emerald-light transition-all text-xs disabled:opacity-40 cursor-pointer flex items-center justify-center gap-1.5"
                  >
                    <CheckCircle2 className="w-4 h-4" /> Approve
                  </button>
                  <button
                    onClick={() => handleModerateForm('rejected')}
                    disabled={modifyingStatus || profile.form.status === 'rejected'}
                    className="py-3.5 px-4 bg-rose-600 text-white hover:bg-rose-700 rounded-xl font-bold transition-all text-xs disabled:opacity-40 cursor-pointer flex items-center justify-center gap-1.5"
                  >
                    <X className="w-4 h-4" /> Reject
                  </button>
                </div>
              </div>
            )}

            <div className="p-8 rounded-[2.5rem] border border-white/5 bg-gradient-to-br from-bg-surface to-bg-deep flex flex-col items-center text-center">
              <Settings className="w-8 h-8 text-slate-500 mb-4" />
              <h3 className="text-white font-bold mb-2">Privacy Settings</h3>
              <p className="text-xs text-slate-600 mb-6 leading-relaxed">
                Only verified members can see your contact information and full teaching portfolio.
              </p>
              <button className="text-xs font-bold text-brand-light hover:text-white transition-colors">Manage Access</button>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}