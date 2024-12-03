<template>
  <div id="main-page" class="main-page">
    <div v-if="type === 'book'" class="book-page-wrap">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading book information...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="book" class="book-content">
        <div class="book-header">
          <div class="book-cover">
            <img :src="book.image" :alt="book.title + ' cover'" class="book-image">
          </div>
          <div class="book-info">
            <h1 class="book-title">{{ book.title }}</h1>
            <p class="book-author">by {{ book.authors }}</p>
            <div class="book-meta">
              <span class="book-meta-item">{{ book.genres }}</span>
              <span class="book-meta-item">
                <span class="stars">
                  <span v-for="i in 5" :key="i" :class="{'star-filled': i <= book.rating, 'star-empty': i > book.rating}">★</span>
                </span>
                {{ book.rating }}/5
              </span>
              <span class="book-meta-item">Published: {{ formatDate(book.publication_date) }}</span>
              <span class="book-meta-item">Editorial: {{ book.editorial }}</span>
            </div>
            <div class="book-synopsis">
              <h2>Synopsis</h2>
              <p>{{ book.synopsis }}</p>
            </div>
            <a :href="book.buy_link" target="_blank" rel="noopener noreferrer" class="buy-button">Buy Now</a>
          </div>
        </div>

        <!-- Updated Comments section -->
        <div class="comments-section">
          <h2>Reader Reviews</h2>
          <button @click="showReviewForm = true" class="leave-review-button">Leave a Review</button>

          <!-- Review Form -->
          <div v-if="showReviewForm" class="review-form">
            <h3>Write Your Review</h3>
            <div class="rating-input">
              <span v-for="star in 5" :key="star" @click="newReview.rating = star" class="star-input" :class="{'star-filled': star <= newReview.rating}">★</span>
            </div>
            <textarea v-model="newReview.comment" maxlength="250" placeholder="Write your review (max 250 characters)" class="review-textarea"></textarea>
            <div class="char-count">{{ newReview.comment.length }}/250</div>
            <button @click="cancelReview" class="cancel-review-button">Cancel</button>
            <button @click="submitReview" :disabled="!isReviewValid" class="submit-review-button">Submit Review</button>
            <div v-if="reviewError" class="error-message">{{ reviewError }}</div>
          </div>

          <div v-if="loadingComments" class="loading">
            <div class="spinner"></div>
            <p>Loading comments...</p>
          </div>
          <div v-else-if="commentsError" class="error">
            <p>{{ commentsError }}</p>
          </div>
          <div v-else-if="comments && comments.length > 0" class="comments-list">
            <div v-for="comment in comments" :key="comment.id_comment_rating" class="comment-card">
              <div class="comment-header">
                <div class="user-info">
                  <img src="@/assets/user-black.svg" alt="User avatar" class="user-avatar">
                  <span class="username">{{ comment.username }}</span>
                </div>
                <div class="rating">
                  <span class="stars">
                    <span v-for="i in 5" :key="i" :class="{'star-filled': i <= comment.rating, 'star-empty': i > comment.rating}">★</span>
                  </span>
                </div>
              </div>
              <p class="comment-text">{{ comment.comment }}</p>
            </div>
          </div>
          <div v-else class="no-comments">
            No reviews yet. Be the first to review this book!
          </div>
        </div>
      </div>
      <div v-else class="no-data">No book data available</div>
    </div>
    <div v-else class="user-page-wrap">
      Users page info for {{ textInput }}
    </div>
  </div>
</template>

<script>
import BookService from '../services/BookService'
import UserService from '../services/UserService'

