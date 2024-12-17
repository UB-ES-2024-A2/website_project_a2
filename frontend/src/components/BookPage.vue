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
            <div class="btn-wrap">
              <a :href="book.buy_link" target="_blank" rel="noopener noreferrer" class="buy-button">Buy Now</a>
              <button class="addButton tooltip-container" :class="{
                'red-background': isInMyBooks,
                'gradient-custom': !isInMyBooks
              }" @click="toggleMyBooks" :disabled="isProcessing || loadingMyBooks" >
                <span v-if="!isInMyBooks" class="tooltip-text">Add to Library</span>
                <span v-else class="tooltip-text">Remove from your Library</span>
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 12 12"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  :style="{ transform: isInMyBooks ? 'rotate(30deg)' : 'rotate(0deg)' }"
                >
                  <path d="M6 1.5L6 6M6 6V10.5M6 6H10.5M6 6H1.5" stroke="#282828" stroke-width="4" stroke-linecap="round"/>
                </svg>
              </button>
              <button
                @click="toggleReadBooks"
                class="read-books-button"
                :class="{ 'in-readbooks': isInReadBooks }"
                :disabled="isProcessing2"
              >
                {{ isInReadBooks ? 'Remove from Finished' : 'Add to Finished' }}
              </button>
            </div>

          </div>
        </div>

        <!-- Updated Comments section -->
        <div class="comments-section">
          <h2>Reader Reviews</h2>
          <button id="reviewBtn" @click="showReviewForm = true" class="leave-review-button">Leave a Review</button>

          <!-- Review Form -->
          <div v-if="showReviewForm" class="review-form">
            <h3>Write Your Review</h3>
            <div class="rating-input">
              <span v-for="star in 5" :key="star" :id="'star-' + star" @click="newReview.rating = star" class="star-input" :class="{'star-filled': star <= newReview.rating}">★</span>
            </div>
            <textarea id="reviewText" v-model="newReview.comment" maxlength="250" placeholder="Write your review (max 250 characters)" class="review-textarea"></textarea>
            <div class="char-count">{{ newReview.comment.length }}/250</div>
            <button @click="cancelReview" class="cancel-review-button">Cancel</button>
            <button id="submitReviewBtn" @click="submitReview" :disabled="!isReviewValid" class="submit-review-button">Submit Review</button>
            <div v-if="reviewError" class="error-message">{{ reviewError }}</div>
          </div>

          <div v-if="loadingComments" class="loading">
            <div class="spinner"></div>
            <p>Loading comments...</p>
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
              <button id="deleteBtn" v-if="comment.user_id === currentUser.id_user" @click="showDeleteConfirmationModal(comment.id_comment_rating)" class="delete-comment-button">
                <img src="@/assets/trashcan.svg" alt="Delete" class="trash-icon">
              </button>
            </div>
          </div>
          <div v-else class="no-comments">
            No reviews yet. Be the first to review this book!
          </div>
          <div v-if="showDeleteConfirmation" class="delete-confirmation-modal">
            <div class="modal-content">
              <h3>Delete Review</h3>
              <p>Are you sure you want to delete this review?</p>
              <div class="modal-buttons">
                <button id="confirmDelete" @click="confirmDelete" class="confirm-button">Yes</button>
                <button id="cancelDelete" @click="cancelDelete" class="cancel-button">No</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-data">No book data available</div>
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
        <div v-if="!isEditing">
          <div class="container mt-4">
            <div class="profile row">
              <div class="col-md-12 d-flex flex-column align-items-center justify-content-center text-center">
                <img
                  src="@/assets/user-black.svg"
                  alt="User Photo"
                  class="img-fluid rounded-circle shadow"
                  style="width: 150px; height: 150px;"
                />
                <p><strong>Name:</strong> {{ user.name }} {{ user.surname }}</p>
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>
                <button id="editProfileBtn" v-if="user.id_user==currentUser.id_user" @click="toggleEdit" class="btn btn-edit">Edit Profile</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <form @submit.prevent="updateUser">
            <div style="justify-content: center; align-items: center;">
              <img
                src="@/assets/user-black.svg"
                alt="User Photo"
                class="img-fluid rounded-circle shadow"
                style="width: 90px; height: 90px;"
              />
            </div>
            <div>
              <label for="name">Name</label>
              <input id="name" v-model="userForm.name" />
            </div>
            <div>
              <label for="surname">Surname</label>
              <input id="surname" v-model="userForm.surname" />
            </div>
            <div>
              <label for="username">Username</label>
              <input id="username" v-model="userForm.username" />
            </div>
            <div>
              <label for="email">Email</label>
              <input id="email" v-model="userForm.email" />
            </div>

            <div id="alertBanner" v-if="errorList.length > 0" class="alert alert-danger">
                <li v-for="err in errorList" :key="err">{{ err }}</li >
            </div>

            <button id="submitBtnUser" type="submit" class="btn btn-success">Save</button>
            <button type="button" @click="toggleEdit" class="btn btn-secondary">Cancel</button>
          </form>
        </div>
      </div>
      <div v-else class="no-data">No user data available</div>
  </div>
  </div>
