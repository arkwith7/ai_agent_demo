<template>
  <router-view></router-view>
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

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: var(--light-bg);
  color: var(--text-color);
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

/* Font Awesome 아이콘 전역 스타일 */
.fa-solid,
.fas {
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
  display: inline-block;
  line-height: 1;
  vertical-align: middle;
}

/* 이미지 전역 스타일 */
img {
  max-width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
}

.app:not(.home-page) {
  padding-top: 80px;
}

.main-content {
  flex: 1;
  width: 100%;
  padding: 0 20px;
  margin: 0 auto;
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
