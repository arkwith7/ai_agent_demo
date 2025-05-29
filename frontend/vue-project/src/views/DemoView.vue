<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    <header class="bg-white border-bottom shadow-sm py-3 mb-4">
      <div class="container d-flex align-items-center">
        <div class="fw-bold fs-3 text-primary">
          <Icon icon="mdi:brain" class="me-2" />AI Agent 주식 분석
        </div>
        <!-- 데모 페이지는 상단 메뉴 없음 -->
      </div>
    </header>
    <main class="flex-grow-1 d-flex flex-column flex-md-row justify-content-center align-items-center">
      <aside class="bg-white border-end p-4 col-12 col-md-4 d-flex flex-column" style="max-width:400px;">
        <h2 class="h5 mb-3"><Icon icon="mdi:chat" class="me-2" />대화창</h2>
        <section class="flex-grow-1 mb-4 overflow-auto" style="min-height:200px;">
          <div v-for="(msg, idx) in chatHistory" :key="idx" :class="['mb-3', msg.sender === 'user' ? 'text-end' : 'text-start']">
            <span class="fw-bold small"><Icon :icon="msg.sender === 'user' ? 'mdi:account' : 'mdi:robot'" class="me-1"></Icon>{{ msg.sender === 'user' ? '사용자' : 'AI Agent' }}</span>
            <div :class="['rounded p-2 d-inline-block', msg.sender === 'user' ? 'bg-primary text-white' : 'bg-light border']" style="max-width:90%">{{ msg.text }}</div>
          </div>
        </section>
        <h2 class="h5 mb-3"><Icon icon="mdi:cog" class="me-2" />Agent 활동 로그</h2>
        <section class="mb-4 overflow-auto" style="height:140px;">
          <div v-for="(log, idx) in agentLog" :key="idx" class="d-flex align-items-center mb-2 small text-secondary">
            <span class="me-2"><Icon :icon="log.icon" :class="{ 'animate-spin': log.spin }"></Icon></span> {{ log.text }}
          </div>
        </section>
        <form @submit.prevent="onSubmit" class="mt-auto">
          <h3 class="h6 mb-2"><Icon icon="mdi:keyboard" class="me-2" />질문 입력</h3>
          <textarea v-model="userInput" class="form-control mb-2" placeholder="AI Agent에게 요청하세요..." rows="2"></textarea>
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary flex-grow-1"><Icon icon="mdi:send" class="me-1"></Icon>전송</button>
            <button type="button" class="btn btn-outline-secondary btn-sm" @click="suggestPrompt('워런 버핏 기준으로 회사 찾아줘')">워런 버핏 기준</button>
            <button type="button" class="btn btn-outline-secondary btn-sm" @click="suggestPrompt('성장주 찾아줘')">성장주 찾기</button>
          </div>
        </form>
      </aside>
      <section class="flex-grow-1 p-4 bg-light d-flex justify-content-center align-items-center">
        <component :is="rightPanelComponent" v-bind="rightPanelProps" />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'

// 상태
const chatHistory = ref([
  { text: '안녕하세요! AI 주식 분석 비서입니다. 무엇을 도와드릴까요? 예를 들어 \"워런 버핏 기준으로 회사 찾아줘\" 와 같이 질문해보세요.', sender: 'agent' }
])
const agentLog = ref([
  { text: 'AI Agent 준비 완료.', icon: 'mdi:check-circle', spin: false }
])
const userInput = ref('')
const rightPanelState = ref<'welcome'|'loading'|'buffett'|'growth'|'details'|'error'>('welcome')
const resultCompanies = ref<any[]>([])
const selectedCompany = ref<any>(null)
const router = useRouter()

