import React, { useState, useRef, useEffect } from 'react';
import { Bot, User, Send, AlertCircle, Loader2 } from 'lucide-react';
import ProgressIndicator from './ProgressIndicator';

export default function ChatInterface({
  messages,
  onSendMessage,
  loading,
  error,
  turnCount,
  maxTurns,
  candidate
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="max-w-4xl mx-auto my-4 px-4 flex flex-col h-[calc(100vh-100px)]">
      {/* Progress Header */}
      <ProgressIndicator
        turnCount={turnCount}
        maxTurns={maxTurns}
        candidateRole={candidate?.jobRole}
      />

      {/* Error Alert */}
      {error && (
        <div className="mb-4 bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 flex items-center space-x-2 text-rose-300 text-xs">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Messages Scroll Window */}
      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl p-4 overflow-y-auto space-y-4 shadow-xl">
        {messages.map((msg, index) => {
          const isAI = msg.role === 'interviewer';

          return (
            <div
              key={index}
              className={`flex items-start space-x-3 ${
                isAI ? 'justify-start' : 'justify-end flex-row-reverse space-x-reverse'
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  isAI
                    ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                    : 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                }`}
              >
                {isAI ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>

              {/* Message Content */}
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  isAI
                    ? 'bg-slate-800/80 text-slate-100 border border-slate-700/60 rounded-tl-none shadow-md'
                    : 'bg-indigo-600 text-white rounded-tr-none shadow-md shadow-indigo-600/20'
                }`}
              >
                <div className="text-[10px] font-bold tracking-wider uppercase mb-1 opacity-70">
                  {isAI ? 'Interviewer Agent' : candidate?.name || 'Candidate'}
                </div>
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>
            </div>
          );
        })}

        {/* Typing Loading Indicator */}
        {loading && (
          <div className="flex items-start space-x-3 justify-start">
            <div className="w-8 h-8 rounded-lg bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-slate-800/80 text-slate-400 border border-slate-700/60 rounded-2xl rounded-tl-none px-4 py-3 text-xs flex items-center space-x-2">
              <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
              <span>Analyzing response & formulating follow-up question...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mt-4 flex space-x-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your technical response here... (Press Shift+Enter for new line)"
          rows={2}
          disabled={loading}
          className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 resize-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="px-5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold flex items-center justify-center shadow-lg shadow-indigo-600/30 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
