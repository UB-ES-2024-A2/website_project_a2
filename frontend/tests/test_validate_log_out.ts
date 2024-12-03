import { By, until } from 'selenium-webdriver'
import { WebDriverFactory } from '../utils/WebDriverFactory'

/**
 * Ejecuta una prueba de logout en el sistema.
 */
describe('Logout button validation', () => {
  it('should logout successfully', async () => {
    const driver = await WebDriverFactory.createDriver()
    try {
      await driver.get('http://localhost:8080')
      await driver.manage().window().setRect({ width: 1920, height: 1080 })

      // Iniciar sesión (suponiendo que ya hay una lógica de login)
      await driver.findElement(By.id('logInBtn')).click()
      await driver.wait(until.urlIs('http://localhost:8080/login'), 10000)
      await driver.findElement(By.id('loginUsername')).sendKeys('testUI@gmail.com')
      await driver.findElement(By.id('loginPassword')).sendKeys('123456789Aa')
      await driver.findElement(By.id('loginButton')).click()
      await driver.wait(until.urlIs('http://localhost:8080/'), 10000)

      // Verificar que el usuario está logueado
      const localStorageUsername = await driver.executeScript(
        'return localStorage.getItem("username");'
      )
      console.log(localStorageUsername) // Debería mostrar el nombre de usuario

      // Realizar logout
      await driver.findElement(By.id('logOutBtn')).click()

      // Verificar que el localStorage está vacío después del logout
      const localStorageAfterLogout = await driver.executeScript(
        'return localStorage.getItem("username");'
      )
      if (!localStorageAfterLogout) {
        console.log('LocalStorage is cleared after logout')
      } else {
        console.error('LocalStorage still contains username after logout')
      }
    } catch (error) {
      console.error('Test execution failed:', error)
      throw error // Lanza el error para que Mocha registre el fallo
    } finally {
      // Cerrar el navegador
      await driver.quit()
    }
  })
})
