/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        "handled-ink": "#101828",
        "handled-mint": "#22c55e",
        "handled-sand": "#f8f5f0"
      }
    }
  },
  plugins: []
};
