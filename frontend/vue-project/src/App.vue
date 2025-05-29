<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <router-view></router-view>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --light-bg: #f8f9fa;
  --border-color: #dee2e6;
  --text-color: #212529;
  --card-bg: #ffffff;
  --hover-darken-primary: #0056b3;
}

body, #app {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: var(--light-bg);
  color: var(--text-color);
  min-height: 100vh;
  width: 100vw;
}

#app {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

.home {
  width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

a {
  text-decoration: none;
  color: inherit;
}
</style>
