<template>
  <div class="demo-container">
    <div class="chat-container">
      <div class="chat-header">
        <h2>AI Agent와 대화하기</h2>
        <p>원하는 주식 정보나 투자 조언을 자유롭게 물어보세요</p>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.type]"
        >
          <div class="message-content">
            <div class="message-header">
              <i :class="message.type === 'user' ? 'fa-solid fa-user' : 'fa-solid fa-robot'"></i>
              <span>{{ message.type === 'user' ? '사용자' : 'AI Agent' }}</span>
            </div>
            <p>{{ message.content }}</p>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <form @submit.prevent="sendMessage">
          <input
            type="text"
            v-model="newMessage"
            placeholder="메시지를 입력하세요..."
            :disabled="isLoading"
          />
          <button type="submit" :disabled="isLoading || !newMessage.trim()">
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </form>
      </div>
    </div>

    <div class="demo-sidebar">
      <div class="sidebar-section">
        <h3>예시 질문</h3>
        <ul class="example-questions">
          <li v-for="(question, index) in exampleQuestions" :key="index" @click="useExampleQuestion(question)">
            {{ question }}
          </li>
        </ul>
      </div>

      <div class="sidebar-section">
        <h3>주요 기능</h3>
        <ul class="feature-list">
          <li v-for="(feature, index) in features" :key="index">
            <i :class="feature.icon"></i>
            {{ feature.text }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

const messages = ref([
  {
    type: 'agent',
    content: '안녕하세요! 저는 AI Agent입니다. 주식 투자와 관련된 어떤 것이든 물어보세요.'
  }
])

const newMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const exampleQuestions = [
  '삼성전자의 최근 실적은 어때요?',
  '반도체 섹터의 전망을 알려주세요.',
  '배당주 추천해주세요.',
  '테슬라의 주가 전망은 어떻게 되나요?'
]

const features = [
  { icon: 'fa-solid fa-chart-line', text: '실시간 시장 분석' },
  { icon: 'fa-solid fa-comments', text: '자연어 대화' },
  { icon: 'fa-solid fa-lightbulb', text: '스마트 추천' },
  { icon: 'fa-solid fa-shield-alt', text: '리스크 관리' }
]

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMessage = newMessage.value
  messages.value.push({ type: 'user', content: userMessage })
  newMessage.value = ''
  isLoading.value = true

  // TODO: 실제 AI 응답 로직 구현
  setTimeout(() => {
    messages.value.push({
      type: 'agent',
      content: '죄송합니다. 현재는 데모 버전으로 실제 응답을 제공하지 않습니다. 실제 서비스에서는 AI가 실시간으로 분석하여 답변을 제공할 예정입니다.'
    })
    isLoading.value = false
    scrollToBottom()
  }, 1000)

  scrollToBottom()
}

const useExampleQuestion = (question: string) => {
  newMessage.value = question
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.demo-container {
  display: flex;
  gap: 30px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 80px);
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.chat-header {
  padding: 20px;
  background: var(--primary-color);
  color: white;
  text-align: center;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.5em;
}

.chat-header p {
  margin: 10px 0 0;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
}

.message.agent {
  align-self: flex-start;
}

.message-content {
  background: var(--light-bg);
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.message.user .message-content {
  background: var(--primary-color);
  color: white;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 0.9em;
  opacity: 0.8;
}

.message p {
  margin: 0;
  line-height: 1.5;
}

.chat-input {
  padding: 20px;
  background: var(--light-bg);
  border-top: 1px solid var(--border-color);
}

.chat-input form {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  font-size: 1em;
}

.chat-input button {
  padding: 12px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.chat-input button:hover:not(:disabled) {
  background: var(--hover-darken-primary);
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.demo-sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background: var(--card-bg);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.sidebar-section h3 {
  margin: 0 0 15px;
  color: var(--text-color);
  font-size: 1.2em;
}

.example-questions {
  list-style: none;
  padding: 0;
  margin: 0;
}

.example-questions li {
  padding: 10px;
  margin-bottom: 8px;
  background: var(--light-bg);
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.example-questions li:hover {
  background: var(--border-color);
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  color: var(--text-color);
}

.feature-list li i {
  color: var(--primary-color);
}

@media (max-width: 1024px) {
  .demo-container {
    flex-direction: column;
  }

  .demo-sidebar {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .message {
    max-width: 90%;
  }
}
</style> 