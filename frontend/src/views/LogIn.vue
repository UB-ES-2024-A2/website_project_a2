<template>
  <div class="body">
    <div class="gradient-custom min-vh-100">
      <div class="container py-5 h-100">
        <div class="row justify-content-center align-items-center h-100">
          <div class="col-12 col-lg-9 col-xl-7">
            <div class="card shadow-2-strong card-login" style="border-radius: 15px;">
              <div class="card-body p-4 p-md-5">

                <div class="text-center mb-4">
                  <img loading="lazy"  src="@/assets/bookhub-black.svg" alt="BookHub Logo" class="bookhub-logo">
                </div>

                <h2 class="title mb-4 pb-3 pb-md-0 mb-md-5">ReadHub Account</h2>
                <form @submit.prevent="submitLogin">

                  <div class="row">
                    <div class="col-12 mb-4">
                      <div class="form-floating">
                        <input type="text" class="form-control custom-input" id="loginUsername"
                               placeholder="Email"
                               v-model="username"
                               @input="clearStyles('loginUsername')" />
                        <label id="loginUsernameLabel" for="loginUsername">Email</label>
                        <div class="text-start text-error">
                          <div class="invalid-feedback" id="loginUsernameFeedback"></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12 mb-2">
                      <div class="form-floating">
                        <input type="password" class="form-control custom-input" id="loginPassword"
                               placeholder="Password"
                               v-model="password"
                               @input="clearStyles('loginPassword')" />
                        <label id="loginPasswordLabel" for="loginPassword">Password</label>
                        <div class="text-start text-error">
                          <div class="invalid-feedback" id="loginPasswordFeedback"></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div id="errorMessage" class="error-message-box text-error" v-if="errorMessage">{{ errorMessage }}</div>
                  <div class="mt-4 pt-2">
                    <input id="loginButton" class="btn btn-primary btn-lg w-100 gradient-custom" type="submit" value="Login"/>
                  </div>

                  <p class="text-center text-muted mt-5 mb-0">
                    Don’t have an account?
                    <router-link to="/signup" class="text-link">
                      <u>Sign up here</u>
                    </router-link>
                  </p>

                </form>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from '../services/AuthService'

export default {
  name: 'Login',
  data () {
    return {
      username: null,
      password: null,
      errorMessage: ''
    }
  },
  mounted () {
    const token = this.$store.getters.token

    if (token) {
      this.$router.push('/')
    }
  },
  methods: {
    clearStyles (field) {
      const inputElement = document.getElementById(field)
      const feedbackElement = document.getElementById(field + 'Feedback')
      inputElement.classList.remove('is-invalid', 'red-background')
      feedbackElement.style.display = 'none'
    },
    setMessage (field, message) {
      const inputElement = document.getElementById(field)
      const feedbackElement = document.getElementById(field + 'Feedback')
      inputElement.classList.add('is-invalid', 'red-background')
      feedbackElement.innerText = message
      feedbackElement.style.display = 'block'
    },
    validateInputs () {
      let isValid = true
      this.errorMessage = ''
      if (!this.username) {
        this.setMessage('loginUsername', "Email can't be empty.")
        isValid = false
      }
      if (!this.password) {
        this.setMessage('loginPassword', "Password can't be empty.")
        isValid = false
      }
      return isValid
    },
    async submitLogin () {
      if (this.validateInputs()) {
        AuthService.login(this.username, this.password)
          .then(response => {
            this.$store.dispatch('setToken', { token: response.data.access_token })
            this.$router.push({ name: 'HomePage' })
          })
          .catch(error => {
            this.errorMessage = 'Email or password is incorrect'
            console.error(error)
          })
      }
    }
  }
}
</script>

<style scoped>

.title {
  font-weight: 900;
}

.text-error {
  margin-top: 0.25rem;
}

.error-message-box {
  background-color: rgba(255, 0, 0, 0.2);
  border: 1px solid red;
  color: darkred;
  padding: 10px;
  border-radius: 5px;
  margin-top: 20px;
}

.text-link {
  color: var(--blue-link);
  font-weight: bold;
}

.bookhub-logo {
  width: 7rem;
}
</style>
