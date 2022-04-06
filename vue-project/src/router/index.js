import { createRouter, createWebHistory } from "vue-router";
import HelloWorld from "@/components/HelloWorld";

const routes = [
  {
    path: "/",
    name: "home",
    component: HelloWorld,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