</template>

<script>
import BookService from '../services/BookService'
import UserService from '../services/UserService'
import VueJwtDecode from 'vue-jwt-decode'
import { decode } from '../../utils/encoding.js'

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
      showReviewForm: false,
      newReview: {
        rating: 0,
        comment: ''
      },
      reviewError: null,
      showDeleteConfirmation: false,
      commentToDelete: null,
      currentUser: null,
      isProcessing: false,
      isInReadBooks: false,
      isProcessing2: false
    }
  },
  props: {
    searchResults: Array,
    myBooksList: Array,
    loadingMyBooks: Boolean
  },
  watch: {
    '$route.query': {
      handler () {
        // Decodificar el parámetro de la URL
        const decodedQuery = decode(this.$route.query.q || '')

        // Usar URLSearchParams para obtener los valores de los parámetros
        const queryParams = new URLSearchParams(decodedQuery)

        // Asignar los valores a las variables locales
        let textInput = queryParams.get('search') || ''
        let type = queryParams.get('type') || ''
        let id = queryParams.get('id') || ''

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
  computed: {
    token () {
      return this.$store.getters.token
    },
    isReviewValid () {
      return this.newReview.rating > 0 && this.newReview.comment.trim().length > 0
    },
    isInMyBooks () {
      if (!this.myBooksList.length) return false
      return this.myBooksList.some(item => item.data.id === this.book.id_book)
    }
  },
  created () {
    this.getCurrentUser()
  },
  mounted () {
    const token = this.$store.getters.token

    if (!token) {
      this.$router.push('/login')
    } else {
      this.getCurrentUser().then(() => {
        this.checkReadBooksStatus()
      })
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
      this.comments = [] // Reset comments before fetching
      BookService.getCommentsRatings(id)
        .then(response => {
          if (response.data && Array.isArray(response.data.comments)) {
            this.comments = response.data.comments
          } else {
            console.error('Unexpected response format:', response.data)
            this.comments = []
          }
          this.loadingComments = false
        })
        .catch(error => {
          console.error('Error fetching comments:', error)
          this.comments = []
          this.loadingComments = false
        })
    },
    formatDate (dateString) {
      if (!dateString) return ''
      const options = {year: 'numeric', month: 'long', day: 'numeric'}
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    deleteComment (commentId) {
      BookService.deleteComment(commentId)
        .then(() => {
          // Actualizar la lista de comentarios
          this.fetchComments(this.book.id_book)
          // Actualizar la información del libro (por si cambia el rating)
          this.fetchBook(this.book.id_book)
          this.$emit('updated-comments')
        })
        .catch(error => {
          console.error('Error deleting comment:', error)
          // Manejar el error (por ejemplo, mostrar un mensaje al usuario)
        })
    },
    submitReview () {
      this.reviewError = null
      // Primero, verificamos si el usuario ya ha comentado
      BookService.getCommentsRatings(this.book.id_book)
        .then(commentsResponse => {
          const comments = commentsResponse.data.comments || []
          const userHasCommented = comments.some(
            comment => comment.user_id === this.currentUser.id_user
          )
          if (userHasCommented) {
            throw new Error('You have already submitted a review for this book.')
          }
          // Si el usuario no ha comentado, procedemos a crear el comentario
          console.log('user', this.currentUser)
          return BookService.createCommentRating(
            this.book.id_book,
            this.currentUser.id_user,
            this.newReview.comment,
            this.newReview.rating
          )
        })
        .then(() => {
          this.showReviewForm = false
          this.newReview = {rating: 0, comment: ''}
          this.fetchComments(this.book.id_book)
          this.fetchBook(this.book.id_book)
          this.$emit('updated-comments')
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
      this.newReview = {rating: 0, comment: ''}
    },
    showDeleteConfirmationModal (commentId) {
      this.commentToDelete = commentId
      this.showDeleteConfirmation = true
    },
    confirmDelete () {
      if (this.commentToDelete) {
        BookService.deleteComment(this.commentToDelete)
          .then(() => {
            this.fetchComments(this.book.id_book)
            this.fetchBook(this.book.id_book)
            this.showDeleteConfirmation = false
            this.commentToDelete = null
          })
          .catch(error => {
            console.error('Error deleting comment:', error)
          })
      }
    },
    cancelDelete () {
      this.showDeleteConfirmation = false
      this.commentToDelete = null
    },
    async getCurrentUser () {
      if (this.token) {
        try {
          let decoded = VueJwtDecode.decode(this.token)
          const response = await UserService.readUserById(decoded.sub)
          this.currentUser = response.data
        } catch (error) {
          console.error('Error loading current user:', error)
          this.currentUser = {}
        }
      }
    },
    async toggleMyBooks () {
      if (!this.currentUser || !this.book) {
        return
      }
      try {
        this.isProcessing = true
        let myBooks = null
        if (this.isInMyBooks) {
          // Si el libro ya está en la lista "MyBooks", lo eliminamos
          await BookService.deleteBookFromMyBooks(this.currentUser.id_user, this.book.id_book)
          myBooks = this.myBooksList.filter(
            (book) => book.data.id !== this.book.id_book
          )
          this.$emit('update-my-books', myBooks)
        } else {
          // Si el libro no está en la lista "MyBooks", lo añadimos
          await BookService.addBookToMyBooks(this.currentUser.id_user, this.book.id_book)
          const newBook = {
            type: 'book',
            data: {
              title: this.book.title,
              genres: this.book.genres || [],
              image: this.book.image,
              authors: this.book.authors || 'Unknown Author',
              synopsis: this.book.synopsis || 'No synopsis available',
              rating: this.book.rating || 0.0,
              id: this.book.id_book
            }
          }

          // Añadir el libro modificado al array `myBooks`
          myBooks = [...this.myBooksList]
          myBooks.push(newBook)
          this.$emit('update-my-books', myBooks)
        }
        // Actualizar la lista de "MyBooks" del usuario
      } catch (error) {
        console.error('Error toggling MyBooks:', error)
      } finally {
        this.isProcessing = false // Reactiva el botón al finalizar
      }
    },
    async toggleReadBooks () {
      if (!this.currentUser || !this.book) {
        console.error('User not logged in or book not loaded')
        return
      }

      this.isProcessing2 = true

      try {
        if (this.isInReadBooks) {
          await BookService.deleteBookFromReadBooks(this.currentUser.id_user, this.book.id_book)
          this.isInReadBooks = false
          console.log('Book removed from Read Books')
        } else {
          await BookService.addBookToReadBooks(this.currentUser.id_user, this.book.id_book)
          this.isInReadBooks = true
          console.log('Book added to Read Books')
        }
        // Refresh the read books status after the operation
        await this.checkReadBooksStatus()
      } catch (error) {
        console.error('Error toggling read books status:', error)
        // Optionally, add user feedback here (e.g., this.$toast.error('Failed to update read books'))
      } finally {
        this.isProcessing2 = false
      }
    },
    async checkReadBooksStatus () {
      if (!this.currentUser || !this.book) return

      try {
        const response = await BookService.myReadBooks(this.currentUser.id_user)
        this.isInReadBooks = response.data.some(item => item.id_book === this.book.id_book)
        console.log('Read Books status:', this.isInReadBooks)
      } catch (error) {
        console.error('Error checking read books status:', error)
        this.isInReadBooks = false // Assume not in read books if there's an error
      }
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
  position: relative;
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

.submit-review-button, .cancel-review-button {
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: var(--panel-gap);
}

.submit-review-button {
  background-color: var(--purple-background);
  color: var(--text-color);
}

.submit-review-button:hover:not(:disabled) {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

.submit-review-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-review-button {
  background-color: var(--text-color-secundary);
  color: var(--text-color);
  margin-right: var(--panel-gap);
}

.cancel-review-button:hover {
  background-color: var(--half-transparent-background);
  transform: translateY(-2px);
}

.error-message {
  color: #ff4d4d;
  margin-top: var(--panel-gap);
  font-size: var(--font-size-xs);
}

.delete-comment-button {
  position: absolute;
  bottom: var(--panel-gap);
  right: var(--panel-gap);
  background: none;
  border: none;
  padding: calc(var(--panel-gap) / 2);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.delete-comment-button:hover {
  transform: scale(1.1);
}

.trash-icon {
  width: 1.5rem;
  height: 1.5rem;
  fill: white;
}

.delete-confirmation-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--box-background-color);
  padding: calc(var(--panel-gap) * 3);
  border-radius: var(--border-radius);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: var(--panel-gap);
  margin-top: calc(var(--panel-gap) * 2);
}

.confirm-button, .cancel-button {
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.confirm-button {
  background-color: #ff4d4d;
  color: white;
}

.confirm-button:hover {
  background-color: #cc0000;
}

.cancel-button {
  background-color: var(--text-color-secundary);
  color: white;
}

.cancel-button:hover {
  background-color: var(--half-transparent-background);
}

.btn-wrap {
  display: flex;
  flex-direction: row;
  gap: var(--panel-gap);
  align-items: center;
  margin-top: var(--panel-gap);
}

.addButton {
  border: 0;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: calc(var(--border-radius) * 2);
  align-items: center;
  display: flex;
  justify-content: center;
}

.red-background {
  background-color: rgba(255, 0, 0, 0.2);
}

.addButton svg {
  transition: transform 0.3s ease;
}

.read-books-button {
  background-color: var(--purple-background);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.read-books-button:hover {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

.read-books-button.in-readbooks {
  background-color: var(--text-color-secundary);
}

.read-books-button.in-readbooks:hover {
  background-color: var(--half-transparent-background);
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
