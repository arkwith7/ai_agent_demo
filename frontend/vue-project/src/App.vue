<template>
  <div class="min-h-screen bg-light">
    <NavBar />
    <main class="container mx-auto px-4 pt-8 pb-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script> 