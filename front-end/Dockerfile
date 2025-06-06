# frontend/Dockerfile

# Usar uma imagem base oficial do Node.js
FROM node:18-alpine

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos package.json e package-lock.json
COPY package.json package-lock.json ./

# Instalar as dependências do Node.js
RUN npm install

# Copiar o restante do código da aplicação
COPY . .

# Remover a etapa de build para permitir que o servidor de desenvolvimento seja iniciado.
# Para produção, você precisaria de 'npm run build' e um servidor web como Nginx.
# RUN npm run build

# Expor a porta que sua aplicação React (ou servidor de desenvolvimento) está ouvindo
# Geralmente React development server roda na porta 3000
EXPOSE 3000

# Comando para iniciar a aplicação React em modo de desenvolvimento
CMD ["npm", "run", "dev"]
