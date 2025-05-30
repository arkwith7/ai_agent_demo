<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from './components/layout/AppHeader.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isHomePage = computed(() => route.path === '/')
</script>

<template>
  <div class="app" :class="{ 'home-page': isHomePage }">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --light-bg: #f8f9fa;
  --border-color: #dee2e6;
  --text-color: #212529;
  --card-bg: #ffffff;
  --hover-darken-primary: #0056b3;
}

body {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: var(--light-bg);
  color: var(--text-color);
  min-height: 100vh;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

.app:not(.home-page) {
  padding-top: 80px;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .main-content {
    padding: 0 15px;
  }
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
