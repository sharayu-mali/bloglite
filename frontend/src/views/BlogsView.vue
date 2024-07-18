<template>
    <div class="blog_view">
      <!--Blog Display Completed-->
      <div v-if="error_msg" class="h3 text-danger m-4">
        {{ error_msg }}!!
      </div>
     
      <div v-else>
        <div class="container-fluid">
  
          <div class="row justify-content-end d-flex">
            <div class="col-sm-3">
              <h4> Welcome - {{ user.username }} </h4>
            </div>
            
            <div class="col-sm-3">
              <h4> Your Blog Count - {{ user.no_blogs }} </h4>
            </div>

            <div class="col-sm-2">
              <b-button   @click="show_add_modal=true" size="lg" class="p-2" >
                  <b-icon icon="plus-square-fill" aria-hidden="true" ></b-icon>
                  Add Blog
                </b-button>
            </div>
            <div class="col-sm-2">
              <b-button   @click="export_blogs" size="lg" class="p-2" >
                  <b-icon icon="upload" aria-hidden="true" ></b-icon>
                  Export
                </b-button>
            </div>
            <div class="col-sm-2">
              <b-button   @click="show_import_modal=true" size="lg" class="p-2" >
                  <b-icon icon="download" aria-hidden="true" ></b-icon>
                  Import
                </b-button>
            </div>
          </div>
         
          
          <br>
       
          <div class="row justify-content-right d-flex">
            <div v-for="blog in user.blogs" 
            :key="blog['.blog_id']"
            >
                <BlogDisplay
                :blog="blog"
                :id="user.id"
                :author="user.username"
                class="m-3"
                />

                <div>
                <b-button class="btn m-2"  variant="primary" 
                @click="show_edit_modal=true;
                        selected_blog=blog" 
                    >
                    Edit
                </b-button>
                <b-button class="btn m-2" variant="danger" 
                    @click="show_delete_modal=true;selected_blog.blog_id=blog.blog_id" 
                    >
                    Delete
                </b-button>
                <b-button class="btn m-2" variant="secondary" 
                    @click="export_single_blog(blog.blog_id)" 
                    >
                    Export
                </b-button>
                </div>
            </div>
          </div>
        </div>
      </div>
      <!--Blog Display Completed-->
      <!--Modals-->
      <b-modal v-model="show_alert_modal" id="alert_modal" ok-only size="sm" title="">
        Your blogs have been exported and mailed successfully
      </b-modal>

      <b-modal  v-model="show_delete_modal" id="delete_modal" size="lg"  centered title="Delete Blog">
        <h5>
          Are you sure you want to delete this blog?
        </h5>
        <template #modal-footer>
          <div class="w-100">
            
           <b-button
                variant="primary"
                class="btn-lg float-right m-3"
                @click="delete_blog()"
              >
                Yes
              </b-button>
              <b-button
                variant="secondary "
                class="btn-lg float-right m-3 "
                @click="show_delete_modal=false"
              >
                No
              </b-button>
            </div>
        </template>
      </b-modal>
      <b-modal  v-model="show_import_modal" id="import_modal" size="lg"  centered title="Import Blogs">
       <b-form >
          Upload a zip file containing blog images and CSV file for blog data
          <br>
            <b-form-file class="data_entry"
                    @change="onZipFileUpload"
                    :state="Boolean(import_modal.zip_file)"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
                    required
           ></b-form-file>
          
        </b-form> 
        <template #modal-footer>
          <div class="w-100">
            
           <b-button
                variant="primary"
                class="btn-lg float-right "
                @click="import_blogs"
              >
                Import
              </b-button>
            </div>
        </template>
      </b-modal>
      <b-modal  v-model="show_add_modal" id="add_modal" size="lg"  centered title="Add Blog">
       <b-form >
            <b-form-input v-model="add_form.blog_name" 
            class="data_entry"
            placeholder="Enter Blog Title"
            required>
            </b-form-input>
            <b-form-textarea
                    id="textarea"
                    class="data_entry"
                    v-model="add_form.description"
                    placeholder="Enter description"
                    rows="3"
                    max-rows="6"
                    required
            ></b-form-textarea>
            <b-form-file class="data_entry"
                   
                    @change="onFileUpload"
                    :state="Boolean(add_form.image_loc)"
                    placeholder="Choose a file or drop it here..."
                    drop-placeholder="Drop file here..."
           ></b-form-file>
          
        </b-form> 
        <template #modal-footer>
          <div class="w-100">
            
           <b-button
                variant="primary"
                class="btn-lg float-right "
                @click="add_blog"
              >
                Save
              </b-button>
            </div>
        </template>
      </b-modal>
      <b-modal  v-model="show_edit_modal" id="edit_modal" size="lg"  centered title="Edit Blog">
       <b-form >
            <b-form-input v-model="selected_blog.blog_name" 
            class="data_entry"
            :placeholder="selected_blog.blog_name"></b-form-input>
            <b-form-textarea
                    id="textarea"
                    class="data_entry"
                    v-model="selected_blog.description"
                    :placeholder="selected_blog.description"
                    rows="3"
                    max-rows="6"
            ></b-form-textarea>
          
        </b-form> 
        <template #modal-footer>
          <div class="w-100">
            
           <b-button
                variant="primary"
                class="btn-lg float-right "
                @click="edit_blog"
              >
                Save
              </b-button>
            </div>
        </template>

      </b-modal>
      <!--Modals Completed-->
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import BlogDisplay from '@/components/BlogDisplayComponent.vue'

  export default {
    name: 'BlogView',
      
    data(){
      return {
        user:Object,
        show_add_modal: false,
        show_edit_modal: false,
        show_delete_modal: false,
        show_alert_modal: false,
        show_import_modal: false,
        error_msg:null,
        selected_blog:{
          blog_id:"",
          blog_name: "",
          description: "",
          image_loc: null
        },
        import_modal:{
          zip_file:null,
          user_id:null
        },
        add_form:{
          user_id:"",
          blog_name: "",
          description: "",
          image_loc: null
        }
      }
    },
    components: {
      BlogDisplay
    },
    methods:{
      
        onFileUpload (event) {
          this.add_form.image_loc= event.target.files[0]
        }, 
        onZipFileUpload (event) {
          this.import_modal.zip_file= event.target.files[0]
        },
        export_single_blog:async function(blog_id){
          await axios({
                  method: 'get',
                  url: 'http://127.0.0.1:5000/export_blog/'+localStorage.getItem("user_id")+'/'+blog_id,
                  responseType: 'blob',
                  headers:{
                    'Authentication-Token': localStorage.getItem("token"),
                   }
                }).then((response) => {
                  var fileURL = window.URL.createObjectURL(new Blob([response.data],
                   {type:  'application/pdf'}));
                  var fileLink = document.createElement('a');
                  fileLink.href = fileURL;
                  fileLink.setAttribute('download', 'file.pdf');
                  document.body.appendChild(fileLink);
                  fileLink.click();
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })
        },
        export_blogs:async function(){
           axios({
                  method: 'get',
                  url: 'http://127.0.0.1:5000/get_report/'+localStorage.getItem("user_id"),
                  responseType: 'blob',
                  headers:{
                    'Authentication-Token': localStorage.getItem("token"),
                   }
                }).then((response) => {
                  /*var fileURL = window.URL.createObjectURL(new Blob([response.data],
                   {type:  'application/csv'}));
                  var fileLink = document.createElement('a');
                  fileLink.href = fileURL;
                  fileLink.setAttribute('download', 'file.csv');
                  document.body.appendChild(fileLink);
                  fileLink.click();*/
                  console.log(response)
                  this.show_alert_modal=true;
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })
        },
      edit_blog:function(){
        console.log("edit")
        console.log(this.selected_blog)
        axios.put('http://127.0.0.1:5000/api/blogs',
                {     
                  
                    blog_id: this.selected_blog.blog_id,
                    blog_name: this.selected_blog.blog_name,
                    description: this.selected_blog.description
                 
                },
                { 
                  headers:{
                  'Content-Type': 'application/json',
                  'Authentication-Token': localStorage.getItem("token")
                   }
                })
                 .then((res) => {
                     //Perform Success Action
                     console.log(res)
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })

        this.get_user_blogs()
        this.show_edit_modal=false
      },
      delete_blog:async function(){
        console.log(this.selected_blog.blog_id)
        await axios.delete('http://127.0.0.1:5000/api/blogs/'+localStorage.getItem("user_id")+'/'+this.selected_blog.blog_id,{
                  headers:{
                  'Content-Type': 'multipart/form-data',
                  'Authentication-Token': localStorage.getItem("token")
                   }
                })
                 .then((res) => {
                     //Perform Success Action
                     console.log(res)
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })

        this.get_user_blogs()
        this.show_delete_modal=false
        console.log("delete")

        this.$forceUpdate();
      },
      get_user_blogs: async function(){
       
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
            this.user=this.$store.state.user;
        
      },
      add_blog:function(){
        console.log("add")
        this.add_form.user_id=this.user.id;
        if(this.add_form.blog_name.length > 0 && this.add_form.description.length > 0 && this.add_form.image_loc){

        axios.post('http://127.0.0.1:5000/add_blog', this.add_form,{
                  headers:{
                  'Content-Type': 'multipart/form-data',
                  'Authentication-Token': localStorage.getItem("token")
                   }
                })
                 .then((res) => {
                     //Perform Success Action
                     console.log(res)
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })

        this.get_user_blogs()
        this.add_form.description="";
        this.add_form.image_loc=null;
        this.add_form.blog_name="";
        this.show_add_modal=false;
        this.get_user_blogs();
        }
        
      },
      import_blogs: async function(){
        console.log("import blogs")
        this.import_modal.user_id=this.user.id;
        axios.post('http://127.0.0.1:5000/import_blogs', this.import_modal,{
                  headers:{
                  'Content-Type': 'multipart/form-data',
                  'Authentication-Token': localStorage.getItem("token")
                   }
                })
                 .then((res) => {
                     //Perform Success Action
                     console.log(res)
                     this.get_user_blogs();
        
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                     console.log(error)
                 })

        this.zip_loc=null;
       
        this.show_import_modal=false;
      }
  
    },
    beforeMount: async function(){
      console.log("Befor mount")
      await this.get_user_blogs()
    },
    mounted: function() {
      var source = new EventSource("http://localhost:5000/stream");
      source.addEventListener('greeting', event => {
          let data = JSON.parse(event.data);
          console.log(data.message)
      }, false);
    } 
  }
  </script>
  
  <style scoped>
    .blog_view{
      margin:20px;
  
    }
    .data_entry{
      margin-top: 5px;
    }
  
  </style>
  