// 우측 패널 컴포넌트 동적 렌더링
const rightPanelComponent = computed(() => {
  switch (rightPanelState.value) {
    case 'welcome': return WelcomePanel
    case 'loading': return LoadingPanel
    case 'buffett': return BuffettResultsPanel
    case 'growth': return GrowthResultsPanel
    case 'details': return CompanyDetailsPanel
    case 'error': return ErrorPanel
    default: return WelcomePanel
  }
})
const rightPanelProps = computed(() => {
  if (rightPanelState.value === 'details') return { company: selectedCompany.value, onBack: backToResults }
  return {}
})

// 패널 컴포넌트 정의
const WelcomePanel = {
  template: `<div class='results-placeholder'>
    <i class='fas fa-comments'></i>
    <h2 id='results-panel-label'>AI Agent와 대화를 시작하세요!</h2>
    <p>좌측 하단에 궁금한 점이나 분석하고 싶은 내용을 입력하시면, AI Agent가 분석 결과를 이곳에 표시해 드립니다.</p>
    <p>예시: \"워런 버핏 기준으로 회사 찾아줘\", \"A 기업 재무상태 알려줘\"</p>
  </div>`
}
const LoadingPanel = {
  template: `<div class='results-placeholder'>
    <i class='fas fa-hourglass-half fa-spin'></i>
    <h2 id='results-panel-label'>데이터 분석 중...</h2>
    <p>Agent가 요청을 처리하고 있습니다. 잠시만 기다려주세요.</p>
  </div>`
}
const ErrorPanel = {
  template: `<div class='results-placeholder'>
    <i class='fas fa-exclamation-triangle'></i>
    <h2 id='results-panel-label'>지원하지 않는 요청입니다.</h2>
    <p>\"워런 버핏\" 또는 \"성장주\"를 포함하여 질문해보세요.</p>
  </div>`
}
const BuffettResultsPanel = {
  emits: ['details'],
  setup(props, { emit }) {
    const companies = [
      {
        id: 'buffett_a',
        icon: 'fas fa-building-columns',
        name: '(주) 가나다전자',
        summary: 'ROE 22%, PBR 1.2, 시총 5조',
        match: '워런 버핏 기준: 5/6 충족',
        matchIcon: 'fas fa-check-circle',
        matchColor: 'green'
      },
      {
        id: 'buffett_b',
        icon: 'fas fa-microchip',
        name: '(주) 마이크로솔루션',
        summary: 'ROE 18%, PBR 0.9, 시총 8조',
        match: '워런 버핏 기준: 6/6 충족',
        matchIcon: 'fas fa-check-circle',
        matchColor: 'green'
      },
      {
        id: 'buffett_c',
        icon: 'fas fa-industry',
        name: '(주) 대한민국철강',
        summary: 'ROE 16%, PBR 1.0, 시총 3조',
        match: '워런 버핏 기준: 4/6 충족',
        matchIcon: 'fas fa-times-circle',
        matchColor: 'orange'
      }
    ]
    return { companies, emit }
  },
  template: `
    <div>
      <h2 id='results-panel-label'>분석 결과: 워런 버핏 기준 추천 종목</h2>
      <div class='results-container'>
        <article v-for='c in companies' :key='c.id' class='company-card'>
          <h3><i :class='c.icon'></i> {{ c.name }}</h3>
          <p><strong>주요 지표:</strong> {{ c.summary }}</p>
          <p class='criteria-match'><i :class='c.matchIcon' :style='{color: c.matchColor}'></i> {{ c.match }}</p>
          <button class='details-button' @click="$emit('details', c.id)"><i class='fas fa-eye'></i> 상세 보기</button>
        </article>
      </div>
    </div>
  `
}
const GrowthResultsPanel = {
  emits: ['details'],
  setup(props, { emit }) {
    const companies = [
      {
        id: 'growth_x',
        icon: 'fas fa-rocket',
        name: '(주) 넥스트테크',
        summary: '연매출성장률 35%, 영업이익률 15%',
        match: '높은 성장 잠재력 보유',
        matchIcon: 'fas fa-chart-line',
        matchColor: 'green'
      },
      {
        id: 'growth_y',
        icon: 'fas fa-biohazard',
        name: '(주) 바이오퓨처',
        summary: '신약 파이프라인 다수, 기술수출 기대',
        match: '혁신 기술 기반 성장 기대',
        matchIcon: 'fas fa-flask',
        matchColor: 'green'
      }
    ]
    return { companies, emit }
  },
  template: `
    <div>
      <h2 id='results-panel-label'>분석 결과: 추천 성장주</h2>
      <div class='results-container'>
        <article v-for='c in companies' :key='c.id' class='company-card'>
          <h3><i :class='c.icon'></i> {{ c.name }}</h3>
          <p><strong>주요 지표:</strong> {{ c.summary }}</p>
          <p class='criteria-match'><i :class='c.matchIcon' :style='{color: c.matchColor}'></i> {{ c.match }}</p>
          <button class='details-button' @click="$emit('details', c.id)"><i class='fas fa-eye'></i> 상세 보기</button>
        </article>
      </div>
    </div>
  `
}
const CompanyDetailsPanel = {
  props: ['company', 'onBack'],
  setup(props) {
    // 예시 데이터
    let companyName = '', roe = '', pbr = '', marketCap = '', fcfData = '', agentCommentText = ''
    if (props.company === 'buffett_b') {
      companyName = '(주) 마이크로솔루션'; roe = '18%'; pbr = '0.9'; marketCap = '8조';
      fcfData = `<table><thead><tr><th>연도</th><th>예상 FCF (억원)</th></tr></thead><tbody>
        <tr><td>2025</td><td>800</td></tr><tr><td>2026</td><td>850</td></tr>
        <tr><td>2027</td><td>920</td></tr><tr><td>2028</td><td>1000</td></tr>
        <tr><td>2029</td><td>1100</td></tr><tr><td><strong>합계</strong></td><td><strong>4670</strong></td></tr>
      </tbody></table>`;
      agentCommentText = '(주) 마이크로솔루션의 향후 5년 예상 FCF 총합은 4,670억원으로 현재 시가총액(8조원) 대비 양호한 수준입니다. 워런 버핏의 모든 기준을 충족하며, 특히 지속적인 ROE 성장과 안정적인 현금 흐름이 긍정적입니다.'
    } else if (props.company === 'buffett_a') {
      companyName = '(주) 가나다전자'; roe = '22%'; pbr = '1.2'; marketCap = '5조';
      fcfData = `<p>FCF 데이터 준비 중입니다.</p>`;
      agentCommentText = '(주) 가나다전자는 높은 ROE와 시장 신뢰도를 바탕으로 워런 버핏 기준 5가지를 충족합니다. 다만, 잉여현금흐름의 변동성이 다소 있어 장기적 안정성은 추가 검토가 필요합니다.'
    } else if (props.company === 'growth_x') {
      companyName = '(주) 넥스트테크'; roe = 'N/A (성장 초기)'; pbr = 'N/A'; marketCap = '1.5조';
      fcfData = `<div class='chart-placeholder'>성장 초기 기업 FCF 예측 모델 적용 예정</div>`;
      agentCommentText = '(주) 넥스트테크는 최근 3년간 연평균 매출 성장률 35%를 기록하며 빠르게 성장하고 있는 기술 기업입니다. 현재 수익성보다는 시장 점유율 확대에 집중하고 있으며, 향후 2-3년 내 흑자 전환이 기대됩니다.'
    } else {
      companyName = `(${props.company}) 상세 정보`; roe = '15%'; pbr = '1.0'; marketCap = 'N/A';
      fcfData = `<p>상세 FCF 데이터는 준비 중입니다.</p>`;
      agentCommentText = '해당 기업은 안정적인 재무 구조를 가지고 있습니다. 추가적인 분석이 필요합니다.'
    }
    return { companyName, roe, pbr, marketCap, fcfData, agentCommentText, props }
  },
  template: `
    <button class='back-to-results-button' @click='props.onBack'><i class='fas fa-arrow-left'></i> 결과 목록으로</button>
    <div class='company-details-view'>
      <h2><i class='fas fa-clipboard-list'></i> {{ companyName }} 상세 분석</h2>
      <section class='data-section'>
        <h4><i class='fas fa-info-circle'></i> 기본 정보</h4>
        <p><strong>회사명:</strong> {{ companyName }}</p>
        <p><strong>ROE:</strong> {{ roe }} / <strong>PBR:</strong> {{ pbr }} / <strong>시가총액:</strong> {{ marketCap }}</p>
      </section>
      <section class='data-section'>
        <h4><i class='fas fa-hand-holding-usd'></i> 5년 예상 FCF (Free Cash Flow)</h4>
        <div class='chart-placeholder'>미래 FCF 예측 차트 (시뮬레이션)</div>
        <div v-html='fcfData'></div>
      </section>
      <section class='data-section'>
        <h4><i class='fas fa-comment-dots'></i> Agent 분석 코멘트</h4>
        <p class='agent-comment'>{{ agentCommentText }}</p>
      </section>
    </div>
  `
}

