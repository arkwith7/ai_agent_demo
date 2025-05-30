<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>AI Agent, <br>나만의 주식 분석 비서를 경험하세요.</h1>
        <p>복잡한 설정과 버튼 클릭은 이제 그만! <br> AI Agent와 대화하며 원하는 종목을 찾고, 분석 과정을 직접 확인해보세요.</p>
        <router-link to="/demo" class="cta-button">
          AI Agent 데모 체험하기 <i class="fa-solid fa-arrow-right"></i>
        </router-link>
      </div>
    </section>

    <main class="content-container">
      <section class="section">
        <h2>AI Agent 주식 분석, 무엇이 다른가요?</h2>
        <p>본 데모 서비스는 단순한 종목 추천을 넘어, AI Agent가 사용자의 요청을 어떻게 이해하고, 어떤 과정을 통해 정보를 분석하여 결과를 도출하는지 그 '경험'에 초점을 맞추고 있습니다. AI Agent의 능동적인 문제 해결 과정을 직접 체험하며 미래의 투자 방식을 엿볼 수 있습니다.</p>
        <router-link to="/introduction" class="learn-more-link">AI Agent 더 알아보기 &raquo;</router-link>
      </section>

      <section class="section">
        <h2>주요 체험 포인트</h2>
        <div class="features-grid">
          <div class="feature-box" v-for="(feature, index) in features" :key="index">
            <i :class="['feature-icon', feature.icon]"></i>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const features = ref([
  {
    icon: 'fas fa-comments',
    title: '자연스러운 대화',
    description: '복잡한 설정 없이 대화하듯이 원하는 정보를 요청하세요.'
  },
  {
    icon: 'fas fa-chart-line',
    title: '실시간 분석',
    description: 'AI Agent가 실시간으로 주식 데이터를 분석하고 인사이트를 제공합니다.'
  },
  {
    icon: 'fas fa-lightbulb',
    title: '스마트 추천',
    description: '당신의 투자 성향과 목표에 맞는 최적의 종목을 추천해드립니다.'
  }
])
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero {
  width: 100%;
  background: linear-gradient(rgba(0, 123, 255, 0.05), rgba(0, 123, 255, 0.05)),
    url('https://source.unsplash.com/random/1600x600/?stocks,technology') no-repeat center center/cover;
  padding: 80px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-content {
  background-color: rgba(255, 255, 255, 0.85);
  padding: 40px;
  border-radius: 10px;
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
}

.hero h1 {
  margin-bottom: 20px;
  font-size: 2.8em;
  font-weight: 700;
  color: var(--primary-color);
}

.hero p {
  font-size: 1.25em;
  margin-bottom: 30px;
  color: var(--secondary-color);
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
  background-color: var(--hover-darken-primary);
  transform: translateY(-2px);
}

.content-container {
  width: 100%;
  max-width: 1100px;
  margin: 40px auto;
  padding: 20px;
  box-sizing: border-box;
}

.section {
  padding: 40px 0;
  margin-bottom: 30px;
  border-bottom: 1px solid var(--border-color);
}

.section:last-child {
  border-bottom: none;
}

.section h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.2em;
  color: var(--text-color);
  font-weight: 600;
}

.section p {
  text-align: center;
  font-size: 1.1em;
  color: var(--secondary-color);
  line-height: 1.7;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.learn-more-link {
  display: block;
  width: fit-content;
  margin: 20px auto 0 auto;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: bold;
  padding: 10px 20px;
  border: 2px solid var(--primary-color);
  border-radius: 25px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.learn-more-link:hover {
  background-color: var(--primary-color);
  color: white;
}

.features-grid {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 20px;
}

.feature-box {
  background-color: var(--card-bg);
  text-align: center;
  padding: 30px 25px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  flex-basis: calc(33.333% - 40px);
  min-width: 280px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.12);
}

.feature-box .feature-icon {
  font-size: 3em;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.feature-box h3 {
  font-size: 1.4em;
  margin-bottom: 15px;
  color: var(--text-color);
}

.feature-box p {
  font-size: 0.95em;
  color: var(--secondary-color);
  line-height: 1.6;
  text-align: center;
}
</style>
