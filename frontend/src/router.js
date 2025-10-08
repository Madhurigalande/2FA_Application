import { createRouter, createWebHistory } from 'vue-router'
import Register from './pages/Register.vue'
import Login from './pages/Login.vue'
import Dashboard from './pages/Dashboard.vue'
import Enable2FA from './pages/Enable2FA.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/enable-2fa', component: Enable2FA },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

