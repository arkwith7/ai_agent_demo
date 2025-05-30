<template>
  <div class="min-h-screen bg-light">
    <!-- 상단 네비게이션 -->
    <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
      <div class="container mx-auto px-4 py-2 flex justify-between items-center">
        <h1 class="text-xl font-bold text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 inline-block mr-2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
          </svg>
          AI 투자 분석
        </h1>
        <router-link to="/" class="text-primary hover:text-primary/80 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
          </svg>
        </router-link>
      </div>
    </header>

    <main class="container mx-auto px-4 pt-16 pb-8">
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

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <!-- 채팅 히스토리 -->
        <div 
          class="lg:col-span-2 transition-all duration-300 relative"
          :class="{ 
            'hidden': !showMobileHistory && !isLargeScreen,
            'lg:col-span-0': isHistoryCollapsed && isLargeScreen
          }"
        >
          <div class="bg-white rounded-lg shadow-sm p-4 h-[calc(100vh-8rem)] overflow-y-auto">
            <!-- 데스크톱 화면에서의 접기/펼치기 버튼 -->
            <button 
              v-if="isLargeScreen"
              @click="toggleHistory"
              class="absolute -right-3 top-4 bg-white rounded-full shadow-md p-1 hover:bg-primary/5 transition-colors z-10"
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

            <div :class="{ 'hidden': isHistoryCollapsed && isLargeScreen }">
              <h2 class="text-lg font-bold text-primary mb-4">채팅 히스토리</h2>
              <div class="space-y-2">
                <button 
                  v-for="(chat, index) in chatHistory" 
                  :key="index"
                  @click="loadChat(chat)"
                  class="w-full text-left p-2 rounded hover:bg-primary/5 transition-colors"
                  :class="{ 'bg-primary/10': selectedChat === chat }"
                >
                  <p class="text-sm font-medium truncate">{{ chat.title }}</p>
                  <p class="text-xs text-secondary">{{ chat.date }}</p>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 채팅 섹션 -->
        <div 
          class="lg:col-span-5 transition-all duration-300" 
          :class="{ 
            'lg:col-span-6': isHistoryCollapsed && isLargeScreen,
            'lg:ml-0': !isHistoryCollapsed || !isLargeScreen,
            'lg:ml-8': isHistoryCollapsed && isLargeScreen
          }"
        >
          <div class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-8rem)] flex flex-col">
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
          <div class="bg-white rounded-lg shadow-sm p-6 h-[calc(100vh-8rem)] overflow-y-auto">
            <!-- 추천 종목 목록 -->
            <div v-if="showRecommendations" class="mb-8">
              <h2 class="text-xl font-bold text-primary mb-6">추천 종목 목록</h2>
              <div class="overflow-x-auto">
                <table class="min-w-full">
                  <thead>
                    <tr class="bg-primary/5">
                      <th class="px-4 py-2 text-left text-xs font-medium text-secondary">종목명</th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-secondary">현재가</th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-secondary">등락률</th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-secondary">추천사유</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="stock in recommendedStocks" :key="stock.code" 
                        class="border-b border-gray-200 hover:bg-primary/5 cursor-pointer"
                        @click="analyzeStock(stock)">
                      <td class="px-4 py-3">{{ stock.name }}</td>
                      <td class="px-4 py-3">{{ stock.price }}</td>
                      <td class="px-4 py-3" :class="stock.change >= 0 ? 'text-red-600' : 'text-blue-600'">
                        {{ stock.change >= 0 ? '+' : '' }}{{ stock.change }}%
                      </td>
                      <td class="px-4 py-3">
                        <button @click.stop="showRecommendationReason(stock)" 
                                class="text-primary hover:text-primary/80">
                          추천사유 보기
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 종목 분석 결과 -->
            <div v-if="showAnalysis">
              <h2 class="text-xl font-bold text-primary mb-6">분석 결과</h2>
              
              <!-- 종목 정보 -->
              <div class="mb-8">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold">{{ selectedStock.name }} ({{ selectedStock.code }})</h3>
                  <span :class="selectedStock.change >= 0 ? 'text-red-600' : 'text-blue-600'">
                    {{ selectedStock.change >= 0 ? '+' : '' }}{{ selectedStock.change }}%
                  </span>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-primary/5 rounded-lg p-3">
                    <p class="text-sm text-secondary">시가총액</p>
                    <p class="text-lg font-bold">{{ selectedStock.marketCap }}</p>
                  </div>
                  <div class="bg-primary/5 rounded-lg p-3">
                    <p class="text-sm text-secondary">ROE</p>
                    <p class="text-lg font-bold">{{ selectedStock.roe }}%</p>
                  </div>
                  <div class="bg-primary/5 rounded-lg p-3">
                    <p class="text-sm text-secondary">순이익률</p>
                    <p class="text-lg font-bold">{{ selectedStock.profitMargin }}%</p>
                  </div>
                  <div class="bg-primary/5 rounded-lg p-3">
                    <p class="text-sm text-secondary">배당률</p>
                    <p class="text-lg font-bold">{{ selectedStock.dividendYield }}%</p>
                  </div>
                </div>
              </div>

              <!-- 투자 기준 충족 여부 -->
              <div class="mb-8">
                <h3 class="text-lg font-bold mb-4">투자 기준 충족 여부</h3>
                <div class="space-y-3">
                  <div v-for="(criterion, index) in investmentCriteria" :key="index"
                       class="flex items-center justify-between">
                    <span class="text-secondary">{{ criterion.name }}</span>
                    <span :class="criterion.status === 'pass' ? 'text-green-600' : 
                                 criterion.status === 'warning' ? 'text-yellow-600' : 'text-red-600'">
                      {{ criterion.status === 'pass' ? '✓' : 
                         criterion.status === 'warning' ? '△' : '✗' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 투자 의견 -->
              <div>
                <h3 class="text-lg font-bold mb-4">투자 의견</h3>
                <div class="bg-primary/5 rounded-lg p-4">
                  <p class="text-secondary mb-4">{{ selectedStock.analysis.summary }}</p>
                  <p class="text-secondary">{{ selectedStock.analysis.detail }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 추천사유 모달 -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-primary">{{ selectedStock.name }} 추천사유</h3>
          <button @click="showModal = false" class="text-secondary hover:text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div v-for="(reason, index) in selectedStock.recommendationReasons" :key="index"
               class="bg-primary/5 rounded-lg p-4">
            <h4 class="font-bold mb-2">{{ reason.title }}</h4>
            <p class="text-secondary">{{ reason.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'

const userInput = ref('')
const chatContainer = ref(null)
const showModal = ref(false)
const showRecommendations = ref(false)
const showAnalysis = ref(false)
const selectedStock = ref(null)
const selectedChat = ref(null)
const currentChatId = ref(4)
const showMobileHistory = ref(false)
const isLargeScreen = ref(window.innerWidth >= 1024)
const isHistoryCollapsed = ref(false)

// 화면 크기 변경 감지
const handleResize = () => {
  isLargeScreen.value = window.innerWidth >= 1024
  if (isLargeScreen.value) {
    showMobileHistory.value = false
  }
}

// 히스토리 토글
const toggleHistory = () => {
  isHistoryCollapsed.value = !isHistoryCollapsed.value
  // 히스토리가 접힐 때 채팅창에 여백 추가
  if (isHistoryCollapsed.value) {
    nextTick(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  createNewChat()
  scrollToBottom()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

// 가상 데이터: 채팅 히스토리
const chatHistory = ref([
  {
    id: 1,
    title: '삼성전자 분석 요청',
    date: '2024-03-20 14:30',
    messages: [
      {
        content: '안녕하세요! 저는 AI 투자 분석가입니다. 워런 버핏의 투자 철학을 바탕으로 최적의 투자 기회를 찾아드리겠습니다. 어떤 종목에 대해 분석해드릴까요?',
        isUser: false
      },
      {
        content: '삼성전자에 대해 분석해주세요.',
        isUser: true
      },
      {
        content: '삼성전자에 대한 분석을 시작하겠습니다. 워런 버핏의 6단계 투자 기준에 따라 분석하고 있습니다...',
        isUser: false
      }
    ],
    analysis: {
      stock: {
        code: '005930',
        name: '삼성전자',
        price: '74,800원',
        change: 2.5,
        marketCap: '423조원',
        roe: 18.5,
        profitMargin: 12.3,
        dividendYield: 2.8
      },
      criteria: [
        { name: '시가총액 상위 30%', status: 'pass' },
        { name: 'ROE 15% 이상', status: 'pass' },
        { name: '순이익률 업종 평균 이상', status: 'pass' },
        { name: '시가총액 증가율 > 자본 증가율', status: 'pass' },
        { name: '5년 예상 FCF > 시가총액', status: 'warning' },
        { name: '배당 가능성', status: 'pass' }
      ],
      analysis: {
        summary: '워런 버핏의 투자 기준을 5/6 충족하는 우수한 기업입니다. 특히 시가총액, ROE, 순이익률, 배당 가능성에서 매우 우수한 평가를 받았습니다.',
        detail: '다만, 5년 예상 잉여현금흐름이 현재 시가총액을 상회하지 않는 점은 주의가 필요합니다. 반도체 시장의 불확실성을 고려할 때, 장기적인 관점에서의 모니터링이 필요합니다.'
      }
    }
  },
  {
    id: 2,
    title: 'SK하이닉스 분석 요청',
    date: '2024-03-20 13:15',
    messages: [
      {
        content: '안녕하세요! 저는 AI 투자 분석가입니다. 워런 버핏의 투자 철학을 바탕으로 최적의 투자 기회를 찾아드리겠습니다. 어떤 종목에 대해 분석해드릴까요?',
        isUser: false
      },
      {
        content: 'SK하이닉스에 대해 분석해주세요.',
        isUser: true
      },
      {
        content: 'SK하이닉스에 대한 분석을 시작하겠습니다. 워런 버핏의 6단계 투자 기준에 따라 분석하고 있습니다...',
        isUser: false
      }
    ],
    analysis: {
      stock: {
        code: '000660',
        name: 'SK하이닉스',
        price: '156,000원',
        change: -1.2,
        marketCap: '112조원',
        roe: 22.3,
        profitMargin: 15.8,
        dividendYield: 1.2
      },
      criteria: [
        { name: '시가총액 상위 30%', status: 'pass' },
        { name: 'ROE 15% 이상', status: 'pass' },
        { name: '순이익률 업종 평균 이상', status: 'pass' },
        { name: '시가총액 증가율 > 자본 증가율', status: 'warning' },
        { name: '5년 예상 FCF > 시가총액', status: 'fail' },
        { name: '배당 가능성', status: 'warning' }
      ],
      analysis: {
        summary: '워런 버핏의 투자 기준을 3/6 충족하는 기업입니다. 높은 ROE와 순이익률이 장점이나, 시장 불확실성으로 인한 위험이 있습니다.',
        detail: '반도체 시장의 사이클성을 고려할 때, 현재의 높은 수익성은 지속될 수 있을지 주의 깊게 모니터링이 필요합니다.'
      }
    }
  },
  {
    id: 3,
    title: '추천 종목 요청',
    date: '2024-03-20 11:45',
    messages: [
      {
        content: '안녕하세요! 저는 AI 투자 분석가입니다. 워런 버핏의 투자 철학을 바탕으로 최적의 투자 기회를 찾아드리겠습니다. 어떤 종목에 대해 분석해드릴까요?',
        isUser: false
      },
      {
        content: '현재 추천할 만한 종목이 있을까요?',
        isUser: true
      },
      {
        content: '현재 시장 상황에서 추천할 만한 종목들을 분석해보았습니다. 아래 목록에서 관심 있는 종목을 선택하시면 상세 분석 결과를 확인하실 수 있습니다.',
        isUser: false
      }
    ],
    recommendations: [
      {
        code: '005930',
        name: '삼성전자',
        price: '74,800원',
        change: 2.5,
        recommendationReasons: [
          {
            title: '시가총액 상위 30%',
            description: '시가총액 423조원으로 한국 시장 상위 1위 기업입니다.'
          },
          {
            title: 'ROE 15% 이상',
            description: '최근 3년간 평균 ROE 18.5%로 워런 버핏의 기준을 충족합니다.'
          }
        ]
      },
      {
        code: '000660',
        name: 'SK하이닉스',
        price: '156,000원',
        change: -1.2,
        recommendationReasons: [
          {
            title: '높은 ROE',
            description: '최근 3년간 평균 ROE 22.3%로 매우 우수한 수익성을 보여줍니다.'
          }
        ]
      },
      {
        code: '035720',
        name: '카카오',
        price: '45,200원',
        change: 1.5,
        recommendationReasons: [
          {
            title: '높은 성장성',
            description: '플랫폼 사업의 지속적인 성장과 수익성 개선이 기대됩니다.'
          }
        ]
      },
      {
        code: '035420',
        name: 'NAVER',
        price: '198,000원',
        change: 0.8,
        recommendationReasons: [
          {
            title: '안정적인 수익성',
            description: '검색, 커머스 등 핵심 사업의 안정적인 수익 창출이 지속됩니다.'
          }
        ]
      },
      {
        code: '051910',
        name: 'LG화학',
        price: '425,000원',
        change: -0.5,
        recommendationReasons: [
          {
            title: '배터리 사업 성장',
            description: '전기차 배터리 사업의 급성장으로 수익성이 개선될 것으로 예상됩니다.'
          }
        ]
      }
    ]
  }
])

// 현재 채팅 메시지
const messages = ref([])

// 추천 종목 목록
const recommendedStocks = ref([
  {
    code: '005930',
    name: '삼성전자',
    price: '74,800원',
    change: 2.5,
    recommendationReasons: [
      {
        title: '시가총액 상위 30%',
        description: '시가총액 423조원으로 한국 시장 상위 1위 기업입니다.'
      },
      {
        title: 'ROE 15% 이상',
        description: '최근 3년간 평균 ROE 18.5%로 워런 버핏의 기준을 충족합니다.'
      }
    ]
  },
  {
    code: '000660',
    name: 'SK하이닉스',
    price: '156,000원',
    change: -1.2,
    recommendationReasons: [
      {
        title: '높은 ROE',
        description: '최근 3년간 평균 ROE 22.3%로 매우 우수한 수익성을 보여줍니다.'
      }
    ]
  }
])

// 투자 기준
const investmentCriteria = ref([
  { name: '시가총액 상위 30%', status: 'pass' },
  { name: 'ROE 15% 이상', status: 'pass' },
  { name: '순이익률 업종 평균 이상', status: 'pass' },
  { name: '시가총액 증가율 > 자본 증가율', status: 'pass' },
  { name: '5년 예상 FCF > 시가총액', status: 'warning' },
  { name: '배당 가능성', status: 'pass' }
])

// 새로운 채팅 생성
const createNewChat = () => {
  const newChat = {
    id: currentChatId.value++,
    title: '새로운 대화',
    date: new Date().toLocaleString('ko-KR'),
    messages: [{
      content: '안녕하세요! 저는 AI 투자 분석가입니다. 워런 버핏의 투자 철학을 바탕으로 최적의 투자 기회를 찾아드리겠습니다. 어떤 종목에 대해 분석해드릴까요?',
      isUser: false
    }]
  }
  
  chatHistory.value.unshift(newChat)
  selectedChat.value = newChat
  messages.value = [...newChat.messages]
  showRecommendations.value = false
  showAnalysis.value = false
}

// 메시지 전송
const sendMessage = async () => {
  if (!userInput.value.trim()) return

  // 사용자 메시지 추가
  const userMessage = {
    content: userInput.value,
    isUser: true
  }
  messages.value.push(userMessage)

  // 채팅 히스토리 업데이트
  if (selectedChat.value) {
    selectedChat.value.messages.push(userMessage)
    selectedChat.value.title = userInput.value.length > 20 
      ? userInput.value.substring(0, 20) + '...' 
      : userInput.value
  }

  // AI 응답 처리
  let aiResponse = {
    content: '',
    isUser: false
  }

  if (userInput.value.includes('추천') || userInput.value.includes('종목')) {
    showRecommendations.value = true
    showAnalysis.value = false
    aiResponse.content = '현재 시장 상황에서 추천할 만한 종목들을 분석해보았습니다. 아래 목록에서 관심 있는 종목을 선택하시면 상세 분석 결과를 확인하실 수 있습니다.'
    
    // 추천 종목 데이터 추가
    selectedChat.value.recommendations = [
      {
        code: '005930',
        name: '삼성전자',
        price: '74,800원',
        change: 2.5,
        recommendationReasons: [
          {
            title: '시가총액 상위 30%',
            description: '시가총액 423조원으로 한국 시장 상위 1위 기업입니다.'
          },
          {
            title: 'ROE 15% 이상',
            description: '최근 3년간 평균 ROE 18.5%로 워런 버핏의 기준을 충족합니다.'
          }
        ]
      },
      // ... 다른 추천 종목들 ...
    ]
  } else if (userInput.value.includes('삼성전자')) {
    showRecommendations.value = false
    showAnalysis.value = true
    aiResponse.content = '삼성전자에 대한 분석을 시작하겠습니다. 워런 버핏의 6단계 투자 기준에 따라 분석하고 있습니다...'
    
    // 분석 결과 데이터 추가
    selectedChat.value.analysis = {
      stock: {
        code: '005930',
        name: '삼성전자',
        price: '74,800원',
        change: 2.5,
        marketCap: '423조원',
        roe: 18.5,
        profitMargin: 12.3,
        dividendYield: 2.8
      },
      criteria: [
        { name: '시가총액 상위 30%', status: 'pass' },
        { name: 'ROE 15% 이상', status: 'pass' },
        { name: '순이익률 업종 평균 이상', status: 'pass' },
        { name: '시가총액 증가율 > 자본 증가율', status: 'pass' },
        { name: '5년 예상 FCF > 시가총액', status: 'warning' },
        { name: '배당 가능성', status: 'pass' }
      ],
      analysis: {
        summary: '워런 버핏의 투자 기준을 5/6 충족하는 우수한 기업입니다. 특히 시가총액, ROE, 순이익률, 배당 가능성에서 매우 우수한 평가를 받았습니다.',
        detail: '다만, 5년 예상 잉여현금흐름이 현재 시가총액을 상회하지 않는 점은 주의가 필요합니다. 반도체 시장의 불확실성을 고려할 때, 장기적인 관점에서의 모니터링이 필요합니다.'
      }
    }
    selectedStock.value = selectedChat.value.analysis.stock
  } else {
    showRecommendations.value = false
    showAnalysis.value = false
    aiResponse.content = '죄송합니다. 요청하신 내용을 이해하지 못했습니다. 종목 분석이나 추천 종목 목록을 요청해주세요.'
  }

  // AI 응답 추가
  messages.value.push(aiResponse)
  if (selectedChat.value) {
    selectedChat.value.messages.push(aiResponse)
  }

  userInput.value = ''
  await nextTick()
  scrollToBottom()
}

// 채팅 스크롤
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 종목 분석
const analyzeStock = (stock) => {
  selectedStock.value = stock
  showRecommendations.value = false
  showAnalysis.value = true
}

// 추천사유 모달
const showRecommendationReason = (stock) => {
  selectedStock.value = stock
  showModal.value = true
}

// 채팅 히스토리 로드
const loadChat = (chat) => {
  selectedChat.value = chat
  messages.value = [...chat.messages]
  
  if (chat.recommendations) {
    showRecommendations.value = true
    showAnalysis.value = false
  } else if (chat.analysis) {
    showRecommendations.value = false
    showAnalysis.value = true
    selectedStock.value = chat.analysis.stock
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

/* 히스토리 토글 버튼 스타일 */
.absolute.-right-3 {
  right: -0.75rem;
}

/* 히스토리가 접혔을 때의 여백 조정 */
.lg\:ml-8 {
  margin-left: 2rem;
}
</style> 