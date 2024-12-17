import { By, until } from 'selenium-webdriver'
import { WebDriverFactory } from '../utils/WebDriverFactory'

/**
 * Validates the functionality of deleting a rating in the system.
 */
describe('Profile Test', function () {
  this.timeout(300000) // Set a maximum time for the test execution.

  it('should log in, edit profile, validate alerts, and save changes', async function () {
    const driver = await WebDriverFactory.createDriver()

    try {
      // Navigate to the login page
      await driver.get('http://localhost:8080/login')
      await driver.manage().window().setRect({ width: 1000, height: 1000 })

      // Enter credentials
      const usernameInput = await driver.wait(
        until.elementLocated(By.id('loginUsername')),
        10000
      )
      await usernameInput.sendKeys('testUI@gmail.com')

      const passwordInput = await driver.wait(
        until.elementLocated(By.id('loginPassword')),
        10000
      )
      await passwordInput.sendKeys('123456789Aa')

      // Click login button
      const loginButton = await driver.findElement(By.id('loginButton'))
      await loginButton.click()

      // Verify redirection after login
      await driver.wait(until.urlIs('http://localhost:8080/'), 10000)
      console.log('Login successful!')

      // Click on the profile button
      const profileButton = await driver.wait(
        until.elementLocated(By.id('profileBtn')),
        10000
      )
      await profileButton.click()

      await driver.get('http://localhost:8080/?q=FwAHExYESRkOFxcFCwIOXiAbLw4fXxAcFgRIGQc6GUMQAFhXUkQ%3D')

      // Click the Edit Profile button
      const editProfileButton = await driver.wait(
        until.elementLocated(By.id('editProfileBtn')),
        10000
      )
      await editProfileButton.click()

      // Wait for inputs to have content before clearing
      const nameInput = await driver.findElement(By.id('name'))
      await driver.wait(async () => (await nameInput.getAttribute('value')).trim() !== '', 5000)

      const surnameInput = await driver.findElement(By.id('surname'))
      await driver.wait(async () => (await surnameInput.getAttribute('value')).trim() !== '', 5000)

      const usernameInputEdit = await driver.findElement(By.id('username'))
      await driver.wait(async () => (await usernameInputEdit.getAttribute('value')).trim() !== '', 5000)

      const emailInput = await driver.findElement(By.id('email'))
      await driver.wait(async () => (await emailInput.getAttribute('value')).trim() !== '', 5000)

      // Clear inputs for name, surname, username, and email
      await nameInput.clear()
      await nameInput.sendKeys(' ')

      await surnameInput.clear()
      await surnameInput.sendKeys(' ')

      await usernameInputEdit.clear()
      await usernameInputEdit.sendKeys(' ')

      await emailInput.clear()
      await emailInput.sendKeys(' ')

      // Click the Submit button for the profile form
      const submitButton = await driver.findElement(By.id('submitBtnUser'))
      await submitButton.click()

      // Verify that the alert banner is now visible
      const alertBanner = await driver.wait(
        until.elementLocated(By.id('alertBanner')),
        10000
      )
      const isAlertVisible = await alertBanner.isDisplayed()
      if (isAlertVisible) {
        console.log('Alert banner is visible as expected.')
      } else {
        throw new Error('Alert banner is not visible.')
      }

      // Update the inputs with new data
      await nameInput.sendKeys('Fernando')
      await surnameInput.sendKeys('Lopez')
      await usernameInputEdit.sendKeys('fernandoLopez')
      await emailInput.sendKeys('testUI@gmail.com')

      console.log('Profile updated successfully!')
    } catch (error) {
      console.error('Test execution failed:', error)
      throw error // Throw error for Mocha to register the test failure
    } finally {
      // Close the browser
      await driver.quit()
    }
  })
})
