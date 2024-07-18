<template>
    <div class="search">
      <b-form inline>
        <b-form-input
         size="lg" 
         v-model="search_name" placeholder="Type a username.... Jane Doe"
         class="col-sm-4"
         style="margin-left:10%;"
         >
        </b-form-input>
        <b-button variant="secondary" class="btn-lg"
         @click="find_users">
         Search
          <b-icon
          icon="search"
          variant="light">
        </b-icon>
        </b-button>
        
      </b-form>
     
      <!--<div class="mt-5" style="margin-left:10%;margin-right:10%;">
        <b-table :items="users" :fields="fields" >
          <template #cell(username)="data">
            <router-link :to="`/profile/${data.item.user_id}`">
              <b>{{ data.value.toUpperCase() }}</b>
            </router-link>
           
          </template>
          <template #cell(following_status)="data">
            <div v-if="data.value">
              <b-button
                variant="primary"
                @click="unfollow(data.item.user_id);"
                >
                Unfollow
              </b-button>
            </div>
            <div v-else>
              <b-button
                @click="follow(data.item.user_id);"
                >
                Follow
              </b-button>
            </div>
            
           
          </template>

        </b-table>
      </div>-->
      <FollowersDisplayComponent
      :users="users"
      :fields="fields"
      :page="page"
      
      @change="find_users">

      </FollowersDisplayComponent>
    </div>
  </template>
  
  <script>
  import FollowersDisplayComponent from '@/components/FollowersDisplayComponent.vue';
  export default {
    name: 'SearchView',
    
    data(){
      return {
        fields:["username","following_status"],
        search_name:"",
        users:[],
        page:"followers"
      }
    },
    components:{
      FollowersDisplayComponent
    },
    methods:{
      find_users: async function(){
        console.log(this.search_name)
        await fetch('http://127.0.0.1:5000/search_users', {
                method: 'POST',
                body: JSON.stringify({
                  "username":this.search_name, 
                  "user_id": localStorage.getItem("user_id")}),
                headers: {
                'Authentication-Token': localStorage.getItem("token")
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data.users);
                this.users=data.users
                
            }).catch((error) => {
                console.error('Error:', error);
                this.savedIconClass = "text-danger";
            });
      }
    },
    mounted: async function() {
      this.find_users()
    },
  
  }
  </script>
  
  <style scoped>
   .search{
    margin:40px;
   }
  </style>
  