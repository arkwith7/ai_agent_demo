<template>
  <div class="min-h-screen bg-light">
    <main class="container mx-auto px-8 pt-8 pb-8">
      <!-- 데이터 수집 섹션 추가 -->
      <div class="mb-6 bg-white rounded-lg shadow-sm p-4">
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">시장 데이터</h2>
          <div class="flex items-center space-x-4">
            <span v-if="collectionStatus" :class="[
              'text-sm',
              collectionStatus.success ? 'text-green-600' : 'text-red-600'
            ]">
              {{ collectionStatus.message }}
            </span>
            <button
              @click="collectMarketData"
              :disabled="isCollecting"
              class="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
            >
              {{ isCollecting ? '수집 중...' : '시장 데이터 수집' }}
            </button>
          </div>
        </div>
      </div>

      <div class="flex flex-row justify-center items-start gap-2 relative">
        <!-- 히스토리 패널 -->
        <div 
          v-show="!isHistoryCollapsed"
          class="history-panel bg-white rounded-lg shadow-sm p-4 h-[calc(100vh-11rem)] overflow-y-auto transition-all duration-300 ease-in-out relative"
          style="width: 200px; min-width: 120px;"
        >
          <div class="flex items-center space-x-2 mb-2">
            <button
              @click="toggleHistory"
              class="bg-primary text-white rounded-full p-3 shadow-md hover:bg-primary/90 transition-colors z-20"
              style="position: static;"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>
            <button
              @click="startNewChat"
              class="text-left px-3 py-1 rounded bg-primary text-white hover:bg-primary/90 transition-colors font-medium text-xs"
              style="min-width: 90px;"
            >
              + New chat
            </button>
          </div>
          <div v-show="!isHistoryCollapsed">
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

        <!-- 히스토리 토글 버튼 (버블 버튼) -->
        <button
          v-show="isHistoryCollapsed"
          @click="toggleHistory"
          class="absolute top-4 left-4 bg-primary text-white rounded-full p-3 shadow-md hover:bg-primary/90 transition-colors z-10"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6" />
          </svg>
        </button>

        <!-- 분석 결과 섹션 -->
        <div 
          class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-11rem)] overflow-y-auto transition-all duration-300"
          style="width: 450px; min-width: 250px;"
        >
          <template v-if="isLoading">
            <div class="flex flex-col items-center justify-center h-full">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <p class="mt-4 text-secondary">분석 중입니다...</p>
              <p class="text-sm text-secondary mt-2">잠시만 기다려주세요.</p>
            </div>
          </template>
          
          <template v-else-if="error">
            <div class="text-red-500 p-4 rounded-lg bg-red-50">
              <p class="font-semibold">오류가 발생했습니다</p>
              <p class="text-sm mt-2">{{ error }}</p>
              <button 
                @click="retryAnalysis" 
                class="mt-4 px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200"
              >
                다시 시도
              </button>
            </div>
          </template>
          
          <template v-else-if="analysisResult">
            <!-- 종목 추천 결과 -->
            <template v-if="analysisResult.message_type === 'stock_recommendation'">
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <h2 class="text-xl font-semibold">추천 종목</h2>
                  <span class="text-sm text-secondary">총 {{ analysisResult.analysis_result?.length || 0 }}개</span>
                </div>
                
                <template v-if="!analysisResult.analysis_result || analysisResult.analysis_result.length === 0">
                  <div class="text-secondary/80 text-center py-8">
                    <p class="text-lg font-semibold">추천 종목 없음</p>
                    <p>현재 조건에 맞는 추천 종목을 찾지 못했습니다.</p>
                  </div>
                </template>
                
                <div v-else class="space-y-4">
                  <div v-for="(stock, index) in displayedRecommendations" :key="index" 
                       class="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
                    <div class="flex justify-between items-start mb-2">
                      <div>
                        <h3 class="text-lg font-semibold">{{ stock.name }}</h3>
                        <span :class="[
                          'inline-block px-2 py-1 rounded text-xs font-medium',
                          stock.market === 'KOSPI' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'
                        ]">
                          {{ stock.market }}
                        </span>
                      </div>
                      <div class="text-right">
                        <p class="text-lg font-semibold">{{ formatNumber(stock.currentPrice) }}원</p>
                        <p :class="[
                          'text-sm',
                          stock.changeRate > 0 ? 'text-red-500' : stock.changeRate < 0 ? 'text-blue-500' : 'text-gray-500'
                        ]">
                          {{ stock.changeRate > 0 ? '+' : '' }}{{ formatNumber(stock.changeRate) }}%
                        </p>
                      </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-2 text-sm mb-3">
                      <div>
                        <p class="text-secondary">거래량</p>
                        <p class="font-medium">{{ formatNumber(stock.volume) }}</p>
                      </div>
                      <div>
                        <p class="text-secondary">시가총액</p>
                        <p class="font-medium">{{ formatNumber(stock.marketCap) }}원</p>
                      </div>
                    </div>
                    
                    <div class="border-t pt-3">
                      <p class="text-sm text-secondary">추천 이유</p>
                      <p class="text-sm">{{ stock.reason }}</p>
                    </div>
                  </div>
                </div>

                <!-- 페이지네이션 -->
                <div v-if="analysisResult.analysis_result && analysisResult.analysis_result.length > itemsPerPage" 
                     class="flex justify-center items-center space-x-4 mt-4">
                  <button 
                    @click="currentPage--" 
                    :disabled="currentPage === 1"
                    class="px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    이전
                  </button>
                  <span class="text-sm text-secondary">
                    {{ currentPage }} / {{ totalPages }}
                  </span>
                  <button 
                    @click="currentPage++" 
                    :disabled="currentPage === totalPages"
                    class="px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    다음
                  </button>
                </div>
              </div>
            </template>
            
            <!-- 종목 상세 분석 결과 -->
            <template v-else-if="analysisResult.message_type === 'stock_analysis'">
              <StockAnalysisResult
                :analysis="analysisResult.analysis_result"
                :show-esg="showESGAnalysis"
                :show-risk="showRiskAnalysis"
                @back="backToRecommendations"
              />
            </template>
          </template>
          
          <template v-else>
            <div class="text-secondary/80 text-center py-12">
              <div class="text-lg font-semibold mb-2">분석 결과 안내</div>
              <div>아직 분석 결과가 없습니다.<br>종목을 입력하거나 추천을 받아보세요.</div>
            </div>
          </template>
        </div>

        <!-- 채팅 섹션 -->
        <div 
          class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-11rem)] flex flex-col transition-all duration-300"
          style="width: 400px; min-width: 250px;"
        >
          <!-- 채팅 메시지 영역 -->
          <div class="flex-1 overflow-y-auto mb-4 space-y-4" ref="chatContainer">
            <template v-if="messages.length === 0">
              <div class="flex flex-col items-center justify-center h-full text-center text-secondary/80 py-12">
                <div class="text-lg font-semibold mb-2">AI 투자분석 챗봇</div>
                <div class="mb-2">분석이 필요한 종목을 입력하거나, 종목 추천을 받아보세요.</div>
                <div class="text-xs text-secondary">예시: "삼성전자 분석해줘", "2025년 유망한 종목 추천해줘"</div>
              </div>
            </template>
            <template v-else>
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
            </template>
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
                class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary/90 transition-colors flex items-center justify-center"
              >
                <!-- Paper Airplane 아이콘 -->
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount, watch, computed } from 'vue'
import { chatService } from '../services/api'
import StockRecommendationList from '../components/StockRecommendationList.vue'
import StockAnalysisResult from '../components/StockAnalysisResult.vue'

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
const analysisResult = ref(null)
const isLoading = ref(false)
const error = ref(null)
const showESGAnalysis = ref(true)
const showRiskAnalysis = ref(true)
const currentPage = ref(1)
const itemsPerPage = 10
const isCollecting = ref(false)
const collectionStatus = ref(null)

