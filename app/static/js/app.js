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
                        router.push('/explore');
  
                        swal({title: "Login",text: jsonResponse.data.message,icon: "success",button: "OK!"});
                    }
                }else{
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
    <h1 class="mt-sm-2">Logging out...</h1>
    `,
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
        })
        .then(function(jsonResponse){
            localStorage.removeItem('token');
            localStorage.removeItem('current_user');
            router.push('/');
        })
        .catch(function(error){
          console.log(error);
        });
    }
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
      reg: function() {
          this.$router.push({ path: '/register' });
      },
        login: function() {
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



app.component('app-header', {
  name: 'AppHeader',
  template: `
      <header>
          <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
            <a class="navbar-brand" href="/">United Auto Sales</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                <router-link to="/register" class="nav-link">Register</router-link>
                </li>
                <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
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
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

  
const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
  });

app.use(router)
app.mount('#app');