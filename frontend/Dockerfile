# Usa una imagen base de Node.js
FROM node:16

# Establece el directorio de trabajo
WORKDIR /frontend

# Copia los archivos de configuración
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de la aplicación
COPY . .

# Exponer el puerto de la aplicación
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["npm", "run", "dev"]
