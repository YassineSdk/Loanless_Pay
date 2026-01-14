/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#0d8a75',
          DEFAULT: '#0a6d5d',
          dark: '#085648',
        },
         accent: {
          DEFAULT: '#f59e0b',
        }
      }
    },
  },
  plugins: [],
}
