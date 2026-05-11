/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-bg': '#FFFFFF',
        'secondary-bg': '#F8F9FA',
        'border-color': '#E9ECEF',
        'text-primary': '#212529',
        'text-secondary': '#6C757D',
        'accent': '#3A57E8',
        'success': '#198754',
        'error': '#DC3545',
      },
      backgroundImage: {
        'gradient-summary': 'linear-gradient(45deg, #EEF2FF 0%, #F3E8FF 100%)',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'h1': '28px',
        'h2': '22px',
        'h3': '18px',
        'body': '16px',
        'secondary': '14px',
      },
      spacing: {
        // 8px grid system
        '8': '8px',
        '16': '16px',
        '24': '24px',
        '32': '32px',
        '40': '40px',
        '48': '48px',
      },
      borderRadius: {
        'button': '6px',
        'card': '1px',
        'modal': '12px',
      },
    },
  },
  plugins: [],
}

