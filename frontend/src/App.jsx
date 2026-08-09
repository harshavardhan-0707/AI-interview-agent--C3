import React, { useState } from 'react';
import Navbar from './components/Navbar';
import CandidateStartModal from './components/CandidateStartModal';
import ChatInterface from './components/ChatInterface';
import FeedbackDashboard from './components/FeedbackDashboard';
import { startInterview, sendTurnMessage } from './services/api';

export default function App() {
  const [viewState, setViewState] = useState('setup'); // 'setup' | 'interviewing' | 'completed'
  const [sessionId, setSessionId] = useState('');
  const [candidate, setCandidate] = useState(null);
  const [messages, setMessages] = useState([]);
  const [turnCount, setTurnCount] = useState(0);
  const [maxTurns] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState(null);

  // 1. Start Interview Action
  const handleStartInterview = async (selectedCandidate) => {
    setLoading(true);
    setError('');
    const newSessionId = `session-${Date.now()}`;
    setSessionId(newSessionId);
    setCandidate(selectedCandidate);

    try {
      const response = await startInterview(newSessionId, selectedCandidate);
      
      setMessages([
        {
          role: 'interviewer',
          content: response.reply,
        },
      ]);
      setTurnCount(0);
      setViewState('interviewing');
    } catch (err) {
      setError(err.message || 'Failed to start interview session. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // 2. Send Turn Message Action
  const handleSendMessage = async (userMessage) => {
    if (!sessionId || loading) return;

    // Append user candidate message to chat
    const updatedMessages = [
      ...messages,
      { role: 'candidate', content: userMessage },
    ];
    setMessages(updatedMessages);
    setLoading(true);
    setError('');

    try {
      const response = await sendTurnMessage(sessionId, userMessage);

      if (response.done) {
        // Interview Completed
        setFeedback(response.feedback);
        setMessages([
          ...updatedMessages,
          { role: 'interviewer', content: response.reply || 'Interview completed.' },
        ]);
        setViewState('completed');
      } else {
        // Continue Interview
        setMessages([
          ...updatedMessages,
          { role: 'interviewer', content: response.reply },
        ]);
        setTurnCount((prev) => prev + 1);
      }
    } catch (err) {
      setError(err.message || 'Failed to send turn response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // 3. Reset / New Interview Action
  const handleNewInterview = () => {
    setViewState('setup');
    setSessionId('');
    setCandidate(null);
    setMessages([]);
    setTurnCount(0);
    setFeedback(null);
    setError('');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar
        candidateName={candidate?.name}
        sessionState={viewState}
        onNewInterview={handleNewInterview}
      />

      <main className="flex-1">
        {viewState === 'setup' && (
          <CandidateStartModal
            onStartInterview={handleStartInterview}
            loading={loading}
          />
        )}

        {viewState === 'interviewing' && (
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            loading={loading}
            error={error}
            turnCount={turnCount}
            maxTurns={maxTurns}
            candidate={candidate}
          />
        )}

        {viewState === 'completed' && (
          <FeedbackDashboard
            candidate={candidate}
            feedback={feedback}
            onRestart={handleNewInterview}
          />
        )}
      </main>
    </div>
  );
}
