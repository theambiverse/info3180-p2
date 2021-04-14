/* Add your Application JavaScript */
const app = Vue.createApp({
  data() {
    return {
      
      welcome: 'Hello World! Welcome to VueJS',
      components: {
        'home': Home,
        'news-list': NewsList
        }
    }
  }
});


const Home = {
  name: 'Home',
  template: `
  _ADD CODE_
  `,
  data() {return {
  welcome: 'Hello World! Welcome to VueJS'
  }
  }
  };


app.component('app-header', {
  name: 'AppHeader',
  template: `
      <header>
          <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
            <a class="navbar-brand" href="#">United Auto Sales</a>
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
  data: function() {
      return {
          year: (new Date).getFullYear()
      }
  }
})

const NewsList ={
  name: 'Newslist', 
  template:

  `<div class="news">
  <h2>News</h2>
  <div class="form-inline d-flex justify-content-center">
<div class="form-group mx-sm-3 mb-2">
<label class="sr-only" for="search">Search</label>
<input type="search" name="search" v-model="searchTerm"
id="search" class="form-control mb-2 mr-sm-2" placeholder="Enter 
search term here" />
<p>You are searching for {{ searchTerm }}</p>
</div><button class="btn btn-primary mb-2"
@click="searchNews">Search</button>
</div>
  <ul class="news__list">
  <li v-for="article in articles"
class="news__item"> {{article.title }} <br> <img :src=article.urlToImage> <br> {{article.description}} </li>
  </ul>
  </div>
  `,
  created() {
    let self=this;
    fetch('https://newsapi.org/v2/top-headlines?country=us',
    {
      
    headers: {
      
    'Authorization': 'Bearer <toke>'
    }
    })
    .then(function(response) {
    return response.json();
    })
    .then(function(data) {
    console.log(data);
    self.articles=data.articles;
    });
    },
    data() {
    return {
    articles: [],
    searchTerm:''
    }
    },
    methods: {
    searchNews() {
    let self = this;
    fetch('https://newsapi.org/v2/everything?q='+
    self.searchTerm + '&language=en', {
    headers: {
    'Authorization': 'Bearer <token>'
    }
    })
    .then(function(response) {
    return response.json();
    })
    .then(function(data) {
    console.log(data);
    self.articles = data.articles;
    });
    }
    }

}

  
const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes: [
  { path: '/', component: Home },
  { path: '/news', component: NewsList }
  ]
  });

app.use(router)
app.mount('#app');