// 입력/버튼 핸들러
function suggestPrompt(text: string) {
  userInput.value = text
  onSubmit()
}
function backToResults() {
  if (selectedCompany.value && selectedCompany.value.startsWith('buffett')) rightPanelState.value = 'buffett'
  else rightPanelState.value = 'growth'
}

async function onSubmit() {
  const query = userInput.value.trim()
  if (!query) return
  chatHistory.value.push({ text: query, sender: 'user' })
  userInput.value = ''
  agentLog.value.push({ text: '사용자 요청 분석 중...', icon: 'fas fa-brain', spin: true })
  rightPanelState.value = 'loading'
  await sleep(1200)
  agentLog.value[agentLog.value.length - 1].spin = false
  agentLog.value[agentLog.value.length - 1].text = `사용자 요청 분석 완료: "${query}"`

  if (query.includes('워런 버핏')) {
    await simulateBuffettFlow(query)
  } else if (query.includes('성장주')) {
    await simulateGrowthFlow(query)
  } else {
    await sleep(1000)
    chatHistory.value.push({ text: `"${query}"에 대한 분석은 현재 데모에서 지원하지 않거나, 좀 더 구체적인 질문이 필요합니다. "워런 버핏" 또는 "성장주"를 포함하여 질문해보세요.`, sender: 'agent' })
    rightPanelState.value = 'error'
  }
}

