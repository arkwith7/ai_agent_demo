<script setup lang="ts">
import { Icon } from '@iconify/vue'
</script>

<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    <header class="bg-white border-bottom shadow-sm py-3 mb-4">
      <div class="container d-flex justify-content-between align-items-center">
        <div class="fw-bold fs-3 text-primary">
          <Icon icon="mdi:brain" class="me-2" />AI Agent
        </div>
        <nav>
          <ul class="nav">
            <li class="nav-item"><router-link to="/key-features" class="nav-link">주요 기능</router-link></li>
            <li class="nav-item"><router-link to="/ai-agent-introduction" class="nav-link">AI Agent 소개</router-link></li>
            <li class="nav-item"><router-link to="/warren-buffett" class="nav-link">워렌 버핏</router-link></li>
            <li class="nav-item"><router-link to="/login" class="nav-link">로그인</router-link></li>
            <li class="nav-item"><router-link to="/signup" class="nav-link">회원가입</router-link></li>
          </ul>
        </nav>
      </div>
    </header>
    <main class="flex-grow-1 d-flex flex-column justify-content-center align-items-center">
      <section class="text-center mb-5 w-100 d-flex justify-content-center">
        <div class="bg-white p-5 rounded shadow-lg" style="max-width:600px; width:100%;">
          <h1 class="display-4 fw-bold text-primary mb-3">AI Agent 주식 분석 비서</h1>
          <p class="lead text-secondary mb-4">인공지능 기반의 스마트한 주식 분석 도구로, 당신의 투자 결정을 더욱 현명하게 만들어드립니다.</p>
          <router-link to="/demo" class="btn btn-primary btn-lg">
            지금 시작하기 <Icon icon="mdi:arrow-right" class="ms-2" />
          </router-link>
        </div>
      </section>
      <section class="w-100 d-flex justify-content-center mb-5">
        <div class="w-100" style="max-width:1200px;">
          <h2 class="text-center mb-4 fw-semibold">주요 체험 포인트</h2>
          <div class="row g-4 justify-content-center w-100">
            <div class="col-12 col-md-4">
              <div class="card h-100 text-center shadow-sm">
                <div class="card-body">
                  <Icon icon="mdi:chart-line" class="text-primary mb-3" width="48" height="48" />
                  <h5 class="card-title">실시간 시장 분석</h5>
                  <p class="card-text">최신 시장 데이터를 기반으로 한 실시간 분석과 예측을 제공합니다.</p>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-4">
              <div class="card h-100 text-center shadow-sm">
                <div class="card-body">
                  <Icon icon="mdi:robot" class="text-primary mb-3" width="48" height="48" />
                  <h5 class="card-title">AI 기반 추천</h5>
                  <p class="card-text">머신러닝 알고리즘을 통한 맞춤형 투자 추천을 받아보세요.</p>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-4">
              <div class="card h-100 text-center shadow-sm">
                <div class="card-body">
                  <Icon icon="mdi:shield-check" class="text-primary mb-3" width="48" height="48" />
                  <h5 class="card-title">리스크 관리</h5>
                  <p class="card-text">체계적인 리스크 관리 시스템으로 안전한 투자를 도와드립니다.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="container mb-5">
        <h2 class="text-center mb-4 fw-semibold">AI Agent의 특별함</h2>
        <p class="text-center text-secondary mb-3">우리의 AI Agent는 단순한 분석 도구를 넘어, 당신의 투자 파트너가 되어드립니다. 워렌 버핏의 투자 철학을 바탕으로 한 분석과 함께, 최신 기술을 활용한 예측 모델을 통해 더욱 정확한 투자 결정을 내릴 수 있도록 도와드립니다.</p>
        <div class="text-center">
          <router-link to="/ai-agent-introduction" class="btn btn-outline-primary">더 알아보기</router-link>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --light-bg: #f8f9fa;
  --border-color: #dee2e6;
  --text-color: #212529;
  --card-bg: #ffffff;
  --hover-darken-primary: #0056b3;
}

.home {
  width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.static-header {
  background: var(--card-bg);
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.container {
  width: 90%;
  max-width: 1100px;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8em;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: bold;
}

.logo .mdi-brain {
  margin-right: 8px;
}

nav ul {
  padding: 0;
  list-style: none;
  text-align: center;
  margin: 0;
}

nav ul li {
  display: inline;
  margin-left: 25px;
}

nav ul li:first-child {
  margin-left: 0;
}

nav ul li a {
  color: var(--text-color);
  text-decoration: none;
  font-weight: 500;
  padding: 8px 0;
  transition: color 0.2s ease;
}

nav ul li a:hover,
nav ul li a.active {
  color: var(--primary-color);
  border-bottom: 2px solid var(--primary-color);
}

.hero {
  background: linear-gradient(rgba(0, 123, 255, 0.05), rgba(0, 123, 255, 0.05)),
              url('https://source.unsplash.com/random/1600x600/?stocks,technology') no-repeat center center/cover;
  background-color: var(--primary-color);
  color: var(--text-color);
  padding: 80px 20px;
  text-align: center;
}

.hero-content {
  background-color: rgba(255, 255, 255, 0.85);
  display: inline-block;
  padding: 40px;
  border-radius: 10px;
  max-width: 700px;
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

.cta-button .mdi-arrow-right {
  margin-left: 10px;
  transition: transform 0.3s ease;
}

.cta-button:hover .mdi-arrow-right {
  transform: translateX(5px);
}

.content-container {
  width: 90%;
  max-width: 1100px;
  margin: 40px auto;
  padding: 20px;
  background-color: transparent;
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
</style>
