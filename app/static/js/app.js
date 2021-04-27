/* Add your Application JavaScript */



const app = Vue.createApp({
  data() {
    return {
      
      
    }
  }
});


const login = {
    name: 'Login',
    template: `
        <div class="center-form m-6 login">
            <h2 class="text-center mb-4">Login to your account</h2>
            <form @submit.prevent="login()" method="POST" class="form center-form " action="" id="loginform" >
                <div class="mt-sm-1 mb-sm-1">
                    <label class="" for="username">Username</label><br>
                    <input type="text" class="form-control form-field login-field" name="username" required>
                </div>
                <div class="mt-sm-3 mb-sm-1">
                    <label class="" for="biography">Password</label><br>
                    <input type="password" class="form-control form-field login-field" name="password" required>
                </div>
                <button type="submit" name="submit" class="btn bg-success   btn-block text-white mt-sm-3 mb-sm-1 login-field">Login</button>
            </form>
        </div>
    `,
    data() {
        return {}
    },
    methods: {
        login() {
            let self = this;
            let loginform = document.getElementById('loginform');
            let formd = new FormData(loginform);
  
            fetch("/api/auth/login", {
                method: 'POST',
                body: formd,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'        
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(jsonResponse) {
                
                if(jsonResponse.errors==undefined){
                    if(jsonResponse.token !== null) {
  
                        let jwt_token = jsonResponse.data.token;
  
                        let id = jsonResponse.data.id;
  
                        localStorage.setItem('token', jwt_token);
                        localStorage.setItem('current_user', id);
                        router.push('/profile');
                        //this.$alert(jsonResponse.data.message);
                        swal({title: "Login",text: jsonResponse.data.message,icon: "success",button: "OK!"});
                    }
                }else{
                    //this.$alert(jsonResponse.data.message, " try again");
                   swal({title: "Logged In",text: jsonResponse.errors[0],icon: "error",button: "Try Again!"});  
                }
  
            })
            .catch(function(error) {
                console.log(error);
            });
    
        }
    }
  };
  
const logout = {
    name: 'Logout',
    template: `
    <button @click="logout" class="btn btn-success  text-white" type="button">Log out?</button>
    `
      ,
   
    logout() {
        fetch("api/auth/logout", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token,
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            credentials: 'same-origin'
        })
        .then(function(response){
          return response.json();
          swal({title: "Logged Out",text: jsonResponse.data.message,icon: "success",button: "OK!"});
            router.push('/login');
        })
        .then(function(jsonResponse){
            localStorage.removeItem('token');
            localStorage.removeItem('current_user');
            
            
        })
        .catch(function(error){
          console.log(error);
        });
    },
    methods: {
        logout(){
            this.$router.push({ path: '/login' });
        }}
  };

  
const home = {
  name: 'Home',
  template: `
      <div class="d-flex align-items-center home-div col-md-10">
          <div class="row align-items-center col-md-5 intro">
              <h1 class="font-weight-bold">Buy and Sell Cars Online</h1>
              <p class="text-secondary">United Auto Sales provides the fastest, easiest and most user friendly way to buy or sell cars online. Find a Great Price on the Vehicle You Want</p>
              <div class="flex-area ">
                  <button @click="reg" class="btn bg-primary text-white" type="button">Resister</button>
                  <button @click="login" class="btn btn-success  text-white" type="button">Login</button>
                  
              </div>
          </div>
          <div >
              <img class="" src="static/images/hompage.jpg">
          </div>
      </div>
  `,
  data() {
      return {}
  }, 
  methods: {
      reg(){
          this.$router.push({ path: '/register' });
      },
        login() {
          this.$router.push({ path: '/login' });
      }
    
  },
};

const register = {
  name: 'Register',
  template: `
      <div class="maincontainer">
      <div class="register m-6">
          <h1 class="mb-4">Register New User</h1>
          <form @submit.prevent="register()" method="POST" class="form" action="" id="registerform" >
              <div class="d-flex flex-area1  mt-sm-1 mb-sm-1">
                  <div>
                      <label class="" for="username">Username</label><br>
                      <input type="text" class="form-control form-field" name="username" required>
                  </div>
                  <div>
                      <label class="" for="password">Password</label><br>
                      <input type="password" class="form-control form-field" name="password" required>
                  </div>
              </div>
              <div class="d-flex flex-area1 mt-sm-3 mb-sm-1">
                  <div>
                      <label class="" for="name">Fullname</label><br>
                      <input type="text" class="form-control form-field" name="name" required>
                  </div>
                  <div>
                      <label class="" for="email">Email</label><br>
                      <input type="email" class="form-control form-field" name="email" required>
                  </div>
              </div>
              <div class="mt-sm-3 mb-sm-1">
                  <label class="" for="location">Location</label><br>
                  <input type="text" class="form-control form-field" name="location" required>
              </div>
              <div class="mt-sm-3">
                  <label class="" for="biography">Biography</label><br>
                  <textarea name="biography" class="form-control" required></textarea><br>
              </div>
              <div class="">
                  <label class="" for="photo">Upload Photo</label><br>
                  <input type="file" class="form-control form-field" name="photo" accept=".jpeg, .jpg, .png">
              </div>
              <button type="submit" name="submit" class="btn bg-success text-white mt-sm-3 mb-sm-1">Register</button>
          </form>
      </div>
      </div>
  `,
  data() {
      return {
          
      };
  },
  methods: {
      register() {
          let self=this;
          let registerform=document.getElementById('registerform');
          let formd = new FormData(registerform);
          fetch("/api/register", {
              method: 'POST',
              body: formd,
              headers: {
                  'X-CSRFToken': token
              },
              credentials: 'same-origin'        
          })
          .then(function(response) {
              return response.json();
          })
          .then(function(jsonResponse) {
              console.log(jsonResponse)
              if(jsonResponse.errors==undefined){
                  router.push('/login');
                
                  //flash("User  was successfully registered", 'success')
                  swal({title: "Registeration",text: "User  was successfully registered!",icon: "success",button: "OK!"});
              }else{
                  swal({title: "Registeration",text: jsonResponse.errors[0],icon: "error",button: "Try Again!"});
              }
          })
          .catch(function(error) {
              console.log(error);
          });
      }
  }
};

