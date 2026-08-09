const API_BASE = '/api';

/**
 * Communicates with the mandatory POST /api/interview endpoint.
 */
export async function postInterview(payload) {
  try {
    const response = await fetch(`${API_BASE}/interview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error (${response.status})`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error in postInterview:', error);
    throw error;
  }
}

/**
 * Starts a new interview session.
 */
export async function startInterview(sessionId, candidate) {
  return postInterview({
    sessionId,
    candidate,
  });
}

/**
 * Sends a candidate response during an ongoing interview session.
 */
export async function sendTurnMessage(sessionId, message) {
  return postInterview({
    sessionId,
    message,
  });
}

/**
 * Fetches sample candidate profiles from the backend data directory.
 */
export async function fetchSampleCandidates() {
  try {
    const response = await fetch(`${API_BASE}/candidates`);
    if (!response.ok) return [];
    return await response.json();
  } catch (err) {
    console.warn('Could not fetch sample candidates:', err);
    return [];
  }
}
