import { createRouter, createWebHistory } from "vue-router";
import Home from "./components/Home";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
];

const router = createRouter({
  history: createWebHistory("/GuitarTabPro/"),
  routes,
});

export default router;
