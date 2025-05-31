<template>
  <div class="min-h-screen bg-light">
    <main class="container mx-auto px-4 pt-8 pb-8">
      <!-- 모바일 화면에서의 채팅 히스토리 토글 버튼 -->
      <div class="lg:hidden mb-4">
        <button 
          @click="showMobileHistory = !showMobileHistory"
          class="w-full bg-white rounded-lg shadow-sm p-4 flex items-center justify-between"
        >
          <span class="font-medium">채팅 히스토리</span>
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="1.5" 
            stroke="currentColor" 
            class="w-5 h-5 transform transition-transform"
            :class="{ 'rotate-180': showMobileHistory }"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 relative">
        <!-- 토글 버튼: 데스크탑에서만 보임 -->
        <button
          v-if="isLargeScreen"
          @click="toggleHistory"
          class="toggle-history-btn absolute bg-white rounded-full shadow-md p-1 hover:bg-primary/5 transition-colors z-20"
          :style="{ left: isHistoryCollapsed ? '0' : '16rem', top: '2.5rem' }"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="1.5" 
            stroke="currentColor" 
            class="w-4 h-4 transform transition-transform"
            :class="{ 'rotate-180': isHistoryCollapsed }"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
        </button>

        <!-- 히스토리 패널 -->
        <div 
          class="history-panel bg-white rounded-lg shadow-sm p-4 h-[calc(100vh-11rem)] overflow-y-auto transition-all duration-300 ease-in-out relative"
          :class="{
            'w-64 opacity-100 pointer-events-auto': !isHistoryCollapsed && isLargeScreen,
            'w-0 opacity-0 pointer-events-none': isHistoryCollapsed && isLargeScreen,
            'hidden': !showMobileHistory && !isLargeScreen
          }"
        >
          <div v-show="!isHistoryCollapsed">
            <h2 class="text-lg font-bold text-primary mb-4">채팅 히스토리</h2>
            <div class="space-y-2">
              <button 
                v-for="(chat, index) in chatHistory" 
                :key="chat.id"
                @click="loadChat(chat)"
                class="w-full text-left p-2 rounded hover:bg-primary/5 transition-colors"
                :class="{ 'bg-primary/10': selectedChat && selectedChat.id === chat.id }"
              >
                <p class="text-sm font-medium truncate">{{ chat.title }}</p>
                <p class="text-xs text-secondary">{{ chat.date }}</p>
              </button>
            </div>
          </div>
        </div>

        <!-- 채팅 섹션 -->
        <div 
          class="transition-all duration-300"
          :class="{
            'lg:col-span-5': !isHistoryCollapsed && isLargeScreen,
            'lg:col-span-7': isHistoryCollapsed && isLargeScreen,
            'lg:ml-0': !isHistoryCollapsed || !isLargeScreen,
            'lg:ml-8': isHistoryCollapsed && isLargeScreen
          }"
        >
          <div class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-11rem)] flex flex-col">
            <!-- 채팅 메시지 영역 -->
            <div class="flex-1 overflow-y-auto mb-4 space-y-4" ref="chatContainer">
              <div v-for="(message, index) in messages" :key="index" 
                :class="['flex items-start space-x-4', message.isUser ? 'justify-end' : '']">
                <template v-if="!message.isUser">
                  <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-primary">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                    </svg>
                  </div>
                </template>
                <div :class="[
                  'rounded-lg p-4 max-w-[80%]',
                  message.isUser ? 'bg-primary text-white' : 'bg-primary/5'
                ]">
                  <p :class="message.isUser ? 'text-white' : 'text-secondary'">{{ message.content }}</p>
                </div>
                <template v-if="message.isUser">
                  <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-white">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                    </svg>
                  </div>
                </template>
              </div>
            </div>

            <!-- 입력 영역 -->
            <div class="border-t border-gray-200 pt-4">
              <div class="flex space-x-4">
                <input
                  type="text"
                  v-model="userInput"
                  placeholder="분석하고 싶은 종목을 입력하세요..."
                  class="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  @keyup.enter="sendMessage"
                />
                <button
                  @click="sendMessage"
                  class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary/90 transition-colors"
                >
                  전송
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 분석 결과 섹션 -->
        <div 
          class="lg:col-span-5 transition-all duration-300"
          :class="{ 'lg:col-span-6': isHistoryCollapsed && isLargeScreen }"
        >
          <div class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-11rem)] overflow-y-auto">
            <!-- 분석 결과 등 추가 컨텐츠는 필요시 여기에 렌더링 -->
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { chatService } from '../services/api'

