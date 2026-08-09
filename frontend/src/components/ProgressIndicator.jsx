import React from 'react';
import { Target, CheckCircle2, Clock } from 'lucide-react';

export default function ProgressIndicator({ turnCount = 0, maxTurns = 5, candidateRole }) {
  const percentage = Math.min(100, Math.round((turnCount / maxTurns) * 100));

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-3 mb-4 backdrop-blur">
      <div className="flex items-center justify-between text-xs mb-2">
        <div className="flex items-center space-x-2">
          <Target className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-slate-200">Interview Progress:</span>
          <span className="text-slate-400">
            Question {Math.min(turnCount + 1, maxTurns)} of {maxTurns}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="px-2 py-0.5 rounded-md bg-slate-800 border border-slate-700 text-indigo-300 font-medium text-[11px]">
            {candidateRole || 'Technical Candidate'}
          </span>
          <span className="text-slate-400 font-mono text-xs">{percentage}%</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-500 rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
