<template>
  <div class="home">
   <h2>
      Welcome {{ user }} - Your daily feed
   </h2>
   <br>
    <div v-if="feed_blogs.length==0" class="mt-3">
      <h4>
        <hr>
        There are no posts in your feed.
        <br>
        Connect with other users to see what they are posting
        <br>
        <br>
        <router-link :to="`/search`">Search users</router-link>
        <hr>
      </h4>
    </div>
    <div v-else class="container-fluid row justify-content-right d-flex" v-for="feed in feed_blogs" :key="feed['.username']">
      <div v-for="blog in feed.blogs"
            :key="blog['.blog_id']"
            class="col-sm-4">
            <p>
        <BlogDisplay
            :blog="blog"
            :author="feed.username"
            :id="feed.id"
          /></p>
          <div v-if="likes[blog.blog_id]">
            <b-button  variant="light" class="mt-2 h3" @click="unlike_blog(blog.blog_id)">
              <b-icon icon="heart-fill" variant="danger">
              </b-icon>
            </b-button>
          </div>
          <div v-else>
            <b-button variant="light" class="mt-2 h3" @click="like_blog(blog.blog_id)">
              <b-icon icon="heart" variant="danger" >
              </b-icon>
            </b-button>
           
          </div>
      </div>    
    </div>
   
   <br>

   <div class="container-fluid">
    <div class="row justify-content-right d-flex">
      
    </div>

   </div>
  </div>
</template>

<script>

import BlogDisplay from '@/components/BlogDisplayComponent.vue'
export default {
  name: 'HomeView',
  
  data(){
    return {
     user: "",
     followees: [],
     feed_blogs: [],
     likes: Object
    }
  },
  components: {
    BlogDisplay
  },
  methods:{
    get_likes: async function(blog_id){
      await fetch('http://127.0.0.1:5000/api/likes/'+blog_id+'/'+localStorage.user_id, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem("token")
              }
            }).then(response => response.json())
            .then(data => {
              //console.log(data.length);
              if(data.length==0){
                this.likes[blog_id]=false
              }else{
                this.likes[blog_id]=true
              }
              console.log(blog_id,this.likes[blog_id])
              
            }).catch((error) => {
              console.error('Error:', error);
              this.savedIconClass = "text-danger";
            });
    },
    get_blogs:function (id){
      
      this.feed_blogs=[]
      
      var api='http://127.0.0.1:5000/api/blogs/'+id;
      fetch(api, {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json'
                }
              }).then(response => response.json())
              .then(data => {
                //console.log(data);
                if(data.code){
                  console.log(data.description);

                }else
                {
                  this.feed_blogs=this.feed_blogs.concat(data);
                  console.log("Data",data)
                  for(let id in data["blogs"]){
                    console.log(data["blogs"][id]["blog_id"]);
                    this.get_likes(data["blogs"][id]["blog_id"]);
                  
                  }

                }
              })
              .catch((error) => {
                console.error(error);
                //this.error_msg = error.description;
              });
              
    },

    like_blog: async function(blog_id){

        await fetch('http://127.0.0.1:5000/api/likes', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem("token")
                  },
                  body: JSON.stringify({
                  "user_id":localStorage.getItem("user_id"), 
                  "blog_id": blog_id}),
                }).then(response => response.json())
                .then(data => {
                  console.log(data);
                  
                })
                .catch((error) => {
                  console.error('Error:', error);
                  this.savedIconClass = "text-danger";
                });
            this.likes[blog_id]=true;
            await this.get_feed()
            this.$forceUpdate()
    },

    unlike_blog: async function(blog_id){

    await fetch('http://127.0.0.1:5000/api/likes/'+blog_id+'/'+localStorage.getItem("user_id"), {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem("token")
              }
            }).then(response => response.json())
            .then(data => {
              console.log(data);
              
            })
            .catch((error) => {
              console.error('Error:', error);
              this.savedIconClass = "text-danger";
            });
        this.likes[blog_id]=false;
        await  this.get_feed()
            this.$forceUpdate()
    },
    get_feed:function() {


    fetch('http://127.0.0.1:5000/api/followers/'+localStorage.getItem("user_id"), {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem("token")
              }
            }).then(response => response.json())
            .then(data => {
              console.log(data);
              this.followees=data;
              for(let id in this.followees){
                console.log(this.followees[id]["follow_id"]);
                this.get_blogs(this.followees[id]["follow_id"]);
                console.log(this.feed_blogs)
               
              }
            })
            .catch((error) => {
              console.error('Error:', error);
              this.savedIconClass = "text-danger";
            });
            this.$forceUpdate()
    },
    isliked: function(blog_id){
      return this.likes[blog_id]
    }
  },
  mounted: async function() {
    await fetch('http://127.0.0.1:5000/api/user/'+localStorage.user_id, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem("token")
              }
            }).then(response => response.json())
            .then(data => {
              console.log(data);
              this.$store.commit('setuser',data)
              this.user=this.$store.state.user["username"]
              
            }).catch((error) => {
              console.error('Error:', error);
              this.savedIconClass = "text-danger";
            });

    await this.get_feed();

  },
  computed: {
    
  }
  
}
</script>

<style scoped>
  .home{

    margin:20px;
    margin-top:40px;
  }
</style>
