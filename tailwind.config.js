/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'meme-dark': '#14191f',
        'meme-darker': '#171212',
        'meme-gray': '#293542',
        'meme-light-gray': '#362b2c',
        'meme-text-gray': '#9badc0',
        'meme-text-light': '#b4a2a3',
        'meme-accent': '#e8b4b7',
      },
    },
  },
  plugins: [],
} 