const displayedRecommendations = computed(() => {
  if (!analysisResult.value?.analysis_result) return []
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  // 한글/영문 필드 모두 지원
  return analysisResult.value.analysis_result.slice(start, end).map(stock => ({
    name: stock.name || stock['종목명'],
    market: stock.market || stock['시장구분'] || stock['market'],
    currentPrice: stock.currentPrice || stock['현재가'],
    changeRate: stock.changeRate || stock['등락률'],
    volume: stock.volume || stock['거래량'],
    marketCap: stock.marketCap || stock['시가총액'],
    reason: stock.reason || stock['추천이유'] || stock['reason'],
  }))
})

const totalPages = computed(() => {
  if (!analysisResult.value?.analysis_result) return 1
  return Math.ceil(analysisResult.value.analysis_result.length / itemsPerPage)
})

const formatNumber = (value) => {
  if (typeof value !== 'number') return value
  return new Intl.NumberFormat('ko-KR').format(value)
}

// 새 채팅 시작: 모든 상태 초기화
const startNewChat = () => {
  selectedChat.value = null
  messages.value = []
  analysisResult.value = null
  userInput.value = ''
}

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

const getCriteriaName = (criteria) => {
  const criteriaNames = {
    market_cap: '시가총액',
    roe: 'ROE',
    profit_margin: '순이익률',
    market_growth: '시가총액 증가율',
    future_cash_flow: '미래 현금흐름',
    growth_potential: '성장성'
  }
  return criteriaNames[criteria] || criteria
}

