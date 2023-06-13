// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Home from "/src/views/Home.vue"
import Person from "/src/views/Person.vue"
import Company from "/src/views/Company.vue"
import CompanyTable from "/src/components/ColleagueTable.vue"

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: Home,
      },
      {
        path: '/person/:id', 
        name: 'PersonProfile',
        component: Person
      },
      {
        path: '/company/:company', 
        name: 'CompanyPeople',
        component: Company,
      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
