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
              <div class="col-md-8 d-flex flex-column">
                <!-- <h2 class="book-title mb-4"></h2> -->
              </div>
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
import UserService from '../services/UserService'
import VueJwtDecode from 'vue-jwt-decode'
export default {
  name: 'Profile',
  data () {
    return {
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
      errorList: []
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
          this.userForm = { ...this.user }
          this.loading = false
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
          this.user = { ...this.userForm }
          this.isEditing = false
        })
        .catch((error) => {
          console.error('Error updating user:', error)
          this.errorList = ['Failed to update user data.']
        })
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

@media (max-width: 768px) {
  .profile {
    min-width: auto;
  }
}
</style>