// 시장 데이터 수집
const collectMarketData = async () => {
  isCollecting.value = true
  collectionStatus.value = null
  
  try {
    const response = await chatService.collectMarketData()
    collectionStatus.value = {
      success: true,
      message: `데이터 수집 완료 (${response.collected_count}건)`
    }
  } catch (e) {
    collectionStatus.value = {
      success: false,
      message: e.message || '데이터 수집 중 오류가 발생했습니다.'
    }
  } finally {
    isCollecting.value = false
  }
}

// 분석 재시도
const retryAnalysis = async () => {
  error.value = null
  await getStockRecommendations()
}

// 기존 sendMessage 함수 수정
const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  isLoading.value = true
  error.value = null
  
  try {
    // 사용자 메시지 추가
    messages.value.push({
      content: userInput.value,
      isUser: true
    })

    // 메시지 타입 결정
    let messageType = 'general_chat'
    const message = userInput.value.toLowerCase()
    
    if (message.includes('추천') || message.includes('유망')) {
      messageType = 'stock_recommendation'
    } else if (message.includes('분석')) {
      messageType = 'stock_analysis'
    }

    const response = await chatService.sendMessage(userInput.value, messageType)
    
    // AI 응답 추가
    messages.value.push({
      content: response.content || '응답을 받지 못했습니다.',
      isUser: false
    })
    
    // 분석 결과가 있는 경우 처리
    if (response.analysis_result) {
      let resultArr = response.analysis_result
      if (response.recommendations && Array.isArray(response.recommendations)) {
        resultArr = response.recommendations
      }
      analysisResult.value = {
        message_type: response.message_type || messageType,
        analysis_result: resultArr
      }
    }
    
    userInput.value = ''
    
  } catch (e) {
    console.error('Error in sendMessage:', e)
    // 개선: 백엔드 안내 메시지 우선 표시
    let msg = '분석 중 오류가 발생했습니다.'
    if (e.response && e.response.data && e.response.data.detail) {
      msg = e.response.data.detail
    } else if (e.message) {
      msg = e.message
    }
    error.value = msg
    // 에러 메시지도 채팅에 추가
    messages.value.push({
      content: `오류: ${msg}`,
      isUser: false,
      isError: true
    })
  } finally {
    isLoading.value = false
  }
}

const getStockAnalysis = async (stockCode) => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await chatService.getStockAnalysis(stockCode)
    analysisResult.value = {
      message_type: 'stock_analysis',
      analysis_result: response
    }
  } catch (e) {
    error.value = e.message || '종목 분석 중 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}

const getStockRecommendations = async (market = 'KOSPI') => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await chatService.getStockRecommendations({
      market_segment: market,
      include_esg: showESGAnalysis.value,
      include_risk_analysis: showRiskAnalysis.value
    })
    
    analysisResult.value = {
      message_type: 'stock_recommendation',
      analysis_result: response.recommendations
    }
  } catch (e) {
    error.value = e.message || '종목 추천을 가져오는데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

const backToRecommendations = () => {
  analysisResult.value = null
}

const loadChat = (chat) => {
  selectedChat.value = chat
  // 실제로는 chat.id로 백엔드에서 해당 채팅의 메시지 목록을 불러올 수도 있음
  messages.value = chat.messages || []
  // 분석 결과도 복원 (구조화 응답 파싱)
  let parsed = {}
  try {
    parsed = typeof chat.messages[1]?.content === 'string' ? JSON.parse(chat.messages[1].content) : chat.messages[1]?.content
  } catch (e) {
    parsed = { content_type: 'text', text: chat.messages[1]?.content }
  }
  analysisResult.value = parsed
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
    // 세션 복원: localStorage에 마지막 선택된 채팅 id가 있으면 해당 채팅 불러오기
    const lastChatId = localStorage.getItem('lastSelectedChatId')
    if (lastChatId && chatHistory.value.some(c => c.id == lastChatId)) {
      loadChat(chatHistory.value.find(c => c.id == lastChatId))
    } else if (chatHistory.value.length > 0) {
      loadChat(chatHistory.value[0])
    } else {
      // 히스토리가 없으면 초기화
      startNewChat()
    }
  } catch (error) {
    console.error('Failed to load chat history:', error)
    startNewChat()
  }
}

// 메뉴 이동/새로고침 시 세션 복원
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  await loadChatHistory()
})

// 채팅 선택 시 localStorage에 저장
watch(selectedChat, (val) => {
  if (val && val.id) {
    localStorage.setItem('lastSelectedChatId', val.id)
  } else {
    localStorage.removeItem('lastSelectedChatId')
  }
})
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

.toggle-history-btn {
  transition: left 0.3s cubic-bezier(0.4,0,0.2,1);
  z-index: 20;
}

/* 새로운 스타일 추가 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>