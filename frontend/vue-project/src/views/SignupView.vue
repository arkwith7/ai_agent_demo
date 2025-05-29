<template>
  <div class="signup">
    <div class="signup-container">
      <h1>회원가입</h1>
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label for="name">이름</label>
          <input
            type="text"
            id="name"
            v-model="name"
            required
            placeholder="이름을 입력하세요"
          />
        </div>
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
        <div class="form-group">
          <label for="passwordConfirm">비밀번호 확인</label>
          <input
            type="password"
            id="passwordConfirm"
            v-model="passwordConfirm"
            required
            placeholder="비밀번호를 다시 입력하세요"
          />
        </div>
        <div class="form-group terms">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="agreeToTerms"
              required
            />
            <span>이용약관 및 개인정보 처리방침에 동의합니다</span>
          </label>
        </div>
        <button type="submit" class="signup-button" :disabled="isLoading">
          <span v-if="!isLoading">회원가입</span>
          <div v-else class="loading-spinner"></div>
        </button>
      </form>

      <div class="social-signup">
        <p>소셜 계정으로 가입</p>
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

      <div class="login-link">
        이미 계정이 있으신가요?
        <router-link to="/login">로그인</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import '@fortawesome/fontawesome-free/css/all.css'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const agreeToTerms = ref(false)
const isLoading = ref(false)

const handleSignup = async () => {
  if (password.value !== passwordConfirm.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    isLoading.value = true
    // TODO: API 연동
    await new Promise(resolve => setTimeout(resolve, 1000))
    router.push('/login')
  } catch (error) {
    console.error('Signup failed:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.signup {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 2rem;
}

.signup-container {
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

.signup-form {
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

input[type="text"],
input[type="email"],
input[type="password"] {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus {
  border-color: #4CAF50;
  outline: none;
}

.terms {
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 1.2rem;
  height: 1.2rem;
}

.signup-button {
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

.signup-button:hover:not(:disabled) {
  background: #45a049;
}

.signup-button:disabled {
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

.social-signup {
  margin-top: 2rem;
  text-align: center;
}

.social-signup p {
  color: #666;
  margin-bottom: 1rem;
  position: relative;
}

.social-signup p::before,
.social-signup p::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30%;
  height: 1px;
  background: #e0e0e0;
}

.social-signup p::before {
  left: 0;
}

.social-signup p::after {
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

.login-link {
  margin-top: 2rem;
  text-align: center;
  color: #666;
}

.login-link a {
  color: #4CAF50;
  text-decoration: none;
  margin-left: 0.5rem;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .signup-container {
    padding: 1.5rem;
  }

  .social-buttons {
    grid-template-columns: 1fr;
  }
}
</style> 