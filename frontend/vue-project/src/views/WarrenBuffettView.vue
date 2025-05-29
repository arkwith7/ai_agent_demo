<template>
  <div class="warren-buffett">
    <section class="hero">
      <h1>워렌 버핏의 투자 철학</h1>
      <p>가치 투자의 대가, 워렌 버핏의 투자 원칙을 AI로 구현하다</p>
    </section>

    <section class="content">
      <div class="profile">
        <div class="profile-image">
          <Icon icon="mdi:account-tie" />
        </div>
        <div class="profile-content">
          <h2>워렌 버핏</h2>
          <p class="title">버크셔 해서웨이 회장</p>
          <p class="description">
            "가격이란 당신이 지불하는 것이고, 가치란 당신이 얻는 것이다."
            워렌 버핏은 장기적 관점에서 기업의 내재가치를 분석하고, 
            안전마진을 확보한 투자를 통해 세계 최고의 투자자로 자리매김했습니다.
          </p>
        </div>
      </div>

      <div class="principles">
        <h2>핵심 투자 원칙</h2>
        <div class="principle-grid">
          <div class="principle-card">
            <Icon icon="mdi:magnify" />
            <h3>기업 가치 분석</h3>
            <p>
              기업의 재무제표를 면밀히 분석하여 내재가치를 평가하고,
              장기적인 성장 가능성을 판단합니다.
            </p>
          </div>
          <div class="principle-card">
            <Icon icon="mdi:shield-check" />
            <h3>안전마진</h3>
            <p>
              기업의 내재가치보다 낮은 가격에 매수하여
              투자 위험을 최소화합니다.
            </p>
          </div>
          <div class="principle-card">
            <Icon icon="mdi:clock-outline" />
            <h3>장기 투자</h3>
            <p>
              단기적인 시장 변동에 흔들리지 않고,
              장기적인 관점에서 투자합니다.
            </p>
          </div>
          <div class="principle-card">
            <Icon icon="mdi:crown" />
            <h3>경제적 해자</h3>
            <p>
              경쟁사가 쉽게 따라올 수 없는
              강력한 사업 모델을 가진 기업을 선호합니다.
            </p>
          </div>
        </div>
      </div>

      <div class="analysis">
        <h2>AI Agent의 분석 방법</h2>
        <div class="analysis-steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>기업 분석</h3>
            <p>
              재무제표, 사업 모델, 경쟁력 등을
              종합적으로 분석합니다.
            </p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>가치 평가</h3>
            <p>
              다양한 가치 평가 모델을 활용하여
              기업의 내재가치를 산출합니다.
            </p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>안전마진 확인</h3>
            <p>
              현재 주가와 내재가치를 비교하여
              충분한 안전마진이 있는지 확인합니다.
            </p>
          </div>
          <div class="step">
            <div class="step-number">4</div>
            <h3>투자 판단</h3>
            <p>
              분석 결과를 바탕으로
              투자 여부를 최종 판단합니다.
            </p>
          </div>
        </div>
      </div>

      <div class="cta">
        <h2>워렌 버핏의 투자 철학 체험하기</h2>
        <p>AI Agent와 함께 워렌 버핏의 투자 원칙을 실천해보세요.</p>
        <router-link to="/demo" class="cta-button">데모 시작하기</router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
</script>

<style scoped>
.warren-buffett {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border-radius: 1rem;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 3rem;
  color: #ffffff;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  color: #cccccc;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.profile {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 2rem;
  align-items: center;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-image {
  font-size: 6rem;
  color: #4CAF50;
  opacity: 0.8;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-content h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.profile-content .title {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 1rem;
}

.profile-content .description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #666;
}

.principles {
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.principles h2 {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

.principle-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.principle-card {
  text-align: center;
  padding: 2rem;
  background: #f5f5f5;
  border-radius: 1rem;
  transition: transform 0.3s ease;
}

.principle-card:hover {
  transform: translateY(-5px);
}

.principle-card .iconify {
  font-size: 2.5rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.principle-card h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.principle-card p {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #666;
}

.analysis {
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.analysis h2 {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

.analysis-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.step {
  text-align: center;
  padding: 2rem;
  background: #f5f5f5;
  border-radius: 1rem;
  position: relative;
}

.step-number {
  width: 40px;
  height: 40px;
  background: #4CAF50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 auto 1rem;
}

.step h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.step p {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #666;
}

.cta {
  text-align: center;
  padding: 4rem 0;
  background: #f5f5f5;
  border-radius: 1rem;
}

.cta h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.cta p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background: #45a049;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .profile {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .profile-image {
    margin: 0 auto;
  }

  .principle-grid,
  .analysis-steps {
    grid-template-columns: 1fr;
  }
}
</style> 