import axios from 'axios';

const API_URL = '/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        // 새로운 토큰으로 원래 요청의 헤더 업데이트
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        
        // 새로운 axios 인스턴스로 요청 재시도
        return axios(originalRequest);
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/signin';
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async login(email, password) {
    const response = await api.post('/auth/login', {
      email,
      password
    });
    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/signin';
  },

  getCurrentUser() {
    return api.get('/users/me');
  },
};

export const chatService = {
  async sendMessage(message) {
    const response = await api.post('/ai/chat', { query: message });
    return response.data;
  },

  async getChatHistory(page = 1, size = 20) {
    const response = await api.get(`/ai/me/chat-history?page=${page}&size=${size}`);
    return response.data;
  },

  async searchChatHistory(keyword, startDate, endDate, page = 1, size = 20) {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString()
    });
    if (keyword) params.append('keyword', keyword);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await api.get(`/ai/me/chat-history/search?${params.toString()}`);
    return response.data;
  },

  async summarizeChatHistory(historyId) {
    const response = await api.post(`/ai/me/chat-history/${historyId}/summarize`);
    return response.data;
  }
};

export default api; 