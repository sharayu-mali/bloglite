<template>
    
    <div class="header">
        <b-navbar toggleable="lg" type="dark" variant="info">
          <b-navbar-brand href="#">BlogLite</b-navbar-brand>
  
          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  
          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav v-if="$store.state.user">
              <b-nav-item href="#">
                <router-link to="/">Home</router-link>
              </b-nav-item>
              <b-nav-item href="#">
                 <router-link :to="`/profile/${$store.state.user.id}`">My Profile</router-link>
              </b-nav-item>
              <b-nav-item href="#">
                 <router-link :to="`/myblogs`">Blogs</router-link>
              </b-nav-item>
              <!--<b-nav-item href="#">
                 <router-link :to="`/myconnections`">Connections</router-link>
              </b-nav-item>-->
              <b-nav-item href="#">
                 <router-link :to="`/search`">Search</router-link>
              </b-nav-item>
            </b-navbar-nav>
  
            <b-navbar-nav class="ml-auto">
             <b-icon-box-arrow-right @click="logout" class="h2" variant="light"></b-icon-box-arrow-right>
             
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
    </div>
  </template>
  
  <script>
  
  export default {
   
    name: 'HeaderComponent',
    
    methods: {
    logout(){
      console.log("User logged out successfully")
      this.$store.commit('setuser',null);
      this.$router.push("/login")
      localStorage.removeItem("token")
      localStorage.removeItem("user_id")
    }
  }
  
  }
  </script>
  
  <style scoped>
   
  </style>
  