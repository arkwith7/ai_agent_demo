import { defineStore } from 'pinia'

interface User {
  id: string
  name: string
  email: string
}

interface UserState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isAuthenticated: false,
    isLoading: false
  }),

  getters: {
    getUser: (state) => state.user,
    getIsAuthenticated: (state) => state.isAuthenticated,
    getIsLoading: (state) => state.isLoading
  },

  actions: {
    async login(email: string, password: string) {
      try {
        this.isLoading = true
        // TODO: API 연동
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 임시 사용자 데이터
        this.user = {
          id: '1',
          name: '테스트 사용자',
          email: email
        }
        this.isAuthenticated = true
        
        // 토큰 저장
        localStorage.setItem('token', 'dummy-token')
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async signup(name: string, email: string, password: string) {
      try {
        this.isLoading = true
        // TODO: API 연동
        await new Promise(resolve => setTimeout(resolve, 1000))
      } catch (error) {
        console.error('Signup failed:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      try {
        this.isLoading = true
        // TODO: API 연동
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
      } catch (error) {
        console.error('Logout failed:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async checkAuth() {
      const token = localStorage.getItem('token')
      if (!token) {
        this.user = null
        this.isAuthenticated = false
        return
      }

      try {
        this.isLoading = true
        // TODO: API 연동
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 임시 사용자 데이터
        this.user = {
          id: '1',
          name: '테스트 사용자',
          email: 'test@example.com'
        }
        this.isAuthenticated = true
      } catch (error) {
        console.error('Auth check failed:', error)
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
      } finally {
        this.isLoading = false
      }
    }
  }
}) 