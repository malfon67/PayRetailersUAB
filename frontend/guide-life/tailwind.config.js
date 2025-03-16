module.exports = {
    content: [
        './src/**/*.{js,jsx,ts,tsx}', // The path to your React components/files
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/postcss'),
    ],
};