const profile = {
    name: 'Profile',
    template: `
        <div class="container ">
            <div id="displayfav">

                
        
                        <img class="favcar" id="round" src="./uploads/{{userdata.photo}}">
      
                        <h2 id="profile-name">{{userdata.name}}</h2>
                        <h4 class="graytext">@<span>{{userdata.username}}</span></h4>
                        <p class="graytext">{{userdata.biography}}</p>
                            
                                <p class="profile-user-info graytext">Email     {{userdata.email}}</p>
                                <p class="profile-user-info graytext">Location     {{userdata.location}}</p>
                                <p class="profile-user-info graytext">Joined     {{userdata.date_joined}}</p>
                           
                        
                
            </div>

            <div class="carsfavtext"><h1>Cars Favourited</h1></div>

               
                    <div v-for="cars in carlist.slice(0, 3)">
                        <div class="card" style="width: 18rem;">
                            <img class="card-img-top favcar"  :src="./uploads/{{carlist.photo}}">
                                <div class="name-model-price">
                                    <div class="name-model">
                                        <span  class="car-name">{{carlist.year.concat(" ",carlist.make)}}</span>
                                        <span class="graytext">{{carlist.model}}</span>
                                    </div>
                                    <a href="#" class="btn btn-success card-price-btn">
                                        <img class="icons" src='/static/images/tagicon.png'>
                                        <span><span>$</span>{{carlist.price}}</span>
                                    </a>
                                </div>
                                <a :href="carlist.id" class="btn btn-primary card-view-btn" @click="favcar">View more details</a>
                        </div>
                    </div>
            </div>
        </div>  
    `, 
    created() {
        let self=this;
        fetch("/api/users/"+ localStorage.getItem('current_user'), {
                method: 'GET',
                headers: {
                    'X-CSRFToken': token,
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'        
            })

            .then(function(response) {
                return response.json();
            })
            .then(function(jsonResponse) {
                self.userdata = jsonResponse.data;})
                
            .catch(function(error) {
                console.log(error);
            });      
            fetch("/api/users/"+ localStorage.getItem('current_user') + "/favourites", {
                method: 'GET',
                headers: {
                    'X-CSRFToken': token,
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'        
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(jsonResponse) {
                self.carlist = jsonResponse.data;
            })
            .catch(function(error) {
                console.log(error);
            });
        
    },
    methods:{
        favcar: function(event) {
            event.preventDefault();
            let carid=event.target.getAttribute("href");
            router.push({ name: 'details', params: { id: carid}}); 
        }
    },
    data() {
        return {
            carlist: [],
            userdata: [],
            host:window.location.protocol + "//" + window.location.host
        }
    }
};

app.component('app-header', {
  name: 'AppHeader',
  template: `
      <header>
          <nav class="navbar navbar-expand-lg navbar-dark fixed-top justify-content-between">
                <a class="navbar-brand" href="/"><img src="static/images/sports-car.svg"/>United Auto Sales</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                 </button>

            <div class="right collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                <router-link to="/register" class="nav-link">Register</router-link>
                </li>
                <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
                </li>
                <li class="nav-item">
                <router-link to="/profile" class="nav-link">My Profile</router-link>
                </li> <li class="nav-item">
                <router-link to="/logout" class="nav-link">Logout</router-link>
                </li>
              </ul>
            </div>
          </nav>
      </header>    
  `,
  data: function() {
    return {};
  }
});

app.component('app-footer', {
  name: 'AppFooter',
  template: `
      <footer>
          <div class="container">
              <p>Copyright &copy {{ year }} Flask Inc.</p>
          </div>
      </footer>
  `,
  data() {
      return {
          year: (new Date).getFullYear()
      }
  }
})

const NotFound = {
    name: 'NotFound',
    template: `
    <div>
        <h1>404 - Page Not Found</h1>
    </div>
    `,
    data() {
        return {}
    }
};

const routes = [
  { path: "/", component: home },
  { path: "/register", component: register },
  { path: "/login", component:login },
  { path: "/logout", component: logout },
  {path: "/profile", component: profile},
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

  
const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
  });

app.use(router)
app.mount('#app');
