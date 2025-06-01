import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Analysis from '../views/Analysis.vue'
import IntroAIAgent from '../views/IntroAIAgent.vue'
import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: Analysis,
      meta: { requiresAuth: true }
    },
    {
      path: '/intro-ai-agent',
      name: 'intro-ai-agent',
      component: IntroAIAgent
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    }
  ]
})

// 인증 가드
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 인증이 필요한 페이지에 접근하려고 할 때 로그인 페이지로 리다이렉트
    next({ name: 'signin', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router 