import React from 'react';
import { Award, CheckCircle2, AlertTriangle, ArrowRight, RefreshCw, FileText, Download } from 'lucide-react';

export default function FeedbackDashboard({ candidate, feedback, onRestart }) {
  if (!feedback) return null;

  const { summary, strengths = [], gaps = [], next = [] } = feedback;

  const handleExportJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ candidate, feedback }, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `interview_feedback_${candidate?.name || 'candidate'}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="max-w-5xl mx-auto my-6 px-4 space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-indigo-950/60 border border-emerald-500/30 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center flex-shrink-0">
              <Award className="w-7 h-7" />
            </div>
            <div>
              <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold mb-1">
                <span>Interview Completed</span>
              </div>
              <h2 className="text-2xl font-bold text-slate-100">{candidate?.name || 'Candidate'} Evaluation Report</h2>
              <p className="text-xs text-slate-400">{candidate?.jobRole} • Cohort Technical Assessment</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleExportJSON}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 flex items-center space-x-1.5 transition"
            >
              <Download className="w-4 h-4" />
              <span>Export JSON Report</span>
            </button>
            <button
              onClick={onRestart}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center space-x-1.5 transition"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Start New Interview</span>
            </button>
          </div>
        </div>
      </div>

      {/* Summary Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h3 className="text-xs uppercase font-bold tracking-wider text-indigo-400 mb-2 flex items-center space-x-2">
          <FileText className="w-4 h-4" />
          <span>Executive Evaluation Summary</span>
        </h3>
        <p className="text-slate-200 text-sm leading-relaxed">{summary}</p>
      </div>

      {/* Grid for Strengths, Skill Gaps, Next Steps */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Strengths Card */}
        <div className="bg-slate-900 border border-emerald-500/20 rounded-2xl p-5 shadow-xl flex flex-col">
          <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm mb-4 pb-2 border-b border-slate-800">
            <CheckCircle2 className="w-5 h-5" />
            <span>Key Technical Strengths</span>
          </div>
          <ul className="space-y-3 flex-1">
            {strengths.map((str, idx) => (
              <li key={idx} className="flex items-start space-x-2.5 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Skill Gaps Card */}
        <div className="bg-slate-900 border border-amber-500/20 rounded-2xl p-5 shadow-xl flex flex-col">
          <div className="flex items-center space-x-2 text-amber-400 font-bold text-sm mb-4 pb-2 border-b border-slate-800">
            <AlertTriangle className="w-5 h-5" />
            <span>Identified Skill Gaps</span>
          </div>
          <ul className="space-y-3 flex-1">
            {gaps.map((gap, idx) => (
              <li key={idx} className="flex items-start space-x-2.5 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                <span>{gap}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Next Steps Card */}
        <div className="bg-slate-900 border border-indigo-500/20 rounded-2xl p-5 shadow-xl flex flex-col">
          <div className="flex items-center space-x-2 text-indigo-400 font-bold text-sm mb-4 pb-2 border-b border-slate-800">
            <ArrowRight className="w-5 h-5" />
            <span>Actionable Next Steps</span>
          </div>
          <ul className="space-y-3 flex-1">
            {next.map((step, idx) => (
              <li key={idx} className="flex items-start space-x-2.5 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 flex-shrink-0" />
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
