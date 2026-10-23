const BACKEND_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_BASE = `${BACKEND_URL.replace(/\/$/, '')}/api`;

export const getAuthToken = () => localStorage.getItem('codeduel_token');
export const setAuthToken = (token) => localStorage.setItem('codeduel_token', token);
export const removeAuthToken = () => localStorage.removeItem('codeduel_token');

export const getCurrentUserStored = () => {
  try {
    const u = localStorage.getItem('codeduel_user');
    if (!u) return null;
    const parsed = JSON.parse(u);
    if (parsed && parsed.profile && parsed.profile.rating === 1200) {
      parsed.profile.rating = 0;
    }
    return parsed;
  } catch (e) {
    return null;
  }
};

export const setCurrentUserStored = (user) => {
  localStorage.setItem('codeduel_user', JSON.stringify(user));
};

async function request(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(options.headers || {})
  };

  let response;
  try {
    response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });
  } catch (netErr) {
    throw new Error('Unable to connect to server. Please ensure the backend is running on port 8000.');
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const msg = data.error || 
      data.detail || 
      (Array.isArray(data.password) ? data.password[0] : (typeof data.password === 'string' ? data.password : null)) ||
      (Array.isArray(data.username) ? data.username[0] : (typeof data.username === 'string' ? data.username : null)) ||
      'API request failed';
    const err = new Error(msg);
    err.data = data;
    err.status = response.status;
    throw err;
  }

  return data;
}

export const api = {
  // Auth
  register: async (username, email, password) => {
    const res = await request('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
    setAuthToken(res.tokens.access);
    setCurrentUserStored(res.user);
    return res;
  },
  login: async (username, password) => {
    const res = await request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    setAuthToken(res.access);
    const user = res.user || (await request('/auth/me/'));
    setCurrentUserStored(user);
    return { tokens: res, user };
  },
  guestLogin: async (username = '') => {
    const res = await request('/auth/guest/', {
      method: 'POST',
      body: JSON.stringify({ username })
    });
    setAuthToken(res.access);
    setCurrentUserStored(res.user);
    return { tokens: res, user: res.user };
  },
  getMe: async () => request('/auth/me/'),
  getLeaderboard: async () => request('/auth/leaderboard/'),
  getOnlineStats: async () => request('/auth/online-stats/'),


  // Problems
  getProblems: async () => request('/problems/'),
  getProblemDetail: async (id) => request(`/problems/${id}/`),

  // Submissions
  submitCode: async ({ problem, battle, language, code }) => {
    return request('/submissions/', {
      method: 'POST',
      body: JSON.stringify({ problem, battle, language, code })
    });
  },
  getSubmissions: async (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/submissions/?${q}`);
  },

  // Battles
  createBattle: async (problem_id = null) => {
    return request('/battles/create/', {
      method: 'POST',
      body: JSON.stringify(problem_id ? { problem_id } : {})
    });
  },
  joinBattle: async (room_code) => {
    return request('/battles/join/', {
      method: 'POST',
      body: JSON.stringify({ room_code })
    });
  },
  getBattle: async (room_code) => request(`/battles/${room_code}/`),
  getActiveBattles: async () => request('/battles/active/'),

  // Matchmaking Queue
  joinMatchmaking: async (difficulty = 'ANY') => {
    return request('/battles/matchmaking/join/', {
      method: 'POST',
      body: JSON.stringify({ difficulty })
    });
  },
  checkMatchmakingStatus: async () => request('/battles/matchmaking/status/'),
  leaveMatchmaking: async () => {
    return request('/battles/matchmaking/leave/', {
      method: 'POST'
    });
  },
};
