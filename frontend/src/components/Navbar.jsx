import React from 'react';
import { Bot, Sparkles, RefreshCw, Cpu } from 'lucide-react';

export default function Navbar({ candidateName, sessionState, onNewInterview }) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 p-0.5 shadow-lg shadow-indigo-500/20 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Bot className="w-5 h-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-bold text-slate-100 text-lg leading-tight tracking-tight">
                AI Technical Interviewer
              </h1>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                v1.0 MVP
              </span>
            </div>
            <p className="text-xs text-slate-400">Personalized Cohort Evaluation Agent</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {candidateName && (
            <div className="hidden md:flex items-center space-x-2 bg-slate-800/60 border border-slate-700/60 px-3 py-1.5 rounded-lg text-xs">
              <span className="text-slate-400">Candidate:</span>
              <span className="font-semibold text-slate-200">{candidateName}</span>
            </div>
          )}

          {sessionState !== 'idle' && (
            <button
              onClick={onNewInterview}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>New Interview</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
