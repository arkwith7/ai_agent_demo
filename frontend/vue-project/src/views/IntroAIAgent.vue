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
          <span class="text-primary font-medium">AI Agent 소개</span>
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
      <!-- Hero Section -->
      <section class="bg-gradient-to-r from-primary/5 to-primary/5 py-12">
        <div class="container mx-auto px-4 text-center">
          <h2 class="text-3xl font-bold text-primary mb-4">
            AI Agent와 함께하는<br>
            스마트한 투자 분석
          </h2>
          <p class="text-xl text-secondary">
            AI Agent가 워런 버핏의 투자 철학을 바탕으로<br>
            최적의 투자 기회를 찾아드립니다.
          </p>
        </div>
      </section>

      <!-- AI Agent Features Section -->
      <section class="py-16">
        <div class="container mx-auto px-4">
          <h2 class="section-title">AI Agent의 주요 특징</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold mb-4">자연어 기반 대화</h3>
              <p class="text-secondary">복잡한 설정 없이 자연스러운 대화로 투자 분석을 요청하고 결과를 받아볼 수 있습니다.</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
                </svg>
              </div>
              <h3 class="text-xl font-bold mb-4">투명한 분석 과정</h3>
              <p class="text-secondary">AI Agent가 어떤 데이터를 조회하고, 어떤 기준으로 종목을 필터링하는지 실시간으로 확인할 수 있습니다.</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold mb-4">대화형 인사이트</h3>
              <p class="text-secondary">분석 결과에 대해 궁금한 점을 추가로 질문하고, AI Agent와 대화하며 더 깊이 있는 인사이트를 얻을 수 있습니다.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works Section -->
      <section class="bg-primary/5 py-16">
        <div class="container mx-auto px-4">
          <h2 class="section-title">AI Agent 작동 방식</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
            <div class="feature-box">
              <h3 class="text-xl font-bold mb-4">1. 데이터 수집 및 분석</h3>
              <ul class="list-disc list-inside text-secondary space-y-2">
                <li>KRX, OpenDART 등에서 실시간 데이터 수집</li>
                <li>워런 버핏의 6단계 투자 기준 적용</li>
                <li>기업 재무제표 및 시장 데이터 분석</li>
              </ul>
            </div>

            <div class="feature-box">
              <h3 class="text-xl font-bold mb-4">2. AI 기반 종목 선정</h3>
              <ul class="list-disc list-inside text-secondary space-y-2">
                <li>시가총액 상위 30% 기업 필터링</li>
                <li>ROE 15% 이상 기업 선별</li>
                <li>순이익률 및 잉여현금흐름 분석</li>
              </ul>
            </div>

            <div class="feature-box">
              <h3 class="text-xl font-bold mb-4">3. 성장성 및 가치 평가</h3>
              <ul class="list-disc list-inside text-secondary space-y-2">
                <li>시가총액 vs 자본 증가율 비교</li>
                <li>5년 예상 잉여현금흐름 분석</li>
                <li>배당 가능성 및 성장 잠재력 평가</li>
              </ul>
            </div>

            <div class="feature-box">
              <h3 class="text-xl font-bold mb-4">4. 결과 제공 및 설명</h3>
              <ul class="list-disc list-inside text-secondary space-y-2">
                <li>선정된 종목의 상세 분석 결과 제공</li>
                <li>투자 결정에 필요한 핵심 지표 설명</li>
                <li>추가 질문에 대한 실시간 답변</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="py-16">
        <div class="container mx-auto px-4 text-center">
          <h2 class="text-3xl font-bold text-primary mb-6">AI Agent와 함께 시작하세요</h2>
          <p class="text-xl text-secondary mb-8">워런 버핏의 투자 철학을 바탕으로 한 AI 분석으로<br>최적의 투자 기회를 찾아보세요.</p>
          <router-link to="/analysis" class="btn-primary">
            투자 분석 시작하기
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 ml-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </section>
    </main>

    <footer class="bg-white border-t border-gray-200 py-8">
      <div class="container mx-auto px-4 text-center text-secondary">
        <p>&copy; 2024 AI 투자 분석. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// 컴포넌트 로직은 추후 구현
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

.section-title {
  @apply text-3xl font-bold text-primary mb-8 text-center;
}
.feature-box {
  @apply bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow;
}
.btn-primary {
  @apply bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90 transition-colors inline-flex items-center;
}
</style> 