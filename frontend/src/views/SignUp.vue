<template>
  <div class="body">
    <div class="gradient-custom min-vh-100">
      <div class="container py-5 h-100">
        <div class="row justify-content-center align-items-center h-100">
          <div class="col-12 col-lg-9 col-xl-7">
            <div class="card shadow-2-strong card-registration" style="border-radius: calc(var(--border-radius) * 3)">
              <div class="card-body p-4 p-md-5">

                <div class="text-center mb-4">
                  <img loading="lazy" src="@/assets/bookhub-black.svg" alt="BookHub Logo" class="bookhub-logo">
                </div>

                <h2 class="title mb-4 pb-3 pb-md-0 mb-md-5">Create Your ReadHub Account</h2>
                <form @submit.prevent="sumbitData">

                  <div class="row">
                    <div class="col-md-6 mb-4">

                      <div class="form-floating">
                        <input type="text" class="form-control first-letter-upper-case" id="firstName" placeholder="name"
                               v-model="name"
                               @input="clearStyles('firstName')"
                               maxlength="50"/>
                        <label id="firstNameLabel" for="firstName">First Name</label>
                         <div class="text-start text-error">
                            <div class="invalid-feedback" id="firstNameFeedback" style="display: none;"></div>
                         </div>
                      </div>

                    </div>
                    <div class="col-md-6 mb-4">

                      <div class="form-floating">
                        <input type="text" class="form-control first-letter-upper-case" id="lastName" placeholder="lastname"
                               v-model="lastname"
                               @input="clearStyles('lastName')"
                               maxlength="120"/>
                        <label id="lastNameLabel" for="lastName">Last Name</label>
                         <div class="text-start text-error">
                          <div class="invalid-feedback" id="lastNameFeedback" style="display: none;"></div>
                         </div>
                      </div>

                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12 mb-4">

                      <div class="form-floating">
                        <input type="text" class="form-control custom-input" id="userName"
                               placeholder="username"
                               v-model="username"
                               @input="clearStyles('userName')"/>
                        <label id="userNameLabel" for="userName">Username</label>
                        <div class="text-start text-error">
                          <div class="invalid-feedback" id="userNameFeedback" style="display: none;"></div>
                        </div>
                      </div>

                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12 mb-2">

                      <div class="form-floating">
                        <input type="email" class="form-control custom-input" id="userMail" placeholder="email"
                               v-model="email" @input="clearStyles('userMail')"/>
                        <label id="userMailLabel" for="userMail">Email</label>
                        <div class="text-start text-error">
                          <div class="invalid-feedback" id="userMailFeedback" style="display: none;"></div>
                        </div>
                      </div>

                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12 mb-2">

                     <div class="form-floating">

                      <input type="password" class="form-control custom-input" id="userPassword"
                             placeholder="password" aria-describedby="passwordHelpBlock"
                             v-model="password" @input="checkPassword">
                      <label id="userPasswordLabel" for="userPassword">Password</label>
                       <div class="text-start text-error">
                          <div class="invalid-feedback" id="userPasswordFeedback" style="display: none;"></div>
                       </div>
                       <div class="text-start text-error">
                         <div class="valid-feedback" id="userPasswordCorrect"  style="display: none;">
                           Looks good!
                         </div>
                       </div>
                      <div class="text-start text-error">
                        <small id="passwordHelpBlock" class="form-text text-muted">
                          Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces or special characters.
                        </small>
                      </div>

                    </div>

                    </div>
                  </div>

                  <div class="row">
                    <div class="col-12 mb-2">

                      <div class="form-floating">
                        <input type="password" class="form-control custom-input" id="userPasswordConfirm"
                               placeholder="password"
                               v-model="confirmPassword"
                               @input="clearStyles('userPasswordConfirm')"
                               @blur="checkPasswordMatch"/>
                        <label id="userPasswordConfirmLabel" for="userPasswordConfirm">Confirm password</label>
                        <div class="text-start text-error">
                          <div class="invalid-feedback" id="userPasswordConfirmFeedback" style="display: none;"></div>
                        </div>
                      </div>

                    </div>
                  </div>

                  <div id="errorMessage" class="error-message-box text-error" v-if="errorMessage">{{ errorMessage }}</div>

                  <div class="mt-4 pt-2">
                    <input class="btn btn-primary btn-lg w-100 gradient-custom"
                           type="submit" value="Sign up" />
                  </div>

                  <p class="text-center text-muted mt-5 mb-0">
                    Have already an account?
                    <router-link to="/login" class="text-link">
                      <u>Login here</u>
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
import AuthService from '../services/AuthService' // Service for user registration and login

