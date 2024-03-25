/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["worf/app/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

