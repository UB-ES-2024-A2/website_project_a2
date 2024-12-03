import {Builder, WebDriver, By, until, Key} from 'selenium-webdriver'
import * as chrome from 'selenium-webdriver/chrome'

/**
 * Crea una instancia de WebDriver para ejecutar pruebas en chrome.
 */
export const createWebDriver = async (): Promise<WebDriver> => {
  // Configurar opciones de chrome
  const options = new chrome.Options()
  options.addArguments(
    '--headless',
    '--enable-local-storage',
    '--no-sandbox', // Ejecutar sin sandbox para entornos seguros
    '--disable-dev-shm-usage', // Prevenir problemas con almacenamiento compartido en Docker
    '--disable-gpu' // Deshabilitar la aceleración de GPU para entornos headless
  )

  // Crear y devolver el WebDriver configurado
  return new Builder()
    .forBrowser('chrome') // Indicar que el navegador es chrome
    .setChromeOptions(options) // Aplicar las opciones configuradas
    .build()
}

/**
 * Ejecuta una prueba de login en el sistema.
 */
async function testLogin () {
  const driver = await createWebDriver() // Utiliza la función reutilizable para crear el WebDriver

  try {
    // Navegar a la página de login
    await driver.get('http://localhost:8080')
    await driver.get('http://localhost:8080/login')

    await driver.manage().window().setRect({ width: 1920, height: 1080 })

    // Esperar a que el campo de nombre de usuario esté visible
    const usernameInput = await driver.wait(
      until.elementLocated(By.id('loginUsername')),
      10000
    )
    await usernameInput.sendKeys('testUI@gmail.com')

    // Esperar a que el campo de contraseña esté visible
    const passwordInput = await driver.wait(
      until.elementLocated(By.id('loginPassword')),
      10000
    )
    await passwordInput.sendKeys('123456789Aa')

    // Hacer clic en el botón de login
    const loginButton = await driver.wait(
      until.elementLocated(By.id('loginButton')),
      10000
    )

    await driver.executeScript('arguments[0].scrollIntoView(true);', loginButton)
    await driver.sleep(500)

    await loginButton.click()

    // Esperar a que la URL cambie después del login
    await driver.wait(until.urlIs('http://localhost:8080/'), 10000)
    console.log('Login successful!')

    const targetElement = await driver.wait(
      until.elementLocated(
        By.css('a[href="/?search=To%20Kill%20a%20Mockingbird&type=book&id=1"]')
      ),
      10000
    )

    // Haz clic en el elemento
    await targetElement.click()

    // Step 3: Verifica el elemento con el enlace de Amazon
    await driver.wait(
      until.elementLocated(
        By.css(
          'a[href="https://www.amazon.com/To-Kill-a-Mockingbird-Harperperennial/dp/0060935464"]'
        )
      ),
      10000
    )

    console.log('Element found and test passed!')
  } catch (error) {
    console.error('Test failed:', error)
  } finally {
    // Cerrar el navegador
    await driver.quit()
  }
}

// Ejecutar la prueba
testLogin()