async function simulateBuffettFlow(query: string) {
  chatHistory.value.push({ text: '요청을 접수했습니다. 분석을 시작하겠습니다.', sender: 'agent' })
  rightPanelState.value = 'loading'
  await sleep(1000)
  agentLog.value.push({ text: '플랜 수립: 워런 버핏 6단계 필터링', icon: 'fas fa-list-check', spin: true })
  await sleep(1000)
  agentLog.value[agentLog.value.length - 1].spin = false
  agentLog.value[agentLog.value.length - 1].text = '플랜 수립 완료'
  const steps = [
    { text: '1단계: [KRX 데이터 조회] 시가총액 상위 30% 필터링 완료.', icon: 'fas fa-database', duration: 1200 },
    { text: '2단계: [재무정보 분석] ROE 15% 이상 필터링 완료.', icon: 'fas fa-chart-pie', duration: 1500 },
    { text: '3단계: [현금흐름 분석] 순이익률 및 FCF 확인 완료.', icon: 'fas fa-dollar-sign', duration: 1300 },
    { text: '4단계: [시장가치 분석] 시총 증가율 vs 자본 증가율 비교 완료.', icon: 'fas fa-chart-line', duration: 1000 },
    { text: '5단계: [미래가치 예측] 5년 FCF 예측 및 비교 완료.', icon: 'fas fa-project-diagram', duration: 1800 },
    { text: '6단계: [종합평가] 성장성 및 배당가능성 검토 완료.', icon: 'fas fa-clipboard-check', duration: 900 }
  ]
  for (const step of steps) {
    agentLog.value.push({ text: step.text, icon: step.icon, spin: true })
    await sleep(step.duration)
    agentLog.value[agentLog.value.length - 1].spin = false
  }
  agentLog.value.push({ text: '모든 분석 단계 완료. 결과 생성 중...', icon: 'fas fa-magic', spin: false })
  await sleep(1000)
  chatHistory.value.push({ text: '분석이 완료되었습니다. 워런 버핏 기준에 부합하는 추천 종목은 다음과 같습니다. 우측 화면에서 확인해주세요.', sender: 'agent' })
  rightPanelState.value = 'buffett'
}

