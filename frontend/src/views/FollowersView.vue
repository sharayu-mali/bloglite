<template>
    <div class="followers">
     
        <h2>
            Your Followers: 
        </h2>
            <FollowersDisplayComponent
            :users="$store.state.followers"
            :fields="fields"
            :page="page"
            
            @change="get_followers">

            </FollowersDisplayComponent>
    </div>
  </template>
  
  <script>
  import FollowersDisplayComponent from '@/components/FollowersDisplayComponent.vue';
  export default {
    name: 'FollowersView',
    
    data(){
      return {
        fields:["username","following_status"],
        page:"followers"
      }
    },
    components:{
      FollowersDisplayComponent
    },
    methods:{
        get_followers: async function(){
            console.log("get followers")
            await fetch('http://127.0.0.1:5000/get_connections/'+localStorage.user_id, {
                    method: 'GET',
                    headers: {
                    'Authentication-Token': localStorage.getItem("token")
                    }
                }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.$store.commit('set_followers',data.followers);
                    this.$store.commit('set_following',data.following);
                    
                }).catch((error) => {
                    console.error('Error:', error);
                    this.savedIconClass = "text-danger";
                });
            
        }
   
   },
    mounted: async function() {
      this.get_followers()
    },
  
  }
  </script>
  
  <style scoped>
   .followers{
    margin:40px;
   }
  </style>
  