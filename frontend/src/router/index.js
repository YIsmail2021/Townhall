import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  // Lazy loading the category site.
  {
    path: '/category',
    name: 'category',
    component: () => import(/* webpackChunkName: "about" */ '../views/CategoryView.vue')
  },
  // Lazy loading the post site.
  {
    path: '/post/:postId',
    name: 'post',
    component: () => import(/* webpackChunkName: "about" */ '../views/PostView.vue')
  },
  // Lazy loading the create post site.
  {
    path: '/create-post/',
    name: 'create-post',
    component: () => import(/* webpackChunkName: "about" */ '../views/CreatePostView.vue')
  },
  // Lazy loading the create category site.
  {
    path: '/create-category/',
    name: 'create-category',
    component: () => import(/* webpackChunkName: "about" */ '../views/CreateCategoryView.vue')
  },
  // Lazy loading the list posts based on category site.
  {
    path: '/list-posts/',
    name: 'list-posts',
    component: () => import(/* webpackChunkName: "about" */ '../views/listPostsView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
