<template>
  <header class="static-header" v-if="!isHomePage">
    <div class="container">
      <router-link to="/" class="logo">
        <Icon icon="mdi:brain" class="logo-icon" />
        AI Agent
      </router-link>
      <nav>
        <ul>
          <li><router-link to="/" :class="{ active: $route.path === '/' }">홈</router-link></li>
          <li><router-link to="/introduction" :class="{ active: $route.path === '/introduction' }">소개</router-link></li>
          <li><router-link to="/features" :class="{ active: $route.path === '/features' }">주요 기능</router-link></li>
          <li><router-link to="/demo" :class="{ active: $route.path === '/demo' }">데모</router-link></li>
          <li><router-link to="/login" :class="{ active: $route.path === '/login' }">로그인</router-link></li>
          <li><router-link to="/signup" :class="{ active: $route.path === '/signup' }">회원가입</router-link></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Icon } from '@iconify/vue'

const route = useRoute()
const isHomePage = computed(() => route.path === '/')
</script>

<style scoped>
.static-header {
  background: var(--card-bg);
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.container {
  width: 90%;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: bold;
}

.logo-icon {
  font-size: 1.8rem;
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
</style> 