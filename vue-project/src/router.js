import { createWebHistory, createRouter } from 'vue-router';
import parseJwt from '@/api/jwt';

function checkLogin(to, from, next) {
  if (localStorage.getItem('access_token')) {
    const jwtPayload = parseJwt(localStorage.getItem('access_token'));
    if (jwtPayload.exp < Date.now() / 1000) {
      localStorage.removeItem('access_token');
      next('/login');
    }
    next();
  } else {
    next('/login');
  }
}

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
  {
    path: '/me',
    name: 'Me',
    component: () => import('@/components/users/MyEdit'),
    beforeEnter: checkLogin,
  },
  {
    path: '/board',
    name: 'Board',
    component: () => import('@/components/boards/BoardCategory'),
    beforeEnter: checkLogin,
  },
  {
    path: '/board/:name/column/:id',
    name: 'Column',
    component: () => import('@/components/boards/ColumnSpecific'),
    beforeEnter: checkLogin,
    props: true,
  },
  {
    path: '/write',
    name: 'Write',
    component: () => import('@/components/boards/ColumnWrite'),
    beforeEnter: checkLogin,
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    document.getElementById('app').scrollIntoView();
  },
});
