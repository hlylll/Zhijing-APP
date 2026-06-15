/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#F98C53',
        secondary: '#ABD7FB',
        accent: '#D2E0AA',
      },
    },
  },
  plugins: [],
}