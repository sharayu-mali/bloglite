<template>
  <div class="profile">
    <div v-if="error_msg" class="h3 text-danger m-4">
      {{ error_msg }}!!
    </div>
   
    <div v-else>
      <div class="container-fluid">

        <div class="row justify-content-right d-flex">
          <div class="col-sm-3">
            <h3>
              <b-icon icon="person-square"
                      variant="info"
                      class="h1"
                      style="width: 120px; height: 120px;">
              </b-icon>
              <br>
              {{ user.username }}'s Profile
              <br>
             
            </h3>
          </div>
          <div class="col-sm-3 my-auto">
            <h3> Total Posts - {{ user.no_blogs }} </h3>
          </div>
          <div v-if="mine" class="col-sm-3 my-auto">
            <router-link :to="`/myfollowees`">
              <h3> Following - {{ user.no_following }} </h3>
            </router-link>
          </div>
          <div v-else class="col-sm-3 my-auto">
            <h3> Following - {{ user.no_following }} </h3>
          </div>
          <div v-if="mine" class="col-sm-3 my-auto">
            <router-link :to="`/myfollowers`">
              <h3>  Followers - {{ user.no_followers }} </h3>
            </router-link>
          </div>
          <div v-else class="col-sm-3 my-auto">
            <h3>  Followers - {{ user.no_followers }} </h3>
          </div>

        </div>
       
        
        <br>
     
        <div class="row justify-content-right d-flex">
          <BlogDisplay
            v-for="blog in user.blogs"
            :blog="blog"
            :author="user.username"
            :id="user.id"
            :key="blog['.blog_id']"
            class="col-sm-4 m-3"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import BlogDisplay from '@/components/BlogDisplayComponent.vue'
export default {
  name: 'ProfileView',
    
  data(){
    return {
      user:Object,
      error_msg:null
    }
  },
  components: {
    BlogDisplay
  },
  created() {
    this.$watch(
      () => this.$route.params,
      (toParams, previousParams) => {
        // react to route changes...
        console.log(previousParams);
        this.id=toParams.id;
        this.fetchData();
        
      }
    )
  },
  computed:{
    mine(){
      return this.user.id==localStorage.getItem("user_id")
    }
  },
  methods:{
    fetchData: function() {
      this.id=this.$route.params.id;
      var api='http://127.0.0.1:5000/api/user/'+this.id;
      fetch(api, {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',   
                'Authentication-Token': localStorage.getItem("token")
                }
              }).then(response => response.json())
              .then(data => {
                console.log(data);
                if(data.code){
                  this.error_msg=data.description;
                }else
                {
                  this.user=data
                  this.error_msg=null;
                }
              })
              .catch((error) => {
                console.error(error);
                this.error_msg = error.description;
              });
      } 

  },
  mounted(){
    this.fetchData();
  }
}
</script>

<style scoped>
  .profile{
    margin:20px;

  }


</style>
