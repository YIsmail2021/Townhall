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

    <!-- Displayed in a grid using Bulma CSS-->
    <div class="columns is-multiline">
      <div class="column is-one-quarter" v-for="category in listCategories" v-bind:key="category.id">
        <div class="box">
          <div class="columns">
            <div class="column">
              <router-link 
                :to="{ name: 'list-posts', query: { category: category.id, categoryName: category.name } }" 
                class="has-text-centered is-size-5"
              >
                {{ category.name }}
              </router-link>
            </div>
            <div class="column is-narrow">
              <button 
                @click="deleteCategory(category.id)" 
                class="button is-danger is-small">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'categoryView',
  data() {
    return {
      listCategories: [],
    }
  },
  mounted() {
    this.getListCategories(); // Fetch categories when component is mounted
  },
  methods: {
    // Fetch categories
    getListCategories() {
      const url = `/api/v1/category/`;
      axios
        .get(url)
        .then(response => {
          this.listCategories = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    
    // Delete category by ID
    deleteCategory(categoryId) {
      const url = `/api/v1/category/${categoryId}/`;
      axios
        .delete(url)
        .then(response => {
          console.log('Category deleted:', response.data);
          this.getListCategories();  // Refresh the list after deletion
        })
        .catch(error => {
          console.log('Error deleting category:', error);
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
