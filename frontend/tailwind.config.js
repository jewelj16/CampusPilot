/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // "Steel canteen tray" palette — a nod to the physical mess-coupon
        // booklets and steel thali trays this app is digitizing, not the
        // usual cream/terracotta SaaS default.
        ink: {
          DEFAULT: "#1E2438",
          50: "#F1F2F6",
          100: "#E1E3EC",
          400: "#6E7590",
          600: "#3B4260",
          900: "#1E2438",
        },
        canvas: "#EEEBE1",
        card: "#FBFAF5",
        mustard: {
          DEFAULT: "#DB9E33",
          50: "#FBF1DF",
          600: "#B87E1F",
        },
        veg: "#2F7D52",
        nonveg: "#A33C3C",
      },
      fontFamily: {
        display: ["'Zilla Slab'", "serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      boxShadow: {
        ticket: "0 1px 0 rgba(30,36,56,0.06), 0 8px 20px -12px rgba(30,36,56,0.35)",
      },
      animation: {
        'pan-bg': 'panBackground 30s ease-in-out infinite',
      },
      keyframes: {
        panBackground: {
          '0%, 100%': { backgroundPosition: '0% 50%', backgroundSize: '110% auto' },
          '50%': { backgroundPosition: '100% 50%', backgroundSize: '115% auto' },
        },
      },
    },
  },
  plugins: [],
};
