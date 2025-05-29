<template>
  <div class="login">
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="이메일을 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="비밀번호를 입력하세요"
          />
        </div>
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>로그인 상태 유지</span>
          </label>
          <router-link to="/forgot-password" class="forgot-password">
            비밀번호를 잊으셨나요?
          </router-link>
        </div>
        <button type="submit" class="login-button" :disabled="isLoading">
          <span v-if="!isLoading">로그인</span>
          <div v-else class="loading-spinner"></div>
        </button>
      </form>

      <div class="social-login">
        <p>소셜 계정으로 로그인</p>
        <div class="social-buttons">
          <button class="social-button google">
            <i class="fab fa-google"></i>
            Google
          </button>
          <button class="social-button naver">
            <i class="fas fa-n"></i>
            Naver
          </button>
          <button class="social-button kakao">
            <i class="fas fa-k"></i>
            Kakao
          </button>
        </div>
      </div>

      <div class="signup-link">
        계정이 없으신가요?
        <router-link to="/signup">회원가입</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import '@fortawesome/fontawesome-free/css/all.css'

const router = useRouter()
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)

const handleLogin = async () => {
  try {
    isLoading.value = true
    // TODO: API 연동
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #666;
}

input[type="email"],
input[type="password"] {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="email"]:focus,
input[type="password"]:focus {
  border-color: #4CAF50;
  outline: none;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.forgot-password {
  color: #4CAF50;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  padding: 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 48px;
}

.login-button:hover:not(:disabled) {
  background: #45a049;
}

.login-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.social-login {
  margin-top: 2rem;
  text-align: center;
}

.social-login p {
  color: #666;
  margin-bottom: 1rem;
  position: relative;
}

.social-login p::before,
.social-login p::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: #e0e0e0;
}

.social-login p::before {
  left: 0;
}

.social-login p::after {
  right: 0;
}

.social-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.social-button {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  background: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.social-button i {
  font-size: 1.2rem;
}

.social-button.google:hover {
  background: #f1f1f1;
}

.social-button.naver:hover {
  background: #03c75a;
  color: white;
}

.social-button.kakao:hover {
  background: #fee500;
}

.signup-link {
  margin-top: 2rem;
  text-align: center;
  color: #666;
}

.signup-link a {
  color: #4CAF50;
  text-decoration: none;
  margin-left: 0.5rem;
}

.signup-link a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-container {
    padding: 1.5rem;
  }

  .social-buttons {
    grid-template-columns: 1fr;
  }
}
</style> 