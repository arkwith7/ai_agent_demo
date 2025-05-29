<template>
  <div class="key-features">
    <section class="hero">
      <h1>주요 기능</h1>
      <p>AI Agent의 핵심 기능을 살펴보세요</p>
    </section>

    <section class="content">
      <div class="feature-section">
        <div class="feature-content">
          <h2>자연어 기반 대화형 분석</h2>
          <p>
            복잡한 투자 용어나 전문적인 분석 방법을 알 필요 없이, 
            일상적인 대화처럼 AI Agent와 소통하며 투자 분석을 진행할 수 있습니다.
          </p>
          <ul class="feature-list">
            <li><Icon icon="mdi:check" /> 자연스러운 대화형 인터페이스</li>
            <li><Icon icon="mdi:check" /> 직관적인 질문과 답변</li>
            <li><Icon icon="mdi:check" /> 실시간 피드백 제공</li>
          </ul>
        </div>
        <div class="feature-image">
          <Icon icon="mdi:chat" />
        </div>
      </div>

      <div class="feature-section reverse">
        <div class="feature-content">
          <h2>투명한 분석 과정</h2>
          <p>
            AI Agent는 모든 분석 과정을 투명하게 보여주어, 
            사용자가 투자 결정의 근거를 명확하게 이해할 수 있도록 합니다.
          </p>
          <ul class="feature-list">
            <li><Icon icon="mdi:check" /> 단계별 분석 과정 공개</li>
            <li><Icon icon="mdi:check" /> 데이터 기반 의사결정</li>
            <li><Icon icon="mdi:check" /> 투자 근거 명확화</li>
          </ul>
        </div>
        <div class="feature-image">
          <Icon icon="mdi:chart-bar" />
        </div>
      </div>

      <div class="feature-section">
        <div class="feature-content">
          <h2>전문가 수준의 인사이트</h2>
          <p>
            워렌 버핏의 투자 철학을 학습한 AI Agent는 
            전문가 수준의 투자 분석과 조언을 제공합니다.
          </p>
          <ul class="feature-list">
            <li><Icon icon="mdi:check" /> 워렌 버핏의 투자 원칙 적용</li>
            <li><Icon icon="mdi:check" /> 심층적인 기업 분석</li>
            <li><Icon icon="mdi:check" /> 장기적 관점의 투자 전략</li>
          </ul>
        </div>
        <div class="feature-image">
          <Icon icon="mdi:lightbulb" />
        </div>
      </div>

      <div class="cta">
        <h2>AI Agent 체험하기</h2>
        <p>지금 바로 AI Agent의 강력한 기능을 경험해보세요.</p>
        <router-link to="/demo" class="cta-button">데모 시작하기</router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
</script>

<style scoped>
.key-features {
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

.feature-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-section.reverse {
  direction: rtl;
}

.feature-section.reverse .feature-content {
  direction: ltr;
}

.feature-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-content h2 {
  font-size: 2rem;
  color: #333;
}

.feature-content p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #666;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #666;
}

.feature-list i {
  color: #4CAF50;
}

.feature-image {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 8rem;
  color: #4CAF50;
  opacity: 0.8;
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

  .feature-section {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .feature-image {
    font-size: 6rem;
  }
}
</style> 