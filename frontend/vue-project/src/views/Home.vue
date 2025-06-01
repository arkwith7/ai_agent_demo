<template>
  <div class="min-h-screen bg-light">
    <main>
      <!-- Hero Section -->
      <section class="bg-gradient-to-r from-primary/5 to-primary/5 py-20">
        <div class="container mx-auto px-4">
          <div class="bg-white/85 inline-block p-10 rounded-lg max-w-3xl">
            <h2 class="text-4xl font-bold text-primary mb-6">워런 버핏의 투자 기준으로<br>최적의 종목을 찾아보세요</h2>
            <p class="text-xl text-secondary mb-8">AI가 워런 버핏의 6단계 투자 기준을 분석하여<br>가장 적합한 투자 종목을 추천해드립니다.</p>
            <router-link to="/analysis" class="btn-primary">
              투자 분석 시작하기 <i class="fas fa-arrow-right ml-2"></i>
            </router-link>
          </div>
        </div>
      </section>

      <!-- Investment Criteria Section -->
      <section class="py-16">
        <div class="container mx-auto px-4">
          <h2 class="section-title">워런 버핏의 6단계 투자 기준</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-building"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">1. 시가총액 기준</h3>
              <p class="text-secondary">전체 상장사 중 시가총액 상위 30% 이내에 포함되어야 함</p>
              <p class="text-sm text-primary mt-2">→ 충분한 규모와 시장 신뢰도를 갖춘 기업 선호</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-percentage"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">2. 자기자본이익률 (ROE)</h3>
              <p class="text-secondary">최근 3년간 ROE가 15% 이상</p>
              <p class="text-sm text-primary mt-2">→ 투입 자본 대비 수익성이 높아야 함</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-money-bill-wave"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">3. 순이익률과 잉여현금흐름</h3>
              <p class="text-secondary">매출액 대비 순이익률이 업종 평균 이상, 1주당 잉여현금흐름이 상위 30%</p>
              <p class="text-sm text-primary mt-2">→ 실질 이익과 배당 여력 중시</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-chart-line"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">4. 시가총액 vs 자본 증가율</h3>
              <p class="text-secondary">최근 3년간 시가총액 증가율 > 자본 증가율</p>
              <p class="text-sm text-primary mt-2">→ 이익보다 빠르게 시장 가치가 증가하는 기업 선호</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-coins"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">5. 5년 예상 잉여현금흐름</h3>
              <p class="text-secondary">향후 5년간 예상 잉여현금흐름의 합 > 현재 시가총액</p>
              <p class="text-sm text-primary mt-2">→ 장기적인 수익 창출력과 시장 저평가 여부 판단</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-gem"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">6. 성장성과 배당가능성</h3>
              <p class="text-secondary">전통적 PER, PBR보다 미래 현금흐름 대비 가치를 중시</p>
              <p class="text-sm text-primary mt-2">→ 가치투자자의 본질: "앞으로 벌 돈 대비 현재 주가가 싼가?"</p>
            </div>
          </div>
        </div>
      </section>

      <!-- AI Analysis Section -->
      <section class="bg-primary/5 py-16">
        <div class="container mx-auto px-4">
          <h2 class="section-title">AI 분석 프로세스</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-database"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">데이터 수집</h3>
              <p class="text-secondary">KRX, OpenDART 등에서 실시간 데이터를 수집하여 분석합니다.</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-brain"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">AI 분석</h3>
              <p class="text-secondary">워런 버핏의 6단계 투자 기준에 따라 AI가 종목을 분석합니다.</p>
            </div>

            <div class="feature-box">
              <div class="text-primary text-4xl mb-4">
                <i class="fas fa-chart-pie"></i>
              </div>
              <h3 class="text-xl font-bold mb-4">결과 제공</h3>
              <p class="text-secondary">분석 결과를 시각적으로 제공하고 투자 의사결정을 도와드립니다.</p>
            </div>
          </div>
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
</style> 