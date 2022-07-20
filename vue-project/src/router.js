import { createWebHistory, createRouter } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/components/HomeEnter'),
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: () => import('@/components/auth/RegisterAuth'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/components/auth/LoginAuth'),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
