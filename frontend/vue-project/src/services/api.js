import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

console.log('API URL:', API_BASE_URL); // API URL 확인용 로그

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5분으로 증가
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    console.log('Request:', config.method.toUpperCase(), config.url, config.data); // 요청 로깅
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => {
    console.log('Response:', response.status, response.data); // 응답 로깅
    return response;
  },
  async (error) => {
    console.error('Response Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });

    const originalRequest = error.config;
    
    // 연결 오류 처리
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      throw new Error('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.');
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        return axios(originalRequest);
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/signin';
        return Promise.reject(error);
      }
    }

    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('요청 시간이 초과되었습니다. 다시 시도해주세요.'));
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
  async collectMarketData() {
    const response = await api.post('/analysis/collect-market-data');
    return response.data;
  },

  async sendMessage(message, messageType = 'general_chat') {
    const response = await api.post('/chat/message', {
      content: message,
      message_type: messageType
    });
    return response.data;
  },

  async getStockRecommendations(params = {}) {
    const response = await api.post('/analysis/recommendations/from-latest', params);
    return response.data;
  },

  async getStockAnalysis(stockCode) {
    const response = await api.get(`/analysis/stock/${stockCode}`);
    return response.data;
  },

  async getChatHistory(page = 1, size = 20) {
    const response = await api.get(`/chat/history?page=${page}&size=${size}`);
    return response.data;
  },

  async searchChatHistory(keyword, startDate, endDate, page = 1, size = 20) {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString()
      });
      if (keyword) params.append('keyword', keyword);
      if (startDate) params.append('start_date', startDate);
      if (endDate) params.append('end_date', endDate);
      
      const response = await api.get(`/chat/history/search?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error searching chat history:', error);
      throw new Error('채팅 기록 검색에 실패했습니다.');
    }
  },

  async summarizeChatHistory(historyId) {
    try {
      const response = await api.post(`/chat/history/${historyId}/summarize`);
      return response.data;
    } catch (error) {
      console.error('Error summarizing chat history:', error);
      throw new Error('채팅 기록 요약에 실패했습니다.');
    }
  }
};

export const analysisService = {
  async getStockRecommendations(query) {
    try {
      const response = await axios.post(`${API_BASE_URL}/analysis/recommend`, {
        query
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching stock recommendations:', error);
      throw error;
    }
  },

  async getStockAnalysis(stockCode) {
    try {
      const response = await axios.get(`${API_BASE_URL}/analysis/detail/${stockCode}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching stock analysis:', error);
      throw error;
    }
  }
};

export const stockAnalysisService = {
  // 종목 추천 API
  async getStockRecommendations(params) {
    try {
      const response = await axios.post(`${API_BASE_URL}/recommend-stocks`, {
        market_segment: params.market_segment || 'KOSPI',
        min_score: params.min_score || 60,
        max_results: params.max_results || 10,
        include_esg: params.include_esg ?? true,
        include_risk_analysis: params.include_risk_analysis ?? true
      })
      return response.data
    } catch (error) {
      throw new Error('종목 추천을 가져오는데 실패했습니다.')
    }
  },

  // 종목 분석 API
  async getStockAnalysis(stockCode) {
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze-stock`, {
        stock_code: stockCode,
        include_esg: true,
        include_risk_analysis: true
      })
      return response.data
    } catch (error) {
      throw new Error('종목 분석을 가져오는데 실패했습니다.')
    }
  }
}

export default api; 