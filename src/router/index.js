import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/game',
    name: 'game',
    component: () => import('../views/GameView.vue')
  },
  {
    path: '/character',
    name: 'character',
    component: () => import('../views/CharacterView.vue')
  },
  {
    path: '/task',
    name: 'task',
    component: () => import('../views/TaskView.vue')
  },
  {
    path: '/battle',
    name: 'battle',
    component: () => import('../views/BattleView.vue')
  },
  {
    path: '/ranking',
    name: 'ranking',
    component: () => import('../views/RankingView.vue')
  },
  {
    path: '/user-info',
    name: 'user-info',
    component: () => import('../views/UserInfoView.vue')
  },
  {
    path: '/level',
    name: 'level',
    component: () => import('../views/LevelView.vue')
  },
  {
    path: '/equipment',
    name: 'equipment',
    component: () => import('../views/EquipmentView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router