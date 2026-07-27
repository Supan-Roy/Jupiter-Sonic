/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#030712", // Very deep dark slate
        foreground: "#f3f4f6", // Cool grey text
        primary: {
          DEFAULT: "#8b5cf6", // Vibrant Violet
          hover: "#7c3aed",
          glow: "#a78bfa"
        },
        secondary: {
          DEFAULT: "#1f2937", // Slate-800
          foreground: "#e5e7eb"
        },
        card: {
          DEFAULT: "#0b0f19", // Darker card background
          border: "#1e293b",
          hover: "#131a2b"
        },
        border: "#1e293b",
        success: "#10b981",
        warning: "#f59e0b",
        danger: "#ef4444"
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      boxShadow: {
        "primary-glow": "0 0 15px -3px rgba(139, 92, 246, 0.4)",
        "success-glow": "0 0 15px -3px rgba(16, 185, 129, 0.4)",
        "card-glow": "0 10px 30px -10px rgba(0, 0, 0, 0.7)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in-up": "fadeInUp 0.5s ease-out forwards",
        "glow": "glowCycle 4s ease-in-out infinite",
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        glowCycle: {
          "0%, 100%": { filter: "drop-shadow(0 0 5px rgba(139, 92, 246, 0.3))" },
          "50%": { filter: "drop-shadow(0 0 15px rgba(139, 92, 246, 0.6))" },
        }
      }
    },
  },
  plugins: [],
}