export default {
  name: 'SignUp',
  data () {
    return {
      name: null,
      lastname: null,
      username: null,
      email: null,
      password: null,
      confirmPassword: null,
      isValidPassword: false,
      isValidConfirmPassword: false,
      errorMessage: false
    }
  },
  mounted () {
    const token = this.$store.getters.token

    if (token) {
      this.$router.push('/')
    }
  },
  watch: {
    password () {
      // When password changes, check the confirm password
      this.checkPasswordMatch()
    },
    confirmPassword () {
      // When confirm password changes check it
      this.checkPasswordMatch()
    }
  },
  methods: {
    async login_user () {
      AuthService.login(this.email, this.password)
        .then(res => {
          this.$store.dispatch('setToken', { token: res.acces_token })
          this.$router.push({ name: 'HomePage' })
        })
        .catch((error) => {
          console.error(error)
          this.errorMessage = 'Username or Password incorrect'
        })
    },
    async register_user (event) {
      // Calls the register method from AuthService
      AuthService.register(this.email, this.username, this.password, this.name, this.lastname)
        .then(res => {
          this.login_user()
        })
        .catch((error) => {
          console.error(error)
          if (error.response && error.response.status === 400) {
            this.setMessage('userMail', 'Invalid email: The user already exists')
          } else {
            this.errorMessage = 'An error occurred during registration'
          }
        })
    },
    clearStyles (nameElement) {
      let inputElement = document.getElementById(nameElement)
      let feedbackElement = document.getElementById(nameElement + 'Feedback')
      let labelElement = document.getElementById(nameElement + 'Label')

      // Clears styles invalid and messages for an input element
      inputElement.classList.remove('is-invalid', 'red-background')
      labelElement.classList.remove('red-text')
      feedbackElement.style.display = 'none'
    },
    setMessage (nameElement, errorMessage) {
      let inputElement = document.getElementById(nameElement)
      let feedbackElement = document.getElementById(nameElement + 'Feedback')
      let labelElement = document.getElementById(nameElement + 'Label')

      // Sets error message for input validation
      inputElement.classList.add('is-invalid')
      inputElement.classList.add('red-background')
      labelElement.classList.add('red-text')
      feedbackElement.innerText = errorMessage
      feedbackElement.style.display = 'block'
      inputElement.value && (inputElement.value = inputElement.value.trim())
    },
    checkFirstName () {
      if (this.name) {
        this.name = this.name.trim()
        let isValid = true
        let invalidMessages = []

        // Name can't contain special characters or number
        if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ]+( [a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ]+)*$/.test(this.name)) {
          invalidMessages.push('Can not contain special characters or numbers..')
          isValid = false
        }
        // Name can't contains spaces
        if (this.name.includes(' ')) {
          invalidMessages.push('Cannot contain spaces.')
          isValid = false
        }
        // Name must be between 2 and 50 characters
        if (this.name.length < 2) {
          invalidMessages.push('Name must be between 2 and 50 characters.')
          isValid = false
        }

        if (!isValid) {
          this.setMessage('firstName', 'Invalid name: ' + invalidMessages.join(' '))
        }
        return isValid
      }
      return false
    },
    checkLastName () {
      if (this.lastname) {
        this.lastname = this.lastname.trim()
        let isValid = true
        let invalidMessages = []
        // Last name can't contain special characters or numbers
        if (!/^[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ]+( [a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ]+)*$/.test(this.lastname)) {
          invalidMessages.push('Can not contain special characters or numbers.')
          isValid = false
        }
        // Last name can't contains spaces
        if (this.lastname.includes(' ')) {
          invalidMessages.push('Cannot contain spaces.')
          isValid = false
        }
        // Last name has to be between 2 and 50 characters
        if (this.lastname.length < 2) {
          invalidMessages.push('Must be between 2 and 50 characters.')
          isValid = false
        }

        if (!isValid) {
          this.setMessage('lastName', 'Invalid last name: ' + invalidMessages.join(' '))
        }
        return isValid
      }
      return false
    },
    checkMail () {
      if (this.email && !/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(this.email)) {
        this.setMessage('userMail', 'Invalid email format. Please use a valid format like user@example.com.')
        return false
      }
      return true
    },
    sumbitData () {
      if (this.errorMessage) {
        this.errorMessage = false
      }
      let formArrayValues = [this.name, this.lastname, this.username, this.email, this.password, this.confirmPassword]
      let inputElememtNames = ['firstName', 'lastName', 'userName', 'userMail', 'userPassword', 'userPasswordConfirm']
      let isValid = true
      formArrayValues.forEach((item, index) => {
        // Check if any field is empty
        if (!item || item.toString().trim() === '') {
          isValid = false
          this.setMessage(inputElememtNames[index], "This field can't be empty.")
        }
      })

      // Check field conditions
      let isFirstNameValid = this.checkFirstName()
      let isLastNameValid = this.checkLastName()
      let isMailValid = this.checkMail()
      if (isValid && isFirstNameValid && isLastNameValid && isMailValid && this.isValidPassword && this.isValidConfirmPassword) {
        // Create new user
        this.register_user()
      }
    },

    checkPassword: function () {
      let passwordHelpBlock = document.getElementById('passwordHelpBlock')
      this.clearStyles('userPassword')

      if (this.password) {
        let invalidMessages = []
        let code = this.password.trim()
        let validElement = document.getElementById('userPassword' + 'Correct')

        // Checks if the password length
        if (code.length < 8 || code.length > 20) {
          invalidMessages.push('Password must be 8-20 characters long.')
        }

        // Checks the password letters uppercase
        if (!/[A-Z]/.test(code)) {
          invalidMessages.push('Password must contain at least one uppercase letter.')
        }

        // Checks if the password contains any lowercase letter
        if (!/[a-z]/.test(code)) {
          invalidMessages.push('Password must contain at least one lowercase letter.')
        }

        // Checks if the password contains any number
        if (!/[0-9]/.test(code)) {
          invalidMessages.push('Password must contain at least one digit.')
        }

        if (invalidMessages.length > 0) {
          let feedbackElement = document.getElementById('userPassword' + 'Feedback')

          // Set the invalid message
          feedbackElement.innerText = 'Invalid password: ' + invalidMessages.join(' ')
          feedbackElement.style.display = 'block'
          passwordHelpBlock.style.display = 'none'
          validElement.style.display = 'none'
        } else {
          validElement.style.display = 'block'
          this.isValidPassword = true
        }
      } else {
        passwordHelpBlock.style.display = 'block'
      }
    },
    checkPasswordMatch () {
      this.clearStyles('userPasswordConfirm')
      let feedbackElement = document.getElementById('userPasswordConfirmFeedback')
      let confirmInputElement = document.getElementById('userPasswordConfirm')
      let label = document.getElementById('userPasswordConfirmLabel')
      if (this.password && this.confirmPassword) {
        if (this.password !== this.confirmPassword) {
          // Add invalid styles
          confirmInputElement.classList.add('is-invalid')
          confirmInputElement.classList.add('red-background')
          label.classList.add('red-text')
          feedbackElement.style.display = 'block'
          feedbackElement.innerText = 'Passwords do not match.'
          confirmInputElement.classList.add('is-invalid')
          this.isValidConfirmPassword = false
        } else {
          // Clear styles
          feedbackElement.style.display = 'none'
          confirmInputElement.classList.remove('is-invalid')
          this.isValidConfirmPassword = true
        }
      }
    }
  }

}

</script>
<style scoped>

  .card-registration .select-input.form-control[readonly]:not([disabled]) {
    font-size: 1rem;
    line-height: 2.15;
    padding-left: .75em;
    padding-right: .75em;
  }
  .card-registration .select-arrow {
    top: 0.813rem;
  }

  .title {
    font-weight: 900;
  }

  .text-error{
    margin-top: 0.25rem;
  }

.error-message-box {
  background-color: rgba(255, 0, 0, 0.2);
  border: 0.063rem solid red;
  color: darkred;
  padding: 0.625rem;
  border-radius: 50.313rem;
  margin-top: 1.25rem;
}

  .red-background{
    background-color: rgba(255, 0, 0, 0.1);
    border: 0.063rem solid red;
  }

  .red-text{
    color: red !important;
    background-color: transparent !important;
  }

  .text-link {
    color: var(--blue-link);
    font-weight: bold;
  }

  .bookhub-logo {
    width: 7rem;
  }

  .first-letter-upper-case{
    text-transform:capitalize;
  }

</style>
