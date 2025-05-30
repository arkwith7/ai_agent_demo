<template>
  <div class="features-container">
    <section class="hero-section">
      <h1>주요 기능</h1>
      <p class="subtitle">AI Agent가 제공하는 혁신적인 투자 도구들을 만나보세요</p>
    </section>

    <main class="content-container">
      <section class="section" v-for="(feature, index) in features" :key="index">
        <div class="feature-content" :class="{ 'reverse': index % 2 === 1 }">
          <div class="feature-image">
            <img :src="feature.image" :alt="feature.title">
          </div>
          <div class="feature-text">
            <h2>{{ feature.title }}</h2>
            <p>{{ feature.description }}</p>
            <ul class="feature-list">
              <li v-for="(item, itemIndex) in feature.items" :key="itemIndex">
                <i class="fas fa-check"></i>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section class="section cta-section">
        <h2>지금 바로 시작하세요</h2>
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
    title: '실시간 시장 분석',
    description: 'AI Agent는 실시간으로 시장 데이터를 분석하여 최적의 투자 기회를 찾아냅니다.',
    image: 'https://source.unsplash.com/random/800x600/?stock-market',
    items: [
      '실시간 주가 및 거래량 모니터링',
      '시장 동향 및 패턴 분석',
      '기술적 지표 자동 계산',
      '뉴스 및 이벤트 기반 분석'
    ]
  },
  {
    title: '자연어 기반 대화형 인터페이스',
    description: '복잡한 차트와 지표를 직접 분석할 필요 없이, 자연스러운 대화를 통해 원하는 정보를 얻을 수 있습니다.',
    image: 'https://source.unsplash.com/random/800x600/?chat',
    items: [
      '자연스러운 대화형 인터페이스',
      '맥락 이해 및 추론 능력',
      '다양한 투자 관련 질문 응답',
      '개인화된 투자 조언 제공'
    ]
  },
  {
    title: '스마트 포트폴리오 관리',
    description: 'AI Agent는 투자자의 목표와 위험 선호도에 맞춰 최적의 포트폴리오를 구성하고 관리합니다.',
    image: 'https://source.unsplash.com/random/800x600/?portfolio',
    items: [
      '자산 배분 최적화',
      '리스크 관리 및 분산 투자',
      '포트폴리오 성과 분석',
      '자동 리밸런싱 제안'
    ]
  }
])
</script>

<style scoped>
.features-container {
  padding-bottom: 60px;
}

.hero-section {
  background: linear-gradient(rgba(0, 123, 255, 0.05), rgba(0, 123, 255, 0.05)),
    url('https://source.unsplash.com/random/1600x600/?technology') no-repeat center center/cover;
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
  margin-bottom: 80px;
}

.feature-content {
  display: flex;
  align-items: center;
  gap: 60px;
  margin-bottom: 60px;
}

.feature-content.reverse {
  flex-direction: row-reverse;
}

.feature-image {
  flex: 1;
}

.feature-image img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.feature-text {
  flex: 1;
}

.feature-text h2 {
  font-size: 2em;
  color: var(--text-color);
  margin-bottom: 20px;
}

.feature-text p {
  font-size: 1.1em;
  line-height: 1.7;
  color: var(--secondary-color);
  margin-bottom: 30px;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  color: var(--text-color);
}

.feature-list li i {
  color: var(--primary-color);
  margin-right: 10px;
}

.cta-section {
  text-align: center;
  padding: 60px 20px;
  background: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.cta-section h2 {
  font-size: 2.2em;
  margin-bottom: 20px;
  color: var(--text-color);
}

.cta-section p {
  font-size: 1.1em;
  color: var(--secondary-color);
  max-width: 600px;
  margin: 0 auto 30px;
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

  .feature-content {
    flex-direction: column;
    gap: 30px;
  }

  .feature-content.reverse {
    flex-direction: column;
  }

  .feature-text {
    text-align: center;
  }

  .feature-list li {
    justify-content: center;
  }
}
</style> 