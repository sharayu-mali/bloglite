<template>
   
      <div class="mt-5" style="margin-left:10%;margin-right:10%;">
        <b-table :items="users" :fields="fields" >
          <template #cell(username)="data">
            <router-link :to="`/profile/${data.item.user_id}`">
              <b>{{ data.value.toUpperCase() }}</b>
            </router-link>
           
          </template>
          <template #cell(following_status)="data">
            <!--<div v-if="page=='following'">
                <b-button
                variant="primary"
                @click="unfollow_follower(data.item.user_id);"
                >
                Unfollow
              </b-button>
            </div>
            <div v-else>-->

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
    
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'FollowersDisplayComponent',
    
    props: {
        users: {
          required: true,
          type: Array
        },
        fields:{
          required: true,
          type: Array
        },
        page:{
          type: String
        }
    },
   
    methods:{
        unfollow_follower: async function(follow_id){
       await fetch('http://127.0.0.1:5000/api/followers/'+follow_id+'/'+localStorage.getItem("user_id"), {
               method: 'DELETE',
               headers: {
               'Authentication-Token': localStorage.getItem("token")
               }
           }).then(response => response.json())
           .then(data => {
               console.log(data);
               
           }).catch((error) => {
               console.error('Error:', error);
               this.savedIconClass = "text-danger";
           });
           this.$emit('change')
     },
      follow: async function(follow_id){
       
        await fetch('http://127.0.0.1:5000/api/followers', {
                method: 'POST',
                body: JSON.stringify({
                  "user_id":  localStorage.getItem("user_id"),
                  "follow_id": follow_id
                  }),
                headers: {
                  'Content-Type':"application/json",
                'Authentication-Token': localStorage.getItem("token")
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                
            }).catch((error) => {
                console.error('Error:', error);
                this.savedIconClass = "text-danger";
            });
            this.$emit('change')
      },
      unfollow: async function(follow_id){
        await fetch('http://127.0.0.1:5000/api/followers/'+localStorage.getItem("user_id")+'/'+follow_id, {
                method: 'DELETE',
                headers: {
                'Authentication-Token': localStorage.getItem("token")
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                
            }).catch((error) => {
                console.error('Error:', error);
                this.savedIconClass = "text-danger";
            });
            this.$emit('change')
      }
    }
  
  }
  </script>
  
  <style scoped>
   .component_display{
    margin:40px;
   }
  </style>
  