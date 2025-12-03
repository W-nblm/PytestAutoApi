import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import InterfaceDocs from "../views/InterfaceDocs.vue";
import TestCases from "../views/TestCases.vue";
import TestExecution from "../views/TestExecution.vue";
import CaseGenerator from "../views/CaseGenerator.vue";

const routes = [
  { path: "/", name: "Dashboard", component: Dashboard },
  { path: "/docs", name: "InterfaceDocs", component: InterfaceDocs },
  { path: "/run", name: "TestExecution", component: TestExecution },
  { path: "/case/func", name: "CaseGenerator", component: CaseGenerator },
  { path: "/case/api", name: "TestCases", component: TestCases },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
