import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";

import RegisterHome from "@/components/RegisterHome";
import LoginHome from "@/components/LoginHome";
import KaniHome from "@/components/KaniHome";
import MyHome from "@/components/MyHome";
import WriteForm from "@/components/WriteForm";
import CategoryPost from "@/components/CategoryPost";

const routes = [
  {
    path: "/",
    name: "Home",
    component: KaniHome,
    meta: {
      auth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginHome,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterHome,
  },
  {
    path: "/category",
    name: "Category",
    component: CategoryPost,
    meta: {
      auth: true,
    },
  },
  {
    path: "/my",
    name: "MyHome",
    component: MyHome,
    meta: {
      auth: true,
    },
  },
  {
    path: "/write",
    name: "Write",
    component: WriteForm,
    meta: {
      auth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.auth && !store.getters.user) {
    next("/login");
    return;
  }
  next();
});

export default router;
