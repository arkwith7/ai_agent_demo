<template>
  <div class="ai-agent-introduction">
    <section class="hero">
      <h1>AI Agent 소개</h1>
      <p>워렌 버핏의 투자 철학을 바탕으로 한 AI 기반 주식 분석 도구</p>
    </section>

    <section class="content">
      <div class="description">
        <h2>AI Agent란?</h2>
        <p>
          AI Agent는 워렌 버핏의 투자 철학을 학습하여 주식 시장을 분석하고 투자 기회를 찾아내는 
          인공지능 기반 도구입니다. 자연어 처리 기술을 활용하여 사용자의 질문에 대해 전문가 수준의 
          분석 결과를 제공합니다.
        </p>
      </div>

      <div class="features">
        <h2>주요 특징</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <i class="fas fa-brain"></i>
            <h3>AI 기반 분석</h3>
            <p>머신러닝과 딥러닝 기술을 활용한 정교한 시장 분석</p>
          </div>
          <div class="feature-card">
            <i class="fas fa-chart-line"></i>
            <h3>실시간 데이터</h3>
            <p>최신 시장 데이터를 기반으로 한 실시간 분석 제공</p>
          </div>
          <div class="feature-card">
            <i class="fas fa-comments"></i>
            <h3>자연어 대화</h3>
            <p>자연스러운 대화를 통한 투자 상담 및 분석</p>
          </div>
        </div>
      </div>

      <div class="process">
        <h2>작동 방식</h2>
        <div class="process-steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>데이터 수집</h3>
            <p>주식 시장의 다양한 데이터를 수집하고 분석</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>패턴 분석</h3>
            <p>워렌 버핏의 투자 패턴을 학습하여 적용</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>투자 제안</h3>
            <p>분석 결과를 바탕으로 투자 기회 제안</p>
          </div>
        </div>
      </div>

      <div class="cta">
        <h2>AI Agent 체험하기</h2>
        <p>지금 바로 AI Agent와 함께 투자 여정을 시작하세요.</p>
        <router-link to="/demo" class="cta-button">데모 시작하기</router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import '@fortawesome/fontawesome-free/css/all.css'
</script>

<style scoped>
.ai-agent-introduction {
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

.description {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.description h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.description p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #666;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card i {
  font-size: 2.5rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.5;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.step {
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
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
  margin-bottom: 1rem;
  color: #333;
}

.step p {
  color: #666;
  line-height: 1.5;
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

  .feature-grid,
  .process-steps {
    grid-template-columns: 1fr;
  }
}
</style> 