/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        industrial: {
          950: '#070a12',
          900: '#0f172a',
          800: '#1e293b',
          cyan: '#00f2fe',
          blue: '#4facfe',
        }
      }
    },
  },
  plugins: [],
}
