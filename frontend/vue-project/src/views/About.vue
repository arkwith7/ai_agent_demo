<template>
  <div class="min-h-screen bg-light">
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-primary">Vue + TailwindCSS</h1>
        <nav>
          <ul class="flex space-x-6">
            <li><router-link to="/" class="nav-link">홈</router-link></li>
            <li><router-link to="/about" class="nav-link">소개</router-link></li>
          </ul>
        </nav>
      </div>
    </header>

    <main class="container mx-auto px-4 py-8">
      <section class="text-center mb-12">
        <h2 class="section-title">프로젝트 소개</h2>
        <p class="text-secondary mb-8">이 프로젝트는 Vue 3와 TailwindCSS를 사용하여 개발되었습니다.</p>
      </section>

      <div class="max-w-3xl mx-auto">
        <div class="bg-white p-8 rounded-lg shadow-md">
          <h3 class="text-xl font-bold mb-4">기술 스택</h3>
          <ul class="list-disc list-inside space-y-2 text-secondary">
            <li>Vue 3 - Composition API</li>
            <li>Vue Router - 페이지 라우팅</li>
            <li>Pinia - 상태 관리</li>
            <li>TailwindCSS - 스타일링</li>
            <li>Vite - 빌드 도구</li>
          </ul>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
</script> 