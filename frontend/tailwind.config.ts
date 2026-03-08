import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        glass: "0 8px 32px rgba(0, 0, 0, 0.24)",
        "glass-hover": "0 12px 40px rgba(0, 0, 0, 0.32)",
        soft: "0 4px 24px rgba(0, 0, 0, 0.12)",
      },
      backdropBlur: {
        glass: "12px",
      },
    },
  },
  plugins: [],
};
export default config;
