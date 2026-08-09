import React, { useState, useEffect } from 'react';
import { User, Briefcase, Award, AlertTriangle, Code, Play, FileText, CheckCircle } from 'lucide-react';
import { fetchSampleCandidates } from '../services/api';

const DEFAULT_CANDIDATE = {
  id: "cand-101",
  name: "Alex Chen",
  jobRole: "Senior AI Engineer",
  yearsExperience: 5,
  education: "M.S. in Computer Science",
  status: "active",
  completedMissions: ["m1_env_setup", "m2_git_workflow", "m3_docker_basics", "m4_pandas_wrangling", "m7_embeddings_calc", "m8_vector_db_setup", "m9_rag_retrieval_basic", "m10_prompt_crafting", "m11_llm_api_integration", "m14_fastapi_backend", "m17_tool_calling", "m18_react_agent", "m19_mcp_server", "m21_ragas_eval", "m23_docker_cloud_deploy"],
  failedMissions: ["m22_prompt_security"],
  skippedMissions: ["m5_data_cleaning", "m6_json_parsing"],
  missionAttempts: {
    "m1_env_setup": 1,
    "m7_embeddings_calc": 1,
    "m8_vector_db_setup": 1,
    "m17_tool_calling": 1,
    "m19_mcp_server": 1,
    "m22_prompt_security": 3
  },
  signals: {
    commitDays: 28,
    missionsCompleted: 15,
    missionsFirstTry: 13
  }
};

export default function CandidateStartModal({ onStartInterview, loading }) {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(DEFAULT_CANDIDATE);
  const [activeTab, setActiveTab] = useState('presets'); // 'presets' | 'json'
  const [jsonText, setJsonText] = useState(JSON.stringify(DEFAULT_CANDIDATE, null, 2));
  const [jsonError, setJsonError] = useState('');

  useEffect(() => {
    async function loadPresets() {
      const data = await fetchSampleCandidates();
      if (data && data.length > 0) {
        setCandidates(data);
        setSelectedCandidate(data[0]);
        setJsonText(JSON.stringify(data[0], null, 2));
      }
    }
    loadPresets();
  }, []);

  const handleSelectPreset = (candidate) => {
    setSelectedCandidate(candidate);
    setJsonText(JSON.stringify(candidate, null, 2));
    setJsonError('');
  };

  const handleJsonChange = (e) => {
    const val = e.target.value;
    setJsonText(val);
    try {
      const parsed = JSON.parse(val);
      setSelectedCandidate(parsed);
      setJsonError('');
    } catch (err) {
      setJsonError('Invalid JSON syntax');
    }
  };

  const handleStart = () => {
    if (activeTab === 'json' && jsonError) return;
    onStartInterview(selectedCandidate);
  };

  return (
    <div className="max-w-4xl mx-auto my-8 px-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-900/50 via-slate-900 to-slate-900 p-6 border-b border-slate-800">
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
              <User className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-100">Select Candidate Profile</h2>
              <p className="text-sm text-slate-400">Personalizes interview questions based on role, mission attempts, and performance signals.</p>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex space-x-2 mt-4">
            <button
              onClick={() => setActiveTab('presets')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === 'presets'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-slate-800/80 text-slate-400 hover:text-slate-200'
              }`}
            >
              Preset Cohort Profiles
            </button>
            <button
              onClick={() => setActiveTab('json')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition ${
                activeTab === 'json'
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-slate-800/80 text-slate-400 hover:text-slate-200'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Custom Candidate JSON</span>
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6">
          {activeTab === 'presets' ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {candidates.map((cand) => {
                const isSelected = selectedCandidate?.id === cand.id;
                return (
                  <div
                    key={cand.id}
                    onClick={() => handleSelectPreset(cand)}
                    className={`cursor-pointer rounded-xl p-4 border transition-all ${
                      isSelected
                        ? 'bg-indigo-950/40 border-indigo-500 shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500'
                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700 hover:bg-slate-800/80'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold text-slate-100 text-base">{cand.name}</h3>
                        <p className="text-xs text-indigo-400 font-medium">{cand.jobRole}</p>
                      </div>
                      {isSelected && <CheckCircle className="w-5 h-5 text-indigo-400" />}
                    </div>

                    <div className="space-y-1.5 text-xs text-slate-400 mt-3 pt-3 border-t border-slate-800">
                      <div className="flex justify-between">
                        <span>Experience:</span>
                        <span className="font-medium text-slate-200">{cand.yearsExperience} yrs</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Commit Days:</span>
                        <span className="font-medium text-slate-200">{cand.signals?.commitDays || 0} days</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Missions Passed:</span>
                        <span className="font-medium text-slate-200">{cand.completedMissions?.length || 0}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Struggled/Failed:</span>
                        <span className="font-medium text-rose-400">{cand.failedMissions?.length || 0}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="mb-6">
              <label className="block text-xs font-semibold text-slate-400 mb-2">Candidate Payload JSON:</label>
              <textarea
                value={jsonText}
                onChange={handleJsonChange}
                rows={10}
                className="w-full font-mono text-xs bg-slate-950 text-indigo-300 p-3 rounded-xl border border-slate-800 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
              {jsonError && (
                <div className="flex items-center space-x-1.5 mt-2 text-rose-400 text-xs">
                  <AlertTriangle className="w-4 h-4" />
                  <span>{jsonError}</span>
                </div>
              )}
            </div>
          )}

          {/* Active Selection Details Preview */}
          {selectedCandidate && (
            <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800 mb-6">
              <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400 mb-3">Interview Context Analysis</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                <div>
                  <span className="text-slate-500 block">Candidate Name</span>
                  <span className="font-semibold text-slate-200">{selectedCandidate.name}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Target Role</span>
                  <span className="font-semibold text-indigo-400">{selectedCandidate.jobRole}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Education</span>
                  <span className="font-semibold text-slate-200">{selectedCandidate.education}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Focus Areas</span>
                  <span className="font-semibold text-amber-400">
                    {selectedCandidate.failedMissions?.length ? `Probe: ${selectedCandidate.failedMissions[0]}` : 'General Advanced'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Start Action */}
          <div className="flex justify-end">
            <button
              onClick={handleStart}
              disabled={loading || (activeTab === 'json' && !!jsonError)}
              className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-sm shadow-xl shadow-indigo-600/30 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Initializing Interview...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  <span>Start Personalized Interview</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
