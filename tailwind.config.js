/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./frontend/resources/html/**/*.{html,js}",
    "./frontend/vue-project/src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        light: '#f8f9fa',
        dark: '#212529'
      }
    },
  },
  plugins: [],
} 