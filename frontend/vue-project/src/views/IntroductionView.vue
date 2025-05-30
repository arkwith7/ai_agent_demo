<template>
  <div class="introduction-container">
    <section class="hero-section">
      <h1>AI Agent 소개</h1>
      <p class="subtitle">인공지능이 주식 투자를 더 스마트하게 만듭니다</p>
    </section>

    <main class="content-container">
      <section class="section">
        <h2>AI Agent란?</h2>
        <p>
          AI Agent는 사용자의 투자 목표와 선호도를 이해하고, 실시간으로 주식 시장을 분석하여
          최적의 투자 기회를 찾아주는 인공지능 비서입니다. 복잡한 차트와 지표를 직접 분석할 필요 없이,
          자연스러운 대화를 통해 원하는 정보를 얻을 수 있습니다.
        </p>
      </section>

      <section class="section">
        <h2>주요 특징</h2>
        <div class="features-grid">
          <div class="feature-box" v-for="(feature, index) in features" :key="index">
            <i :class="['feature-icon', feature.icon]"></i>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>작동 방식</h2>
        <div class="process-steps">
          <div class="step" v-for="(step, index) in processSteps" :key="index">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3>{{ step.title }}</h3>
              <p>{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>시작하기</h2>
        <p>
          AI Agent와 함께 스마트한 투자를 시작해보세요. 지금 바로 데모를 체험하고
          미래의 투자 방식을 경험해보세요.
        </p>
        <router-link to="/demo" class="cta-button">
          데모 체험하기 <i class="fa-solid fa-arrow-right"></i>
        </router-link>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const features = ref([
  {
    icon: 'fa-solid fa-brain',
    title: '지능형 분석',
    description: '머신러닝과 딥러닝을 활용한 고급 시장 분석'
  },
  {
    icon: 'fa-solid fa-comments',
    title: '자연어 처리',
    description: '자연스러운 대화를 통한 정보 요청과 응답'
  },
  {
    icon: 'fa-solid fa-chart-line',
    title: '실시간 데이터',
    description: '실시간 시장 데이터 기반의 정확한 분석'
  }
])

const processSteps = ref([
  {
    title: '목표 설정',
    description: '투자 목표와 선호도를 AI Agent에게 전달합니다.'
  },
  {
    title: '시장 분석',
    description: 'AI Agent가 실시간으로 시장을 분석하고 기회를 찾습니다.'
  },
  {
    title: '추천 제공',
    description: '분석 결과를 바탕으로 최적의 투자 기회를 추천합니다.'
  },
  {
    title: '결정 지원',
    description: '투자 결정에 필요한 모든 정보를 제공합니다.'
  }
])
</script>

<style scoped>
.introduction-container {
  padding-bottom: 60px;
}

.hero-section {
  background: linear-gradient(rgba(0, 123, 255, 0.05), rgba(0, 123, 255, 0.05)),
    url('https://source.unsplash.com/random/1600x600/?artificial-intelligence') no-repeat center center/cover;
  padding: 100px 20px;
  text-align: center;
  color: var(--text-color);
}

.hero-section h1 {
  font-size: 3em;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.subtitle {
  font-size: 1.5em;
  color: var(--secondary-color);
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section {
  margin-bottom: 60px;
}

.section h2 {
  text-align: center;
  font-size: 2.2em;
  margin-bottom: 40px;
  color: var(--text-color);
}

.section p {
  text-align: center;
  font-size: 1.1em;
  line-height: 1.7;
  color: var(--secondary-color);
  max-width: 800px;
  margin: 0 auto 30px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.feature-box {
  background: var(--card-bg);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-box:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5em;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.feature-box h3 {
  font-size: 1.4em;
  margin-bottom: 15px;
  color: var(--text-color);
}

.process-steps {
  max-width: 800px;
  margin: 0 auto;
}

.step {
  display: flex;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.step-number {
  background: var(--primary-color);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  font-weight: bold;
  margin-right: 20px;
  flex-shrink: 0;
}

.step-content {
  flex-grow: 1;
}

.step-content h3 {
  margin: 0 0 10px 0;
  color: var(--text-color);
}

.step-content p {
  margin: 0;
  text-align: left;
}

.cta-button {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 15px 35px;
  text-decoration: none;
  border-radius: 30px;
  font-size: 1.2em;
  font-weight: bold;
  transition: background-color 0.2s ease, transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.cta-button:hover {
  background: var(--hover-darken-primary);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5em;
  }

  .subtitle {
    font-size: 1.2em;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .step {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .step-number {
    margin: 0 0 15px 0;
  }

  .step-content p {
    text-align: center;
  }
}
</style> 