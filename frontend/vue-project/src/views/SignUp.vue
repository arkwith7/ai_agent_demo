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
          <router-link to="/signin" class="text-secondary hover:text-primary transition-colors">
            Sign In
          </router-link>
        </nav>
      </div>
    </header>

    <main class="pt-16">
      <div class="min-h-[calc(100vh-4rem)] flex items-start justify-center pt-8">
        <div class="w-full max-w-md p-6 space-y-4 bg-white rounded-lg shadow-lg">
          <div class="text-center">
            <h2 class="text-2xl font-bold text-primary">회원가입</h2>
            <p class="mt-1 text-secondary">AI 투자 분석 서비스의 회원이 되어보세요</p>
          </div>
          
          <form class="mt-4 space-y-4" @submit.prevent="handleSignUp">
            <div v-if="error" class="p-3 bg-red-50 text-red-600 rounded-md text-sm">
              {{ error }}
            </div>

            <div class="space-y-3">
              <div>
                <label for="name" class="block text-sm font-medium text-secondary">이름</label>
                <input
                  id="name"
                  v-model="name"
                  type="text"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  placeholder="홍길동"
                />
              </div>

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
                <p class="mt-1 text-sm text-gray-500">8자 이상의 영문, 숫자, 특수문자 조합</p>
              </div>

              <div>
                <label for="passwordConfirm" class="block text-sm font-medium text-secondary">비밀번호 확인</label>
                <input
                  id="passwordConfirm"
                  v-model="passwordConfirm"
                  type="password"
                  required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div class="flex items-center">
              <input
                id="terms"
                v-model="agreeTerms"
                type="checkbox"
                required
                class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label for="terms" class="ml-2 block text-sm text-secondary">
                <span>이용약관 및 개인정보 처리방침에 동의합니다</span>
                <a href="#" class="text-primary hover:text-primary/80">(자세히 보기)</a>
              </label>
            </div>

            <div>
              <button
                type="submit"
                :disabled="isLoading"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isLoading ? '처리 중...' : '회원가입' }}
              </button>
            </div>
          </form>

          <div class="text-center mt-6">
            <p class="text-sm text-secondary">
              이미 계정이 있으신가요?
              <router-link to="/signin" class="text-primary hover:text-primary/80 font-medium">
                로그인
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
import { useRouter } from 'vue-router'
import { authService } from '../services/api'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const agreeTerms = ref(false)
const error = ref('')
const isLoading = ref(false)

const handleSignUp = async () => {
  try {
    // 비밀번호 확인
    if (password.value !== passwordConfirm.value) {
      error.value = '비밀번호가 일치하지 않습니다.'
      return
    }

    // 비밀번호 유효성 검사
    if (password.value.length < 8) {
      error.value = '비밀번호는 8자 이상이어야 합니다.'
      return
    }

    isLoading.value = true
    error.value = ''

    // 회원가입 API 호출
    await authService.register({
      username: name.value,
      email: email.value,
      password: password.value
    })
    
    // 회원가입 성공 시 로그인 페이지로 이동
    router.push('/signin')
  } catch (error) {
    console.error('Sign up failed:', error)
    if (error.response?.data?.detail) {
      error.value = error.response.data.detail
    } else {
      error.value = '회원가입 중 오류가 발생했습니다.'
    }
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