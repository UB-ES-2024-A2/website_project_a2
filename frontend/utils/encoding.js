const secretKey = process.env.VUE_APP_ENCODING_SECRET_KEY || 'default_key'

/**
 * Codifica un texto utilizando una clave.
 * @param {string} text - El texto a codificar.
 * @returns {string} - Texto codificado.
 */
export function encode (text) {
  const encoded = text
    .split('') // Dividir texto en caracteres
    .map((char, i) => {
      // Aplicar XOR con la clave
      const keyChar = secretKey[i % secretKey.length]
      return String.fromCharCode(char.charCodeAt(0) ^ keyChar.charCodeAt(0))
    })
    .join('')
  return btoa(encoded) // Codificar en Base64
}

/**
 * Decodifica un texto utilizando una clave.
 * @param {string} encodedText - El texto codificado.
 * @returns {string} - Texto decodificado.
 */
export function decode (encodedText) {
  const decodedBase64 = atob(encodedText) // Decodificar de Base64
  const decoded = decodedBase64
    .split('') // Dividir texto en caracteres
    .map((char, i) => {
      // Aplicar XOR inverso con la clave
      const keyChar = secretKey[i % secretKey.length]
      return String.fromCharCode(char.charCodeAt(0) ^ keyChar.charCodeAt(0))
    })
    .join('')
  return decoded
}
