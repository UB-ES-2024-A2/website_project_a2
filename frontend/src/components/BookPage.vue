<template>
  <div id="main-page" class="main-page">
    <div v-if="type === 'book'">
      Book page info for {{ textInput }}
    </div>
    <div v-else>
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading user information...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="user" class="book-content">
        <div class="container">
          <div class="profile row">
            <div class="col-md-8 d-flex flex-column">
              <h2 class="book-title">My books</h2>
            </div>
            <div class="col-md-4 text-center d-flex flex-column align-items-center justify-content-center">
              <img src="@/assets/user-black.svg" alt="User Photo" class="img-fluid rounded-circle shadow" style="width: 150px; height: 150px;">
              <p><strong>Name:</strong> {{ user.name }} {{ user.surname }}</p>
              <p><strong>Username:</strong> {{ user.username }}</p>
              <p><strong>Email:</strong> {{ user.email }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-data">No book data available</div>
    </div>
  </div>
</template>

<script>
import UserService from '../services/UserService'

export default {
  name: 'BookPage',
  data () {
    return {
      user: null,
      textInput: '',
      type: '',
      loading: false,
      error: null
    }
  },
  props: {
    searchResults: Array
  },
  watch: {
    '$route.query': {
      handler () {
        let textInput = this.$route.query.search || ''
        let type = this.$route.query.type || ''
        let id = this.$route.query.id || ''
        if (textInput !== '' && type !== '') {
          this.textInput = textInput
          this.type = type
          if (type === 'user' && id) {
            this.fetchBook(id)
          }
        }
      },
      immediate: true
    }
  },
  methods: {
    fetchBook (id) {
      this.loading = true
      this.error = null
      UserService.readUserById(id)
        .then(response => {
          this.user = response.data
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching user:', error)
          this.error = 'Failed to load user data'
          this.loading = false
        })
    }
  },
  mounted () {
    const token = this.$store.getters.token

    if (!token) {
      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
.main-page {
  grid-area: main-page;
  padding: calc(var(--panel-gap) * 2);
  background-color: var(--box-background-color);
  color: var(--text-color);
  border-radius: calc(var(--border-radius) * 2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-page-wrap {
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .error, .no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  font-size: var(--font-size-medium);
}

.spinner {
  border: 4px solid var(--half-transparent-background);
  border-top: 4px solid var(--purple-background);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: var(--panel-gap);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.book-content {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.book-header {
  display: flex;
  gap: calc(var(--panel-gap) * 4);
  margin-bottom: calc(var(--panel-gap) * 4);
}

.book-cover {
  flex-shrink: 0;
}

.book-image {
  width: 300px;
  height: auto;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.book-image:hover {
  transform: scale(1.05);
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: var(--panel-gap);
}

.book-title {
  font-size: var(--font-size-title);
  margin-bottom: 0;
}

.book-author {
  font-size: var(--font-size-medium);
  color: var(--text-color-secundary);
}

.book-meta {
  display: flex;
  flex-wrap: wrap;
  gap: calc(var(--panel-gap) * 2);
  font-size: var(--font-size-xs);
}

.book-meta-item {
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) / 2) var(--panel-gap);
  border-radius: var(--border-radius);
}

.stars {
  color: var(--purple-background);
}

.star-empty {
  color: var(--text-color-secundary);
}

.book-synopsis {
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  margin-top: var(--panel-gap);
}
.profile {
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  margin-top: var(--panel-gap);
  min-height: 60vh;
  min-width: 170vh;
}
.buy-button {
  align-self: flex-start;
  background-color: var(--purple-background);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: var(--panel-gap);
}

.buy-button:hover {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

h2 {
  font-size: var(--font-size-medium);
  margin-bottom: var(--panel-gap);
  color: var(--purple-background);
}

@media (max-width: 768px) {
  .book-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .book-info {
    align-items: center;
  }

  .buy-button {
    align-self: center;
  }
}
</style>
