/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          primary: '#0f1117',
          panel: '#1a1d27',
          hover: '#222536',
          border: '#2a2d3a',
        },
        teal: {
          DEFAULT: '#2dd4bf',
          dim: 'rgba(45, 212, 191, 0.15)',
        },
        pink: {
          DEFAULT: '#f472b6',
          dim: 'rgba(244, 114, 182, 0.2)',
        }
      }
    }
  },
  plugins: [],
}