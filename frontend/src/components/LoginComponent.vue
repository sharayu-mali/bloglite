<template>
  <div id="form"  class="container-fluid align-items-center m">
    <b-card  class="text-center " title="Login">
        
      <b-form action="#">

        <b-form-group
          label="Enter Username:"
          label-for="username"
        >
          <b-form-input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter username"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Enter Password:"
          label-for="password"
        >
          <b-form-input
            id="password"
            v-model="password"
            type="password"
            placeholder="********"
            required
          ></b-form-input>
        </b-form-group>
        
        <b-button class="btn btn-lg m-3" variant="primary" type="submit" @click.prevent="login">
          Login
        </b-button >
        <br>
        <router-link :to="`/register`">Don't have an account? Register here</router-link>
       
      </b-form>
      <br>
        <p v-if="errors.length">
          <ul>
            <p class="text-danger" v-for="error in errors" :key="error">{{ error }}</p>
          </ul>
        </p>
   </b-card>
  </div>

</template>
  
  <script>
  export default {
    name: "LoginComponent",
    data() {
      return {
        errors:[],
        username:"",
        password: "",
        incorrect: false,
        animate: false,
      };
    },
    methods: {
      checkForm: function () {
          this.errors = [];

          if (!this.username) {
            this.errors.push("UserName is required.");
          }else if (this.username.length<4 || this.username.length>30) {
            this.errors.push("Username should have 4 to 30 characters");
          }else if (!this.password) {
            this.errors.push('Password is required.');
          } else if (this.password.length < 8 ) {
            this.errors.push('Password should have at least 8 characters');
          }
          if (!this.errors.length) {
            return true;
          }

        },
      async login() {
        // Check if the user has filled in the email and password
        if (this.checkForm()) {
          try {
              fetch('http://127.0.0.1:5000/login_user', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  "username":this.username, 
                  "password": this.password}),
              })
              .then(response => response.json())
              .then(data => {
                if(data.status_code==200){
                  //this.$store.commit('setuser',this.username);
                  console.log(data);
                  localStorage.token=data.token
                  localStorage.user_id=data.user_id
                  this.$router.push("/");
                }else{
                  console.log('Error:', data);
                  this.errors.push(data["message"])
                   
                }
               
               
              })
              .catch((error) => {
                console.error('Error:', error);
                this.savedIconClass = "text-danger";
              });
          } catch (e) {
            console.log(e);
            this.incorrect = true;
          }
        }
      },
      async register() {
        this.push('/register')
      }
    },
  };
  </script>
  <style scoped>
   #form{
    width: 50%;
    margin-top:5%;
    box-shadow: 0.3em 0.3em 1em rgba(0, 0, 0, 0.3);
    padding: 30px;
   }
  </style>
  
  
  