import { createRouter, createWebHistory } from "vue-router";
import Cookies from "js-cookie";

import { refreshToken } from "@/plugins/login";
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
  },
  {
    path: "/login",
    name: "Login",
    component: LoginHome,
    meta: { unauthorized: true },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterHome,
    meta: { unauthorized: true },
  },
  {
    path: "/category",
    name: "Category",
    component: CategoryPost,
  },
  {
    path: "/my",
    name: "MyHome",
    component: MyHome,
  },
  {
    path: "/write",
    name: "Write",
    component: WriteForm,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (
    Cookies.get("access_token") === null &&
    Cookies.get("refresh_token") !== null
  ) {
    await refreshToken();
  }

  if (
    to.matched.some((record) => record.meta.unauthorized) ||
    Cookies.get("access_token")
  ) {
    return next();
  }

  alert("You Need to Login");
  return next("/login");
});

export default router;
