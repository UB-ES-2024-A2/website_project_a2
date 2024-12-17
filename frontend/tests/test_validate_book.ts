import { By, until } from 'selenium-webdriver'
import { WebDriverFactory } from '../utils/WebDriverFactory'

/**
 * Valida la funcionalidad de visualización de un libro en el sistema.
 */
describe('Display Book Test', function () {
  this.timeout(300000) // Establece un tiempo máximo para la ejecución del test.

  it('should log in and display the book details', async function () {
    const driver = await WebDriverFactory.createDriver()

    try {
      // Navegar a la página de login
      await driver.get('http://localhost:8080/login')
      await driver.manage().window().setRect({ width: 1920, height: 1080 })

      // Ingresar credenciales
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

      await driver.findElement(By.id('loginButton')).click()

      // Verificar redirección después del login
      await driver.wait(until.urlIs('http://localhost:8080/'), 10000)
      console.log('Login successful!')

      // Hacer clic en el enlace del libro
      const targetElement = await driver.wait(
        until.elementLocated(
          By.css('a[href*="FwAHExYESQsETjINCQpKFEc5MAgOEAoCBAgHCFIrEhUcWQcJDh5KHTtWVA%3D%3D"]')
        ),
        10000
      )
      await targetElement.click()

      // Verificar el enlace de Amazon
      const amazonLink = await driver.wait(
        until.elementLocated(
          By.css(
            'a[href="https://www.amazon.com/To-Kill-a-Mockingbird-Harperperennial/dp/0060935464"]'
          )
        ),
        10000
      )

      // Verifica que el enlace esté presente
      if (amazonLink) {
        console.log('Element found and test passed!')
      } else {
        console.error('Element not found: Test failed')
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
