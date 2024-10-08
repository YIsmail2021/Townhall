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
        <h2 class="is-size-2 has-text-centered">{{ postDetails.title }}</h2>
      </div>

      <div class="column is-full">
        <div class="box">
          <p class="is-size-6 has-text-right mb-5">User: {{ postDetails.author_id }}</p>
          <p class="is-size-6 has-text-grey has-text-centered mb-2">{{ postDetails.body }}</p>
          <!-- Display Image if it exists -->
          <div v-if="postDetails.image" style="text-align: center;">
            <img :src="postDetails.image" alt="Post Image" style="max-width: 100%; height: auto;">
          </div>
          <p class="is-size-6 has-text-grey has-text-right has-text-weight-light">{{ postDetails.humanize_created_on }}</p>
        </div>
      </div>

      <div
        class="column is-full"
        v-for="comment in listPostComments"
        v-bind:key="comment.id">
        <div class="box">
          <p class="is-size-6 has-text-grey has-text-right mb-5">User: {{ comment.author_id }}</p>
          <p class="is-size-6 has-text-grey has-text-centered mb-2">{{ comment.body }}</p>
          <p class="is-size-6 has-text-grey has-text-right has-text-weight-light">{{ comment.humanize_created_on }}</p>
        </div>
      </div>

      <div class="column is-full">
        <div class="box">
          <textarea v-model="commentBody" class="textarea" placeholder="Enter your comment"></textarea>
          <button @click="submitComment" class="button is-primary">Submit</button>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'postView',
  data() {
    return {
      postDetails: {},
      listPostComments: []
    }
  },
  components: {
  },
  mounted() {
    this.getPostDetails()
    this.getPostCommentsList()
  },
  // Get Post info
  methods: {
    getPostDetails() {
      const postId = this.$route.params.postId;
      
      // Construct the correct URL to fetch post details by its ID
      let url = `/api/v1/post/${postId}/`;

      axios
        .get(url)
        .then(response => {
          this.postDetails = response.data;
        })
        .catch(error => {
          console.log('Error fetching post details:', error);
        });
      },
    // Get comments from the post.
    getPostCommentsList() {
      // Get params
      const postId = this.$route.params.postId;
      const url = `/api/v1/post-comments/${postId}/`;
      axios
        .get(url)
        .then(response => {
          this.listPostComments = response.data;
        })
        .catch(error => {
          console.log('Error fetching comments', error);
        });
    },
    // Create a new comment.
    submitComment() {
      const postData = {
        post: this.$route.params.postId,
        body: this.commentBody,

      };
      axios
        .post('/api/v1/comments/', postData)
        .then(response => {
          console.log('Comment submitted successfully:', response.data);
          this.commentBody = '';
          window.location.reload();
        })
        .catch(error => {
          console.error('Error submitting comment:', error);
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
