<template>
  <div id="main-page" class="main-page">
    <div v-if="type === 'user'" class="book-page-wrap">
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
              <div class="col-md-4 d-flex flex-column align-items-center justify-content-center text-center">
                <img
                  src="@/assets/user-black.svg"
                  alt="User Photo"
                  class="img-fluid rounded-circle shadow"
                  style="width: 150px; height: 150px;"
                />
                <p><strong>Name:</strong> {{ user.name }} {{ user.surname }}</p>
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>

                <div class="d-flex flex-column justify-content-center align-items-center gap-3 mt-3">
                  <button
                    id="editProfileBtn"
                    v-if="user.id_user === currentUser.id_user"
                    @click="toggleEdit"
                    class="btn btn-edit"
                    style="padding: 8px 16px; font-size: 14px;"
                  >
                    Edit Profile
                  </button>

                  <button
                    id="statsBtn"
                    @click="toggleStatsModal"
                    class="d-flex align-items-center justify-content-center btn btn-stats"
                    style="padding: 8px 16px; font-size: 14px;"
                  >
                    <img
                      loading="lazy"
                      src="@/assets/stats.png"
                      alt="Stats Icon"
                      style="width: 35px; height: 35px; border-radius: 25%;"
                    />
                    Show stats
                  </button>
                </div>
              </div>
              <div class="col-md-8">
                <div class="read-books-section">
                  <h3 class="read-books-title">{{ user.username }}'s Read Books</h3>
                  <div v-if="loadingBooks" class="loading-books">
                    <div class="spinner"></div>
                    <p>Loading books...</p>
                  </div>
                  <div v-else-if="readBooks.length > 0">
                    <ul class="read-books-list">
                      <li v-for="book in readBooks" :key="book.id" class="read-book-item">
                        <img :src="book.cover" :alt="book.title" class="book-cover">
                        <span class="book-title">{{ book.title }}</span>
                      </li>
                    </ul>
                  </div>
                  <div v-else class="no-books-message">
                    This user hasn't read any books yet.
                  </div>
                </div>
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
              <input id="name" v-model="userForm.name"/>
            </div>
            <div>
              <label for="surname">Surname</label>
              <input id="surname" v-model="userForm.surname"/>
            </div>
            <div>
              <label for="username">Username</label>
              <input id="username" v-model="userForm.username"/>
            </div>
            <div>
              <label for="email">Email</label>
              <input id="email" v-model="userForm.email"/>
            </div>

            <div id="alertBanner" v-if="errorList.length > 0" class="alert alert-danger">
              <li v-for="err in errorList" :key="err">{{ err }}</li>
            </div>

            <button id="submitBtnUser" type="submit" class="btn btn-success">Save</button>
            <button type="button" @click="toggleEdit" class="btn btn-secondary">Cancel</button>
          </form>
        </div>
      </div>
      <div v-else class="no-data">No user data available</div>
    </div>

    <div v-if="showStatsModal" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <!-- Encapçalament -->
          <div class="modal-header">
            <div v-if="currentChartIndex === 0">
              <h5 class="modal-title">User Rating Distribution</h5>
            </div>
            <div v-if="currentChartIndex === 1">
              <h5 class="modal-title">Most read genres</h5>
            </div>
            <div v-if="currentChartIndex === 2">
              <h5 class="modal-title">Average scores by gender</h5>
            </div>
          </div>

          <!-- Contingut del modal -->
          <div class="modal-body">
            <!-- Contenidor de la gràfica -->
            <div class="chart-container">
              <!-- Mostrar gràfica segons l'índex -->
              <div v-if="currentChartIndex === 0 && booksRatings">
                <BarChart :chart-data="chartData1" :options="chartOptions1" />
              </div>
              <div v-if="currentChartIndex === 0 && !booksRatings">
                <p>This user has not rated any book</p>
              </div>
              <div v-if="currentChartIndex === 1 && readBooks">
                <PieChart :chart-data="chartData" :options="chartOptions" />
              </div>
              <div v-if="currentChartIndex === 1 && !readBooks">
                <p>This user has no books marked as read</p>
              </div>
              <div v-if="currentChartIndex === 2 && booksRatings">
                <BarChart :chart-data="chartData2" :options="chartOptions2" />
              </div>
              <div v-if="currentChartIndex === 2 && !booksRatings">
                <p>This user has not rated any book</p>
              </div>
            </div>
          </div>

          <!-- Peu de pàgina amb botons -->
          <div class="modal-footer d-flex justify-content-between align-items-center">
            <!-- Botons de navegació -->
            <div class="navigation-buttons">
              <button
                type="button"
                class="btn btn-primary"
                @click="prevChart"
                :disabled="currentChartIndex === 0"
              >
                &larr; Previous
              </button>
              <button
                type="button"
                class="btn btn-primary"
                @click="nextChart"
                :disabled="currentChartIndex === charts.length - 1"
              >
                Following &rarr;
              </button>
            </div>

            <!-- Botó de tancar -->
            <button type="button" class="btn btn-secondary" @click="toggleStatsModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserService from '../services/UserService'
