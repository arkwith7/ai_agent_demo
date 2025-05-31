<template>
  <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
    <div class="container mx-auto px-4 py-2 flex justify-between items-center">
      <router-link to="/" class="text-primary hover:text-primary/80 transition-colors text-xl font-bold flex items-center">
        AI 투자 분석
      </router-link>
      <nav class="flex items-center space-x-6">
        <router-link to="/intro-ai-agent" class="text-secondary hover:text-primary transition-colors">
          AI Agent 소개
        </router-link>
        <a href="#" @click.prevent="goAnalysis" class="text-secondary hover:text-primary transition-colors">
          투자 분석
        </a>
        <router-link v-if="!isAuthenticated" to="/signin" class="text-secondary hover:text-primary transition-colors">
          Sign In
        </router-link>
        <button
          v-else
          @click="handleLogout"
          class="flex items-center space-x-1 text-primary hover:text-primary/80 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
          </svg>
          <span>Log Out</span>
        </button>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'
import emitter from '../eventBus'

const router = useRouter()
const isAuthenticated = ref(false)

const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
}

const handleLogout = () => {
  authService.logout()
  isAuthenticated.value = false
  emitter.emit('auth-change')
}

const handleAuthChange = () => {
  checkAuth()
}

const goAnalysis = () => {
  if (isAuthenticated.value) {
    router.push('/analysis')
  } else {
    router.push({ name: 'signin', query: { redirect: '/analysis' } })
  }
}

onMounted(() => {
  checkAuth()
  emitter.on('auth-change', handleAuthChange)
})

onUnmounted(() => {
  emitter.off('auth-change', handleAuthChange)
})
</script>

<style scoped>
header {
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.95);
}
</style> 