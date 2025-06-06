// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Garante que o Vite ouça em todos os IPs disponíveis no container
    port: 3000,      // <--- ADICIONE ESTA LINHA para forçar a porta 3000
    watch: {
      usePolling: true, // Pode ser útil em ambientes Linux/WSL para hot-reloading
    }
  }
})