const userInput = ref('')
const chatContainer = ref(null)
const showModal = ref(false)
const showRecommendations = ref(false)
const showAnalysis = ref(false)
const selectedStock = ref(null)
const selectedChat = ref(null)
const showMobileHistory = ref(false)
const isLargeScreen = ref(window.innerWidth >= 1024)
const isHistoryCollapsed = ref(false)

const chatHistory = ref([])
const messages = ref([])

// 화면 크기 변경 감지
const handleResize = () => {
  isLargeScreen.value = window.innerWidth >= 1024
  if (isLargeScreen.value) {
    showMobileHistory.value = false
  }
}

const toggleHistory = () => {
  isHistoryCollapsed.value = !isHistoryCollapsed.value
  if (isHistoryCollapsed.value) {
    nextTick(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  }
}

onMounted(async () => {
  window.addEventListener('resize', handleResize)
  await loadChatHistory()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  // 사용자 메시지 추가
  const userMessage = {
    content: userInput.value,
    isUser: true
  }
  messages.value.push(userMessage)

  try {
    // 실제 백엔드에 메시지 전송
    const response = await chatService.sendMessage(userInput.value)
    const aiResponse = {
      content: response.response,
      isUser: false
    }
    messages.value.push(aiResponse)
  } catch (error) {
    console.error('Failed to send message:', error)
    const errorMessage = {
      content: '죄송합니다. 메시지 전송 중 오류가 발생했습니다.',
      isUser: false
    }
    messages.value.push(errorMessage)
  }

  userInput.value = ''
  await nextTick()
  scrollToBottom()
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const loadChat = (chat) => {
  selectedChat.value = chat
  // 실제로는 chat.id로 백엔드에서 해당 채팅의 메시지 목록을 불러올 수도 있음
  messages.value = chat.messages || []
}

const loadChatHistory = async () => {
  try {
    const history = await chatService.getChatHistory()
    chatHistory.value = history.histories.map(h => ({
      id: h.id,
      title: h.query_text.substring(0, 20) + (h.query_text.length > 20 ? '...' : ''),
      date: new Date(h.created_at).toLocaleString('ko-KR'),
      messages: [
        {
          content: h.query_text,
          isUser: true
        },
        {
          content: h.response_text,
          isUser: false
        }
      ]
    }))
    if (chatHistory.value.length > 0) {
      loadChat(chatHistory.value[0])
    }
  } catch (error) {
    console.error('Failed to load chat history:', error)
  }
}
</script>

<style scoped>
/* 스크롤바 스타일링 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.primary/20') transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: theme('colors.primary/20');
  border-radius: 3px;
}

/* 상단 네비게이션 고정 스타일 */
header {
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.95);
}

/* 컨텐츠 영역 높이 조정 */
.h-\[calc\(100vh-8rem\)\] {
  height: calc(100vh - 8rem);
}

@media (max-width: 1023px) {
  .h-\[calc\(100vh-8rem\)\] {
    height: calc(100vh - 6rem);
  }
}

/* 히스토리 섹션 전환 애니메이션 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* 히스토리 패널 트랜지션 */
.history-panel {
  transition: width 0.3s cubic-bezier(0.4,0,0.2,1), opacity 0.3s cubic-bezier(0.4,0,0.2,1);
  width: 16rem;
  min-width: 0;
  max-width: 100vw;
  overflow: hidden;
}
.history-panel.w-0 {
  width: 0 !important;
}

/* 히스토리 토글 버튼 스타일 */
.absolute.-right-3 {
  right: -0.75rem;
}

/* 히스토리가 접혔을 때의 여백 조정 */
.lg\:ml-8 {
  margin-left: 2rem;
}

.toggle-history-btn {
  transition: left 0.3s cubic-bezier(0.4,0,0.2,1);
  z-index: 20;
}
</style> 