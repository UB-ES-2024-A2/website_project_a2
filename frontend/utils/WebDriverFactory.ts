import { Builder, WebDriver } from 'selenium-webdriver'
import * as chrome from 'selenium-webdriver/chrome'

/**
 * Crea una instancia de WebDriver para ejecutar pruebas en chrome.
 */
export class WebDriverFactory {
  static async createDriver (): Promise<WebDriver> {
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
}
