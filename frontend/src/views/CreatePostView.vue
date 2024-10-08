<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Welcome to Townhall</p>
        <p class="subtitle">A rambling site</p>
      </div>
    </section>

    <div class="columns-is-multiline">
      <div class="column is-full">
        <div class="box">
          <div class="field is-grouped">
            <div class="control is-expanded">
              <input v-model="postTitle" class="input" type="text" placeholder="Enter your Title" />
            </div>
            <div class="control">
              <select v-model="postCategory" class="select">
                <option disabled value="">Select a category</option>
                <option v-for="category in listCategories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-full">
        <div class="box">
          <textarea v-model="postBody" class="textarea" placeholder="Enter your body"></textarea>

          <!-- File input for image -->
          <div class="field">
            <label class="label">Upload Image</label>
            <div class="control">
              <input type="file" @change="handleFileUpload" class="input" />
            </div>
          </div>

          <button @click="submitPost" class="button is-primary">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router/index'

export default {
  data() {
    return {
      postTitle: '',
      postBody: '',
      postCategory: '',
      imageFile: null, // Store image file
      listCategories: []
    }
  },
  mounted() {
    this.getlistCategories()
  },
  methods: {
    getlistCategories() {
      axios.get('/api/v1/category/')
        .then(response => {
          this.listCategories = response.data
        })
        .catch(error => {
          console.log('Error fetching categories:', error)
        })
    },
    handleFileUpload(event) {
      this.imageFile = event.target.files[0] // Capture the uploaded file
    },
    submitPost() {
      const formData = new FormData()
      formData.append('title', this.postTitle)
      formData.append('body', this.postBody)
      formData.append('category', this.postCategory)

      // Append the image file if it exists
      if (this.imageFile) {
        formData.append('image', this.imageFile)
      }

      axios.post('/api/v1/post/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log('Post submitted successfully:', response.data)
        this.postBody = ''
        router.push({ name: 'category' })
      })
      .catch(error => {
        console.error('Error submitting post:', error)
      })
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
