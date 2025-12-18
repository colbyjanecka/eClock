import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'heyanniewei.com',
      'www.heyanniewei.com',
      '.heyanniewei.com'  // allows all subdomains
    ]
  }
})
