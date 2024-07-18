<template>
    <div class="blogdisplay">
      
      <h6 class="mb0">{{ blog.blog_name }} -
            <router-link :to="`/profile/${id}`">
             By {{ author }} 
            </router-link>
        </h6>
      
        <b-card :img-src="img_src+blog.image_loc" img-alt="Card image" img-top>
        <b-card-text>
          <h5>
            {{ blog.description }}
          </h5>
          <br>
          <p> Last Updated on: {{ formatDate(blog.last_updated_on) }}</p>
        </b-card-text>
        <template #footer>
          <b-icon icon="heart-fill" variant="danger">
          </b-icon>
          {{ blog.likes.length }} likes
        </template>
       
      </b-card>
    </div>
  </template>
  
  <script>


  export default {
    name: 'BlogDisplay',
    data(){
      return{
        img_src:"http://127.0.0.1:5000/static/blog_images/"
      }
    } ,
    props: {
        blog: {
          required: true,
          type: Object
        },
        author:{
          required: true,
          type: String
        },
        id:{
          type: Number
        }
    },
    methods:{
      formatDate(dateString) {
            const date = new Date(dateString);
                // Then specify how you want your dates to be formatted
            return new Intl.DateTimeFormat('default', {dateStyle: 'long'}).format(date);
        }
    },
    components: {
      
    },

   
  }
  </script>
  
  <style scoped>
   .blogdisplay{
      max-width: 375px;

   }
  </style>
  