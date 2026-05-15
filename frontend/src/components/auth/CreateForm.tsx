import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  BookOpen, 
  Plus, 
  Trash2, 
  Save, 
  Loader2, 
  AlertCircle, 
  Info,
  CheckCircle2,
  GraduationCap
} from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';
import { apiFetch } from '../../lib/api';
import { SkillType } from '../../context/AuthContext';

interface SkillInput {
  name: string;
  description: string;
  type: SkillType;
}

export default function CreateForm() {
  const { userId } = useParams<{ userId: string }>();
  const [description, setDescription] = useState('');
  const [skills, setSkills] = useState<SkillInput[]>([
    { name: '', description: '', type: SkillType.LEARN }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();

  const addSkill = () => {
    setSkills([...skills, { name: '', description: '', type: SkillType.LEARN }]);
  };

  const removeSkill = (index: number) => {
    setSkills(skills.filter((_, i) => i !== index));
  };

  const updateSkill = (index: number, field: keyof SkillInput, value: string) => {
    const newSkills = [...skills];
    newSkills[index] = { ...newSkills[index], [field]: value };
    setSkills(newSkills);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Basic validation
    if (!description.trim()) {
      setError('Please provide a short description about yourself.');
      setLoading(false);
      return;
    }

    if (skills.some(s => !s.name.trim())) {
      setError('Please ensure all skills have a name.');
      setLoading(false);
      return;
    }

    try {
      await apiFetch(`/user/form/${userId}/create_form`, {
        method: 'POST',
        body: JSON.stringify({
          description,
          skills
        }),
      });

      // After form creation, we usually want them to log in to start their session
      navigate('/login');
    } catch (err: any) {
      setError(err.message || 'Failed to create form. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-deep flex flex-col items-center p-4 py-20">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-2xl"
      >
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-tr from-brand to-emerald rounded-2xl flex items-center justify-center shadow-lg shadow-brand/20 text-white">
              < GraduationCap className="w-7 h-7" />
            </div>
          </div>
          <h1 className="text-4xl font-display font-bold text-white mb-4 tracking-tight">Tell us about your skills</h1>
          <p className="text-slate-400 text-lg">Help us match you with the right community members.</p>
        </div>

        <div className="bg-bg-surface border border-white/5 p-8 lg:p-12 rounded-[3rem] shadow-3xl">
          <form onSubmit={handleSubmit} className="space-y-10">
            {error && (
              <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex items-center gap-3 text-rose-400 text-sm">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <p>{error}</p>
              </div>
            )}

            {/* About Section */}
            <div className="space-y-4">
              <div className="flex items-center gap-2 mb-2">
                <Info className="w-4 h-4 text-brand-light" />
                <label className="text-xs uppercase tracking-[0.2em] font-black text-slate-500">Short Bio / Description</label>
              </div>
              <textarea
                required
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full bg-bg-deep border border-white/5 rounded-3xl p-6 text-white text-lg focus:outline-none focus:border-brand/50 transition-colors min-h-[120px] resize-none"
                placeholder="What are your goals or what value can you bring to others?"
              />
            </div>

            {/* Skills List */}
            <div className="space-y-6">
              <div className="flex justify-between items-center px-1">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-emerald" />
                  <label className="text-xs uppercase tracking-[0.2em] font-black text-slate-500">Skills Portfolio</label>
                </div>
                <button 
                  type="button" 
                  onClick={addSkill}
                  className="flex items-center gap-2 text-xs font-bold text-brand-light hover:text-white transition-colors"
                >
                  <Plus className="w-4 h-4" /> Add Skill
                </button>
              </div>

              <div className="space-y-4">
                <AnimatePresence>
                  {skills.map((skill, index) => (
                    <motion.div 
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      className="p-6 bg-bg-deep/50 border border-white/5 rounded-3xl space-y-4 relative group"
                    >
                      <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1 space-y-2">
                          <input
                            type="text"
                            required
                            value={skill.name}
                            onChange={(e) => updateSkill(index, 'name', e.target.value)}
                            className="w-full bg-bg-deep border border-white/5 rounded-2xl py-3 px-4 text-white placeholder-slate-600 focus:outline-none focus:border-brand/30 transition-colors"
                            placeholder="Skill name (e.g. React, UI Design)"
                          />
                        </div>
                        <div className="flex gap-2">
                          <button
                            type="button"
                            onClick={() => updateSkill(index, 'type', SkillType.LEARN)}
                            className={`flex-1 md:w-24 py-3 rounded-2xl text-[10px] uppercase font-black tracking-widest transition-all ${
                              skill.type === SkillType.LEARN 
                                ? 'bg-emerald text-black shadow-lg shadow-emerald/20' 
                                : 'bg-white/5 border border-white/5 text-slate-500 hover:text-slate-300'
                            }`}
                          >
                            Learn
                          </button>
                          <button
                            type="button"
                            onClick={() => updateSkill(index, 'type', SkillType.TEACH)}
                            className={`flex-1 md:w-24 py-3 rounded-2xl text-[10px] uppercase font-black tracking-widest transition-all ${
                              skill.type === SkillType.TEACH 
                                ? 'bg-brand text-white shadow-lg shadow-brand/20' 
                                : 'bg-white/5 border border-white/5 text-slate-500 hover:text-slate-300'
                            }`}
                          >
                            Teach
                          </button>
                        </div>
                      </div>

                      <textarea
                        value={skill.description}
                        onChange={(e) => updateSkill(index, 'description', e.target.value)}
                        className="w-full bg-bg-deep border border-white/5 rounded-2xl p-4 text-sm text-slate-300 placeholder-slate-700 focus:outline-none focus:border-brand/30 transition-colors min-h-[80px] resize-none"
                        placeholder="Describe your current level or what you want to achieve..."
                      />

                      {skills.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeSkill(index)}
                          className="absolute -top-2 -right-2 w-8 h-8 bg-rose-500/10 text-rose-500 rounded-full flex items-center justify-center border border-rose-500/20 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-rose-500 hover:text-white"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-white text-black py-6 rounded-3xl font-bold text-xl flex items-center justify-center gap-3 hover:bg-slate-200 transition-all shadow-2xl disabled:opacity-50"
            >
              {loading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                <>Finish Profile <CheckCircle2 className="w-6 h-6" /></>
              )}
            </button>
          </form>
        </div>

        <div className="mt-12 text-center text-[10px] uppercase tracking-[0.4em] font-black text-slate-700">
          Step 2 of 2: Profile Customization
        </div>
      </motion.div>
    </div>
  );
}
