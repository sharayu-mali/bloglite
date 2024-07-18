<template>
    <div id="form"  class="container-fluid align-items-center m">
      <b-card  class="text-center " title="Registration">
        
        <b-form action="#">
  
          <b-form-group
            label="Username:"
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
            label="Email:"
            label-for="email"
          >
            <b-form-input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter email address"
              required
            ></b-form-input>
          </b-form-group>
          <b-form-group
            label="password:"
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
          
          <b-button class="btn btn-lg m-3" variant="primary" type="submit" @click="register">
            Register
          </b-button >
          
          <br>
          
        <router-link :to="`/login`">Already have an account? Login here</router-link>
       
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
      name: "RegisterComponent",
     
      data() {
        return {
          errors: [],
          username:"",
          email:"",
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
          }
          if (!this.email) {
            this.errors.push('Email is required.');
          } else if (!this.validEmail(this.email)) {
            this.errors.push('Invalid email');
          }else if (!this.password) {
            this.errors.push('Password is required.');
          } else if (this.password.length < 8 ) {
            this.errors.push('Password should have at least 8 characters');
          }
          if (!this.errors.length) {
            return true;
          }

        },
    validEmail: function (email) {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
        async register() {
          // Check if the user has filled in the email and password
          if (this.checkForm()) {
           try {
                fetch('http://127.0.0.1:5000/register_user', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    "username":this.username,
                    "email": this.email, 
                    "password": this.password}),
                })
                .then(response => response.json())
                .then(data => {
                  if(data["code"]){
                    this.errors.push(data["description"])
                  }else{
                  this.$router.push("/");

                  }
                })
                .catch((error) => {
                  console.error('Error:', error);
                  this.errors.push(error)
                });
            } catch (e) {
              console.log(e);
              this.incorrect = true;
            }
            
          }
        },
        async login() {
        this.push('/login')
      }
      },
      mounted() {
       if(localStorage.getItem("token")) {
          this.$router.push('/');
        }
      }
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
    