async function simulateGrowthFlow(query: string) {
  chatHistory.value.push({ text: '요청을 접수했습니다. 분석을 시작하겠습니다.', sender: 'agent' })
  rightPanelState.value = 'loading'
  await sleep(1000)
  agentLog.value.push({ text: '플랜 수립: 성장주 필터링 (매출 성장률, 이익 성장률 등)', icon: 'fas fa-rocket', spin: true })
  await sleep(1000)
  agentLog.value[agentLog.value.length - 1].spin = false
  agentLog.value[agentLog.value.length - 1].text = '성장주 필터링 플랜 수립 완료'
  const steps = [
    { text: '1단계: [산업동향 분석] 유망 성장 산업군 식별 완료.', icon: 'fas fa-industry', duration: 1200 },
    { text: '2단계: [재무 데이터 스크리닝] 최근 3년 연평균 매출 성장률 20% 이상 완료.', icon: 'fas fa-file-invoice-dollar', duration: 1500 },
    { text: '3단계: [수익성 점검] 영업이익률 및 순이익률 증가 추세 확인 완료.', icon: 'fas fa-coins', duration: 1300 },
    { text: '4단계: [기술력/시장 점유율 평가] 완료.', icon: 'fas fa-microchip', duration: 1000 }
  ]
  for (const step of steps) {
    agentLog.value.push({ text: step.text, icon: step.icon, spin: true })
    await sleep(step.duration)
    agentLog.value[agentLog.value.length - 1].spin = false
  }
  agentLog.value.push({ text: '성장주 분석 완료. 결과 생성 중...', icon: 'fas fa-lightbulb', spin: false })
  await sleep(1000)
  chatHistory.value.push({ text: '성장 가능성이 높은 기업들을 분석했습니다. 우측 화면에서 추천 종목을 확인하세요.', sender: 'agent' })
  rightPanelState.value = 'growth'
}

function sleep(ms: number) { return new Promise(resolve => setTimeout(resolve, ms)) }

// 상세 보기 버튼 핸들러
function handleDetails(id: string) {
  selectedCompany.value = id
  rightPanelState.value = 'details'
}

// 패널 컴포넌트의 이벤트 연결
// (BuffettResultsPanel, GrowthResultsPanel에서 details 이벤트 발생 시)
BuffettResultsPanel.emits = ['details']
GrowthResultsPanel.emits = ['details']

// Vue 3에서는 defineExpose로 하위 emits 연결 필요 없음

const logIcons = {
  'mdi:building-columns': 'mdi:building-columns',
  'mdi:check-circle': 'mdi:check-circle',
  'mdi:microchip': 'mdi:microchip',
  'mdi:industry': 'mdi:industry',
  'mdi:times-circle': 'mdi:times-circle',
  'mdi:rocket': 'mdi:rocket',
  'mdi:chart-line': 'mdi:chart-line',
  'mdi:biohazard': 'mdi:biohazard',
  'mdi:flask': 'mdi:flask',
  'mdi:brain': 'mdi:brain',
  'mdi:list-check': 'mdi:list-check',
  'mdi:database': 'mdi:database',
  'mdi:chart-pie': 'mdi:chart-pie',
  'mdi:currency-usd': 'mdi:currency-usd',
  'mdi:project-diagram': 'mdi:project-diagram',
  'mdi:clipboard-check': 'mdi:clipboard-check',
  'mdi:magic': 'mdi:magic',
  'mdi:file-invoice-dollar': 'mdi:file-invoice-dollar',
  'mdi:coins': 'mdi:coins'
}
</script>

