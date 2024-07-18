<template>
    <div class="connections">
        <div class="container-fluid">
            <div class="row justify-content-end d-flex">            
                <div class="col-sm-6">
                    <h2>
                        Your Followers
                    </h2>
                        <b-table :items="followers" :fields="fields" >
                        <template #cell(username)="data">
                            <router-link :to="`/profile/${data.item.user_id}`">
                            <b>{{ data.value.toUpperCase() }}</b>
                            </router-link>
                        
                        </template>
                        <template #cell(following_status)="data">
                            <b-button
                                variant="primary"
                                @click="unfollow_follower(data.item.user_id);"
                                >
                                Unfollow
                            </b-button>
                        </template>

                        </b-table>
                   
                </div> 
                <div class="col-sm-6">
                    <h2>
                        People you follow
                    </h2>
                    <b-table :items="following" :fields="fields" >
                        <template #cell(username)="data">
                            <router-link :to="`/profile/${data.item.user_id}`">
                            <b>{{ data.value.toUpperCase() }}</b>
                            </router-link>
                        
                        </template>
                        <template #cell(following_status)="data">
                           <b-button
                                variant="primary"
                                @click="unfollow(data.item.user_id);"
                                >
                                Unfollow
                            </b-button>
                            /
                           <b-button
                                @click="follow(data.item.user_id);"
                                >
                                Follow
                            </b-button>
                         </template>
                        </b-table>
                </div>               

            </div>
        </div>
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'ConnectionsView',
    
    data(){
      return {
        fields:["username","following_status"],
        followers:[],
        following:[]
      }
    },
    methods: {
      
        get_followers: async function(){
       
            await fetch('http://127.0.0.1:5000/get_connections/'+localStorage.user_id, {
                method: 'GET',
                headers: {
                'Authentication-Token': localStorage.getItem("token")
                }
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                this.followers=data.followers;
                this.following=data.following;
            }).catch((error) => {
                console.error('Error:', error);
                this.savedIconClass = "text-danger";
            });
        
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
           this.get_followers()
     },
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
           this.get_followers()
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
           
            
            this.get_followers()
      }
    },
    mounted: async function(){
        this.get_followers()
    }
  
  }
  </script>
  
  <style scoped>
    .connections{
        margin-top:40px;
    }
  </style>
  