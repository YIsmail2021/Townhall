<template>
    <div class="home">
      <section class="hero is-medium is-dark mb-6">
        <div class="hero-body has-text-centered">
          <p class="title mb-6">
            Welcome to Townhall
          </p>
          <p class="subtitle">
            A rambling site
          </p>
        </div>
      </section>
      
      <div class="columns-is-multine">
        <div class="column is-12">
          <h2 class="is-size-2 has-text-centered">Posts in {{ categoryName }}</h2>
        </div>
  
        <div
          class="column is-full"
          v-for="post in listPosts"
          v-bind:key="post.id">
          <div class="box">
            <h3 class="is-size-5 has-text-centered">{{ post.title }}</h3>
            <p class="is-size-6 has-text-grey has-text-right mb-5">User: {{ post.author_id }}</p>
            <p class="is-size-6 has-text-grey has-text-centered mb-5">{{ post.body }}</p>
            <router-link :to="{ name: 'post', params: { postId: post.id } }" class="is-size-6 mb-5 is-flex" style="justify-content: center;">View details</router-link>
            <p class="is-size-6 has-text-grey has-text-right has-text-weight-light">{{ post.humanize_created_on }}</p>
          </div>
        </div>
  
      </div>
  
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export default {
    name: 'listPostsView',
    data() {
      return {
        listPosts: []
      }
    },
    watch: {
      // Watch the route query change and refetch posts when category changes
      '$route.query.category': function (newCategory) {
        this.getListPosts(newCategory);
      }
    },
    mounted() {
      this.categoryName = this.$route.query.categoryName,
      // Fetch posts when the component is mounted
      this.getListPosts(this.$route.query.category);
    },
    methods: {
      getListPosts() {
        const category = this.$route.query.category;
        let url = '/api/v1/post/';
        
        // Check if there's a category query parameter
        if (category) {
          url += `?category=${category}`;
        }
        
        axios
          .get(url)
          .then(response => {
            this.listPosts = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    }

  }
</script>

<style scoped>
  .image {
    margin-top: -1.25rem;
    margin-left: 1.25rem;
    margin-right: -1.25rem;
  }
</style>
  