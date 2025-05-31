<template>
  <div class="min-h-screen bg-light">
    <!-- 상단 네비게이션 -->
    <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
      <div class="container mx-auto px-4 py-2 flex justify-between items-center">
        <router-link to="/" class="text-primary hover:text-primary/80 transition-colors">
          <h1 class="text-xl font-bold flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
            </svg>
            AI 투자 분석
          </h1>
        </router-link>
        <nav class="flex items-center space-x-6">
          <router-link to="/intro-ai-agent" class="text-secondary hover:text-primary transition-colors">
            AI Agent 소개
          </router-link>
          <router-link to="/analysis" class="text-secondary hover:text-primary transition-colors">
            투자 분석
          </router-link>
          <span class="text-primary font-medium">Sign In</span>
        </nav>
      </div>
    </header>

    <main class="pt-16">
      <div class="min-h-[calc(100vh-4rem)] flex items-start justify-center pt-8">
        <div class="w-full max-w-md p-6 space-y-4 bg-white rounded-lg shadow-lg">
          <div class="text-center">
            <h2 class="text-2xl font-bold text-primary">로그인</h2>
            <p class="mt-1 text-secondary">AI 투자 분석 서비스를 이용하세요</p>
          </div>
          
          <form class="mt-4 space-y-4" @submit.prevent="handleLogin">
            <div v-if="error" class="p-3 bg-red-50 text-red-600 rounded-md text-sm">
              {{ error }}
            </div>

            <div class="space-y-4">
              <div>
                <label for="email" class="block text-sm font-medium text-secondary">이메일</label>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  placeholder="your@email.com"
                />
              </div>
              
              <div>
                <label for="password" class="block text-sm font-medium text-secondary">비밀번호</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  v-model="rememberMe"
                  type="checkbox"
                  class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
                />
                <label for="remember-me" class="ml-2 block text-sm text-secondary">
                  로그인 상태 유지
                </label>
              </div>

              <div class="text-sm">
                <a href="#" class="text-primary hover:text-primary/80">
                  비밀번호를 잊으셨나요?
                </a>
              </div>
            </div>

            <div>
              <button
                type="submit"
                :disabled="isLoading"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isLoading ? '로그인 중...' : '로그인' }}
              </button>
            </div>
          </form>

          <div class="mt-6">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white text-secondary">
                  또는
                </span>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-2 gap-3">
              <button
                type="button"
                class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-secondary hover:bg-gray-50"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
                </svg>
                <span class="ml-2">Google</span>
              </button>

              <button
                type="button"
                class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-secondary hover:bg-gray-50"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/>
                </svg>
                <span class="ml-2">Facebook</span>
              </button>
            </div>
          </div>

          <div class="text-center mt-6">
            <p class="text-sm text-secondary">
              계정이 없으신가요?
              <router-link to="/signup" class="text-primary hover:text-primary/80 font-medium">
                회원가입
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authService } from '../services/api'
import emitter from '../eventBus'

const route = useRoute()
const router = useRouter()
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const error = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = '이메일과 비밀번호를 모두 입력해주세요.'
    return
  }

  try {
    isLoading.value = true
    error.value = ''
    await authService.login(email.value, password.value)
    emitter.emit('auth-change')
    const redirect = route.query.redirect || '/'
    window.location.href = redirect
  } catch (error) {
    console.error('Login error:', error)
    error.value = '로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 상단 네비게이션 고정 스타일 */
header {
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.95);
}

/* 네비게이션 링크 스타일 */
.router-link-active {
  color: theme('colors.primary');
  font-weight: 500;
}
</style> 