export default {
  name: 'BookPage',
  data () {
    return {
      textInput: '',
      type: '',
      book: null,
      loading: false,
      error: null,
      comments: [],
      loadingComments: false,
      commentsError: null,
      showReviewForm: false,
      newReview: {
        rating: 0,
        comment: ''
      },
      reviewError: null,
      userId: null
    }
  },
  props: {
    searchResults: Array
  },
  computed: {
    isReviewValid () {
      return this.newReview.rating > 0 && this.newReview.comment.trim().length > 0
    }
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
          if (type === 'book' && id) {
            this.fetchBook(id)
            this.fetchComments(id)
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
      BookService.readBookById(id)
        .then(response => {
          this.book = response.data
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching book:', error)
          this.error = 'Failed to load book data'
          this.loading = false
        })
    },
    fetchComments (id) {
      this.loadingComments = true
      this.commentsError = null
      BookService.getCommentsRatings(id)
        .then(response => {
          this.comments = response.data.comments
          this.loadingComments = false
        })
        .catch(error => {
          console.error('Error fetching comments:', error)
          this.commentsError = 'Failed to load comments'
          this.loadingComments = false
        })
    },
    formatDate (dateString) {
      if (!dateString) return ''
      const options = {year: 'numeric', month: 'long', day: 'numeric'}
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    submitReview () {
      this.reviewError = null
      // Primero, verificamos si el usuario ya ha comentado
      BookService.getCommentsRatings(this.book.id_book)
        .then(commentsResponse => {
          const comments = commentsResponse.data.comments || []
          const userHasCommented = comments.some(
            comment => comment.user_id === this.userId
          )
          if (userHasCommented) {
            throw new Error('You have already submitted a review for this book.')
          }
          // Si el usuario no ha comentado, procedemos a crear el comentario
          return BookService.createCommentRating(
            this.book.id_book,
            this.userId,
            this.newReview.comment,
            this.newReview.rating
          )
        })
        .then(() => {
          this.showReviewForm = false
          this.newReview = {rating: 0, comment: ''}
          this.fetchComments(this.book.id_book)
          this.fetchBook(this.book.id_book)
        })
        .catch(error => {
          console.error('Error submitting review:', error)
          if (error.message === 'You have already submitted a review for this book.') {
            this.reviewError = error.message
          } else if (error.response) {
            this.reviewError = `Error ${error.response.status}: ${error.response.data.detail || 'Could not submit review'}`
          } else if (error.request) {
            this.reviewError = 'Did not get a response from the server. Please try again.'
          } else {
            this.reviewError = 'Error submitting review. Please try again later.'
          }
        })
    },
    cancelReview () {
      this.showReviewForm = false
      this.newReview = { rating: 0, comment: '' }
    }
  },
  mounted () {
    const username = this.$store.getters.username

    if (!username) {
      this.$router.push('/login')
    } else {
      // Obtenemos el ID del usuario al montar el componente
      UserService.readUserByEmail(username)
        .then(response => {
          this.userId = response.data.id_user
        })
        .catch(error => {
          console.error('Error fetching user ID:', error)
          // Manejar el error según sea necesario
        })
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
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.book-content {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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

/* Updated styles for comments section */
.comments-section {
  margin-top: calc(var(--panel-gap));
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--panel-gap);
  width: 50%;
  margin: 0 auto;
}

.comment-card {
  background-color: var(--half-transparent-background);
  border-radius: var(--border-radius);
  padding: calc(var(--panel-gap) * 1.25);
  margin-bottom: calc(var(--panel-gap) / 2);
  margin-top: calc(var(--panel-gap) / 2);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: calc(var(--panel-gap) / 2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: calc(var(--panel-gap) / 2);
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
}

.username {
  font-weight: bold;
  color: var(--text-color);
  margin-right: calc(var(--panel-gap) / 2);
}

.stars {
  display: inline-flex;
  align-items: center;
}

.comment-text {
  color: var(--text-color);
  line-height: 1.3;
  margin-top: calc(var(--panel-gap) / 2);
  font-size: var(--font-size-xs);
}

.no-comments {
  text-align: center;
  color: var(--text-color-secundary);
  padding: calc(var(--panel-gap) * 2);
  background-color: var(--half-transparent-background);
  border-radius: var(--border-radius);
}

.leave-review-button {
  background-color: var(--purple-background);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-bottom: var(--panel-gap);
}

.leave-review-button:hover {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

.review-form {
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  margin-bottom: var(--panel-gap);
  width: 50%;
  margin-left: auto;
  margin-right: auto;
}

.rating-input {
  font-size: 24px;
  margin-bottom: var(--panel-gap);
}

.star-input {
  cursor: pointer;
  color: var(--text-color-secundary);
}

.star-input.star-filled {
  color: var(--purple-background);
}

.review-textarea {
  width: 100%;
  height: 100px;
  padding: var(--panel-gap);
  border-radius: var(--border-radius);
  border: 1px solid var(--text-color-secundary);
  background-color: var(--box-background-color);
  color: var(--text-color);
  resize: vertical;
}

.char-count {
  text-align: right;
  color: var(--text-color-secundary);
  font-size: var(--font-size-xs);
  margin-top: calc(var(--panel-gap) / 2);
}

.submit-review-button {
  background-color: var(--purple-background);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: var(--panel-gap);
}

.submit-review-button:hover:not(:disabled) {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

.submit-review-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: #ff4d4d;
  margin-top: var(--panel-gap);
  font-size: var(--font-size-xs);
}

.cancel-review-button {
  background-color: var(--text-color-secundary);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: var(--panel-gap);
  margin-right: var(--panel-gap);
}

.cancel-review-button:hover {
  background-color: var(--half-transparent-background);
  transform: translateY(-2px);
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

  .comment-header {
    flex-direction: row;
    align-items: center;
  }

  .comments-list {
    width: 100%;
  }

  .review-form {
    width: 100%;
  }
}
</style>
