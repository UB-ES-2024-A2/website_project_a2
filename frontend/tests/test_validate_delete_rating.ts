import { By, until } from 'selenium-webdriver'
import { WebDriverFactory } from '../utils/WebDriverFactory'

/**
 * Valida la funcionalidad de eliminar una valoración en el sistema.
 */
describe('Delete Rating Test', function () {
  this.timeout(300000) // Establece un tiempo máximo para la ejecución del test.

  it('should log in, add a review, delete it, and verify its removal', async function () {
    const driver = await WebDriverFactory.createDriver()

    try {
      // Navegar a la página de login
      await driver.get('http://localhost:8080/login')
      await driver.manage().window().setRect({ width: 1920, height: 1920 })

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

      // Verificar que el botón de reseñas está disponible y hacer clic
      const reviewBtn = await driver.wait(
        until.elementLocated(By.id('reviewBtn')),
        10000
      )
      await reviewBtn.click()

      // Verificar si el textarea para la reseña está presente y escribir la reseña
      const reviewText = await driver.wait(
        until.elementLocated(By.id('reviewText')),
        10000
      )
      await reviewText.sendKeys('Great Book')

      // Verificar que el botón de enviar reseña está deshabilitado inicialmente
      const submitReviewBtn = await driver.wait(
        until.elementLocated(By.id('submitReviewBtn')),
        10000
      )

      const submitButtonDisabled = await submitReviewBtn.isEnabled()
      if (submitButtonDisabled) {
        console.error('Submit button should be disabled initially')
      }

      // Hacer clic en el span de las estrellas (por ejemplo, la estrella número 5)
      const star5 = await driver.wait(
        until.elementLocated(By.id('star-5')),
        10000
      )
      await star5.click()

      // Wait for the submitReviewBtn element to be located
      const submitReviewBtnClick = await driver.wait(
        until.elementLocated(By.id('submitReviewBtn')), // Wait for the element to be located
        10000
      )

      // Scroll the element into view
      await driver.executeScript('arguments[0].scrollIntoView(true);', submitReviewBtnClick)

      // Now that it's visible and enabled, click the button
      await submitReviewBtnClick.click()

      // Esperar a que la página se recargue completamente
      await driver.wait(until.urlIs('http://localhost:8080/?q=FwAHExYESQsETjINCQpKFEc5MAgOEAoCBAgHCFIrEhUcWQcJDh5KHTtWVA%3D%3D'), 10000)

      // Localizar el botón de eliminar comentario y hacer clic
      const deleteIcon = await driver.wait(
        until.elementLocated(By.id('deleteBtn')),
        10000
      )

      // Desplazar hasta el elemento para asegurarse de que es visible
      await driver.executeScript('arguments[0].scrollIntoView(true);', deleteIcon)

      // Luego puedes hacer clic en la imagen si lo necesitas
      await deleteIcon.click()

      // Esperar a que el botón de confirmación de eliminación esté visible
      const confirmDeleteButton = await driver.wait(
        until.elementLocated(By.id('confirmDelete')),
        10000
      )

      // Hacer clic en el botón de confirmación de eliminación
      await confirmDeleteButton.click()

      // Esperar que la página se recargue y verificar que la URL sea la correcta
      await driver.wait(
        until.urlIs('http://localhost:8080/?q=FwAHExYESQsETjINCQpKFEc5MAgOEAoCBAgHCFIrEhUcWQcJDh5KHTtWVA%3D%3D'),
        10000
      )

      // Verificar que el botón de eliminar ya no está visible o disponible
      const deleteButtons = await driver.findElements(By.id('deleteBtn'))

      // Verificar si la lista de elementos está vacía (el botón ya no está presente)
      if (deleteButtons.length === 0) {
        console.log('El botón de eliminar ya no está presente.')
      } else {
        // Si el botón está presente, verificar si está visible
        const isVisible = await deleteButtons[0].isDisplayed()

        if (!isVisible) {
          console.log('El botón de eliminar está presente pero no es visible.')
        } else {
          console.log('El botón de eliminar sigue visible y disponible.')
        }
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