<!-- Bootstrap 스타일 사용, 기존 style 태그 제거 -->

<style scoped>
/* start_demo_dynamic.html의 스타일을 그대로 이식 (scoped) */
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --light-bg: #f8f9fa;
  --dark-bg: #343a40;
  --border-color: #dee2e6;
  --text-color: #212529;
  --text-light: #f8f9fa;
  --user-msg-bg: #007bff;
  --agent-msg-bg: #e9ecef;
  --action-log-bg: #f9f9f9;
  --card-bg: #ffffff;
  --hover-darken-primary: #0056b3;
  --hover-lighten-secondary: #5a6268;
}
.demo-root {
  width: 100vw;
  min-height: 100vh;
  background: var(--light-bg);
  display: flex;
  flex-direction: column;
}
.demo-header {
  background: var(--card-bg);
  color: var(--text-color);
  padding: 0 25px;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 65px;
  box-sizing: border-box;
  flex-shrink: 0;
}
.demo-header h1 {
  margin: 0;
  font-size: 1.6em;
  color: var(--primary-color);
}
.demo-header h1 .fa-brain { margin-right: 10px; }
.demo-header .home-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.95em;
  padding: 8px 12px;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}
.demo-header .home-link:hover {
  background-color: var(--agent-msg-bg);
  text-decoration: none;
}
.demo-main-container {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}
.left-panel {
  width: 400px;
  background-color: var(--card-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
}
.right-panel {
  flex-grow: 1;
  background-color: var(--light-bg);
  padding: 25px;
  overflow-y: auto;
  box-sizing: border-box;
}
.right-panel > h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 12px;
  font-size: 1.8em;
}
.chat-history-pane, .agent-action-log-pane {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 15px;
  overflow-y: auto;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.chat-history-pane { flex-grow: 1; min-height: 250px; }
.agent-action-log-pane { height: 180px; font-size: 0.88em; color: var(--secondary-color); background-color: var(--action-log-bg); }
.panel-title { margin-top: 0; margin-bottom: 12px; font-size: 1.1em; color: var(--text-color); font-weight: 600; }
.panel-title .fa-comments, .panel-title .fa-cogs { margin-right: 8px; color: var(--primary-color); }
.message {
  margin-bottom: 12px;
  padding: 10px 15px;
  border-radius: 18px;
  max-width: 90%;
  word-wrap: break-word;
  display: flex;
  flex-direction: column;
  opacity: 1;
  transform: none;
}
.user-message {
  background-color: var(--user-msg-bg);
  color: var(--text-light);
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 6px;
}
.agent-message {
  background-color: var(--agent-msg-bg);
  color: var(--text-color);
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 6px;
}
.message .sender {
  font-weight: bold;
  font-size: 0.85em;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
}
.message .sender .fa-user, .message .sender .fa-robot { margin-right: 6px; font-size: 0.9em; }
.message .text { font-size: 0.95em; line-height: 1.5; }
.log-item { padding: 6px 2px; border-bottom: 1px dotted #e0e0e0; display: flex; align-items: center; opacity: 1; transform: none; }
.log-item:last-child { border-bottom: none; }
.log-item .icon { margin-right: 8px; color: var(--secondary-color); width: 20px; text-align: center; }
.log-item .fa-spinner { color: var(--primary-color); }
.chat-input-form { margin-top: auto; padding-top: 15px; border-top: 1px solid var(--border-color); }
.chat-input-form .panel-title { margin-bottom: 10px; }
.chat-input-form textarea {
  width: calc(100% - 24px);
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  resize: none;
  min-height: 45px;
  box-sizing: border-box;
  margin-bottom: 12px;
  font-size: 1em;
  line-height: 1.4;
  transition: border-color 0.2s ease;
}
.chat-input-form textarea:focus { border-color: var(--primary-color); outline: none; box-shadow: 0 0 0 2px rgba(0,123,255,0.25); }
.chat-input-form .button-group { display: flex; gap: 8px; }
.chat-input-form button {
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95em;
  font-weight: 500;
  transition: background-color 0.2s ease, transform 0.1s ease;
}
.chat-input-form button:active { transform: scale(0.98); }
.chat-input-form button.send-button { background-color: var(--primary-color); color: white; flex-grow: 1; }
.chat-input-form button.send-button:hover { background-color: var(--hover-darken-primary); }
.chat-input-form button.send-button .fa-paper-plane { margin-right: 6px; }
.chat-input-form .suggested-prompt-button { background-color: var(--agent-msg-bg); color: var(--text-color); font-size: 0.85em; padding: 10px 12px; }
.chat-input-form .suggested-prompt-button:hover { background-color: #d3d9df; }
.results-placeholder { text-align: center; padding: 60px 30px; color: var(--secondary-color); font-size: 1.15em; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; box-sizing: border-box; }
.results-placeholder .fa-comments, .results-placeholder .fa-hourglass-half { font-size: 3em; margin-bottom: 20px; color: var(--primary-color); }
.results-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.company-card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); transition: transform 0.2s ease, box-shadow 0.2s ease; }
.company-card:hover { transform: translateY(-5px); box-shadow: 0 4px 10px rgba(0,0,0,0.12); }
.company-card h3 { margin-top: 0; margin-bottom: 12px; color: var(--primary-color); font-size: 1.3em; }
.company-card p { font-size: 0.95em; margin-bottom: 8px; line-height: 1.5; }
.company-card .criteria-match { font-size: 0.85em; color: var(--secondary-color); margin-bottom: 15px; }
.company-card .details-button { background-color: #28a745; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; text-align: center; display: block; width: 100%; margin-top: 15px; font-weight: 500; transition: background-color 0.2s ease; }
.company-card .details-button:hover { background-color: #1e7e34; }
.company-card .details-button .fa-eye { margin-right: 6px; }
.company-details-view { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); }
.company-details-view h2 { margin-top: 0; margin-bottom: 20px; color: var(--primary-color); font-size: 1.6em; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
.company-details-view .data-section { margin-bottom: 25px; }
.company-details-view .data-section h4 { margin-bottom: 10px; font-size: 1.15em; color: var(--text-color); }
.company-details-view .chart-placeholder { width: 100%; height: 250px; background-color: var(--agent-msg-bg); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; color: var(--secondary-color); border-radius: 6px; margin-bottom: 15px; font-style: italic; }
.company-details-view table { width: 100%; border-collapse: collapse; font-size: 0.95em; }
.company-details-view th, .company-details-view td { border: 1px solid var(--border-color); padding: 10px 12px; text-align: left; }
.company-details-view th { background-color: var(--light-bg); font-weight: 600; }
.company-details-view .agent-comment { background-color: #e7f3fe; border-left: 5px solid var(--primary-color); padding: 15px; font-size: 1em; line-height: 1.6; border-radius: 0 6px 6px 0; }
.back-to-results-button { background-color: var(--secondary-color); color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: 500; transition: background-color 0.2s ease; margin-bottom: 20px; }
.back-to-results-button:hover { background-color: var(--hover-lighten-secondary); }
.back-to-results-button .fa-arrow-left { margin-right: 6px; }
.visually-hidden { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0, 0, 0, 0); border: 0; }
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