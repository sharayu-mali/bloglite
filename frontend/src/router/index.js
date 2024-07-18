import Vue from 'vue'
import VueRouter from 'vue-router'
//import ProfileView from '@/views/ProfileView.vue'
//import UserHomeView from '@/views/UserHomeView.vue'
Vue.use(VueRouter)
//import store from '@/store'
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "User" */ '../views/HomeView.vue'),
    meta: {
      requiresAuth: true
    }
    
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "Login" */ '../components/LoginComponent.vue'),
   
  }, 
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "Register" */ '../components/RegisterComponent.vue'),
   
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: () => import(/* webpackChunkName: "profile" */ '../views/ProfileView.vue'),
    meta: {
      requiresAuth: true
    }
  }, 
  {
    path: '/search',
    name: 'search',
    component: () => import(/* webpackChunkName: "search" */ '../views/SearchView.vue'),
    meta: {
      requiresAuth: true
    }
  }, 
  {
    path: '/myblogs',
    name: 'myblogs',
    component: () => import(/* webpackChunkName: "user_blogs" */ '../views/BlogsView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/myconnections',
    name: 'myconnections',
    component: () => import(/* webpackChunkName: "user_connections" */ '../views/ConnectionsView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/myfollowers',
    name: 'myfollowers',
    component: () => import(/* webpackChunkName: "followers" */ '../views/FollowersView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/myfollowees',
    name: 'myfollowees',
    component: () => import(/* webpackChunkName: "followees" */ '../views/FollowingView.vue'),
    meta: {
      requiresAuth: true
    }
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth){
    if(!localStorage.getItem("token")){
      next({
        name:"login"
      });
    }else{
      next();
    }
  }
  else {
    next();
  }
})


export default router
