import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/key-features',
      name: 'key-features',
      component: () => import('../views/KeyFeaturesView.vue')
    },
    {
      path: '/ai-agent-introduction',
      name: 'ai-agent-introduction',
      component: () => import('../views/AiAgentIntroductionView.vue')
    },
    {
      path: '/warren-buffett',
      name: 'warren-buffett',
      component: () => import('../views/WarrenBuffettView.vue')
    },
    {
      path: '/demo',
      name: 'demo',
      component: () => import('../views/DemoView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue')
    }
  ]
})

export default router