import BookService from '../services/BookService'
import VueJwtDecode from 'vue-jwt-decode'
import BarChart from './Barchart.vue'
import PieChart from './PieChart.vue'

import { decode } from '../../utils/encoding.js'

export default {
  name: 'Profile',
  components: {
    BarChart,
    PieChart
  },
  data () {
    return {
      charts: ['BarChart', 'PieChart', 'BarChart'],
      currentChartIndex: 0,
      booksRatings: null,
      chartData2: {},
      chartData1: {},
      chartData: {},
      chartOptions: {},
      chartOptions1: {},
      chartOptions2: {},
      showStatsModal: false,
      textInput: '',
      type: '',
      loading: false,
      error: null,
      user: null,
      currentUser: null,
      userForm: {
        name: '',
        surname: '',
        username: '',
        email: ''
      },
      isEditing: false,
      errorList: [],
      readBooks: [],
      loadingBooks: false
    }
  },
  props: {
    searchResults: Array
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
          if (type === 'user' && id) {
            this.fetchUsers(id)
          }
        }
      },
      immediate: true
    }
  },
  computed: {
    token () {
      return this.$store.getters.token
    }
  },
  created () {
    this.getCurrentUser()
  },
  mounted () {
    const token = this.$store.getters.token

    if (!token) {
      this.$router.push('/login')
    }
  },
  methods: {
    processAverageRatingsByGenre (books) {
      const defaultGenres = [
        'Fiction', 'Classic', 'Romance', 'Adventure',
        'Fantasy', 'Horror', 'Epic', 'Science Fiction'
      ]
      const genreRatings = {}
      defaultGenres.forEach(genre => {
        genreRatings[genre] = { total: 0, count: 0 }
      })

      books.data.forEach(item => {
        const book = item.book
        if (book.genres && genreRatings[book.genres] !== undefined) {
          genreRatings[book.genres].total += item.user_rating
          genreRatings[book.genres].count += 1
        }
      })

      const averageRatings = defaultGenres.map(genre => ({
        genre,
        average: genreRatings[genre].count > 0
          ? (genreRatings[genre].total / genreRatings[genre].count).toFixed(2)
          : '0.00'
      }))

      this.chartData2 = {
        labels: averageRatings.map(data => data.genre),
        datasets: [{
          label: 'Average score',
          data: averageRatings.map(data => data.average),
          backgroundColor: ['#FF6347', '#FFD700', '#32CD32', '#4682B4', '#8A2BE2', '#9400D3', '#FFA500', '#A52A2A']
        }]
      }
      this.chartOptions2 = {
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Genres'
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Average Ratings'
            }
          }]
        }
      }
    },
    processRatings (books) {
      const ratingDistribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
      books.data.forEach(item => {
        ratingDistribution[item.user_rating]++
      })
      this.chartData1 = {
        labels: Object.keys(ratingDistribution),
        datasets: [{
          label: 'Number of ratings per star',
          data: Object.values(ratingDistribution),
          backgroundColor: ['#FF6347', '#FFD700', '#32CD32', '#4682B4', '#8A2BE2']
        }]
      }
      this.chartOptions1 = {
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Number of stars'
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Number of Ratings'
            }
          }]
        }
      }
    },
    prevChart () {
      if (this.currentChartIndex > 0) {
        this.currentChartIndex -= 1
      }
    },
    nextChart () {
      if (this.currentChartIndex < this.charts.length - 1) {
        this.currentChartIndex += 1
      }
    },
    async getMyRatings (id) {
      this.loading = true
      this.error = null
      BookService.myRatings(id)
        .then((response) => {
          if (response.data.count === 0) {
            this.booksRatings = null
          } else {
            this.booksRatings = response.data
            this.processRatings(this.booksRatings)
            this.processAverageRatingsByGenre(this.booksRatings)
          }
          this.loading = false
        })
        .catch((error) => {
          console.error('Error fetching books:', error)
          this.error = 'Failed to load books data'
          this.loading = false
        })
    },
    async getMyReadBooks (id) {
      this.loading = true
      this.error = null
      BookService.myReadBooks(id)
        .then((response) => {
          console.log(response)
          this.readBooks = response.data
          this.processGenres(this.readBooks)
          this.loading = false
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            this.readBooks = null
          } else {
            this.error = 'Failed to load books data'
          }
          this.loading = false
        })
    },
    processGenres (books) {
      const genres = books.map(book => book.genres)
      const genreCount = genres.reduce((acc, genre) => {
        acc[genre] = (acc[genre] || 0) + 1
        return acc
      }, {})
      this.chartData = {
        labels: Object.keys(genreCount),
        datasets: [{
          data: Object.values(genreCount),
          backgroundColor: ['#FF6347',
            '#4682B4',
            '#32CD32',
            '#FFD700',
            '#8A2BE2',
            '#FF1493',
            '#00FA9A',
            '#FF8C00']
        }]
      }
    },
    toggleStatsModal () {
      this.showStatsModal = !this.showStatsModal
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
    fetchUsers (id) {
      this.loading = true
      this.error = null
      UserService.readUserById(id)
        .then((response) => {
          this.user = response.data
          this.userForm = {...this.user}
          this.loading = false

          this.getMyRatings(this.user.id_user)
          this.getMyReadBooks(this.user.id_user)

          this.fetchReadBooks(id)
        })
        .catch((error) => {
          console.error('Error fetching user:', error)
          this.error = 'Failed to load user data'
          this.loading = false
        })
    },
    toggleEdit () {
      this.isEditing = !this.isEditing
    },
    validateUser () {
      this.errorList = []
      if (!this.userForm.name.trim()) this.errorList.push('Name is required.')
      if (!this.userForm.surname.trim()) this.errorList.push('Surname is required.')
      if (!this.userForm.username.trim()) this.errorList.push('Username is required.')
      if (!this.userForm.email.trim()) {
        this.errorList.push('Email is required.')
      } else if (!/\S+@\S+\.\S+/.test(this.userForm.email)) {
        this.errorList.push('Invalid email format.')
      }

      return this.errorList.length === 0
    },
    updateUser () {
      if (!this.validateUser()) {
        return
      }
      UserService.updateUser(this.currentUser.id_user, this.userForm)
        .then(() => {
          this.user = {...this.userForm}
          this.isEditing = false
        })
        .catch((error) => {
          console.error('Error updating user:', error)
          this.errorList = ['Failed to update user data.']
        })
    },
    async fetchReadBooks (userId) {
      this.loadingBooks = true
      this.readBooks = [] // Limpiar el array antes de la petición
      try {
        const response = await BookService.myReadBooks(userId)
        if (response.data && response.data.length > 0) {
          this.readBooks = response.data.map(book => ({
            id: book.id_book,
            title: book.title,
            cover: book.image
          }))
        }
      } catch (error) {
        console.error('Error fetching read books:', error)
      } finally {
        this.loadingBooks = false
      }
    }
  }
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 50%;
  width: 100%;
  margin: 0 auto;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.main-page {
  grid-area: main-page;
  padding: calc(var(--panel-gap) * 2);
  background-color: var(--box-background-color);
  color: var(--text-color);
  border-radius: calc(var(--border-radius) * 2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading,
.error,
.no-data {
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

.profile {
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  margin-top: var(--panel-gap);
  min-height: 60vh;
  min-width: 150vh;
}

.alert-danger {
  background-color: rgba(255, 0, 0, 0.2);
  border: 0.063rem solid red;
  color: white;
  padding: 0.625rem;
  border-radius: 50.313rem;
  margin-top: 1.25rem;
  list-style-type: none;
}

.alert-danger ul {
  margin: 0;
  padding-left: 1.5rem;
}

.btn-edit {
  margin-right: var(--panel-gap);
  font-weight: 700;
  color: var(--text-color);
  width: 9rem;
  height: 3rem;
  transition: transform 0.3s ease-in-out;
  border-radius: calc(var(--border-radius) * 2);
  background: var(--purple-background);
}

.book-page-wrap {
  max-width: 1200px;
  margin: 0 auto;
}

.read-books-section {
  margin-top: 2rem;
  background: var(--half-transparent-background);
  border-radius: var(--border-radius);
  padding: 1.5rem;
}

.read-books-title {
  font-size: var(--font-size-medium);
  color: var(--text-color);
  margin-bottom: 1.5rem;
  text-align: left;
  padding-left: 0.5rem;
}

.read-books-list {
  list-style-type: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.read-book-item {
  display: flex;
  align-items: center;
  background: var(--box-background-color);
  padding: 0.75rem;
  border-radius: var(--border-radius);
  width: calc(50% - 0.5rem);
  transition: transform 0.2s ease-in-out;
}

.read-book-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-cover {
  width: 50px;
  height: 75px;
  object-fit: cover;
  margin-right: 1rem;
  border-radius: calc(var(--border-radius) / 2);
}

.book-title {
  font-size: 0.9rem;
  color: var(--text-color);
}

.no-books-message {
  text-align: center;
  padding: 2rem;
  background: var(--box-background-color);
  border-radius: var(--border-radius);
  color: var(--text-color-secundary);
}

.loading-books {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.loading-books .spinner {
  border: 4px solid var(--half-transparent-background);
  border-top: 4px solid var(--purple-background);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: var(--panel-gap);
}

.loading-books p {
  color: var(--text-color-secundary);
  font-size: var(--font-size-xs);
}

@media (max-width: 768px) {
  .profile {
    min-width: auto;
  }

  .read-book-item {
    width: 100%;
  }
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  z-index: 1050;
}

.modal-content {
  background-color: var(--box-background-color);
  border-radius: var(--border-radius);
  padding: var(--panel-gap);
}

.btn-stats {
  margin-right: var(--panel-gap);
  font-weight: 700;
  color: black;
  width: 9rem;
  height: 3rem;
  transition: transform 0.3s ease-in-out;
  border-radius: calc(var(--border-radius) * 2);
  background: white;
}

</style>
