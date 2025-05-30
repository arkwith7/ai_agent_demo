<template>
  <div class="signup-container">
    <div class="signup-box">
      <h2>회원가입</h2>
      <form @submit.prevent="handleSignup">
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
          <label for="confirmPassword">비밀번호 확인</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            placeholder="비밀번호를 다시 입력하세요"
          />
        </div>
        <button type="submit" class="signup-button">회원가입</button>
      </form>
      <div class="signup-footer">
        <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    // TODO: 실제 회원가입 로직 구현
    console.log('Signup attempt:', {
      name: name.value,
      email: email.value,
      password: password.value
    })
    router.push('/login')
  } catch (error) {
    console.error('Signup failed:', error)
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 20px;
}

.signup-box {
  background: var(--card-bg);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: var(--text-color);
  margin-bottom: 30px;
  font-size: 2em;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-color);
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  font-size: 1em;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.signup-button {
  width: 100%;
  padding: 12px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.signup-button:hover {
  background: var(--hover-darken-primary);
}

.signup-footer {
  text-align: center;
  margin-top: 20px;
  color: var(--secondary-color);
}

.signup-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.signup-footer a:hover {
  text-decoration: underline;
}
</style> 