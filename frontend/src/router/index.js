import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import InterfaceDocs from '../views/InterfaceDocs.vue'
import TestCases from '../views/TestCases.vue'
import TestExecution from '../views/TestExecution.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/docs', name: 'InterfaceDocs', component: InterfaceDocs },
  { path: '/cases', name: 'TestCases', component: TestCases },
  { path: '/run', name: 'TestExecution', component: TestExecution }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
