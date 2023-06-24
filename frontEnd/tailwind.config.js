/** @type {import('tailwindcss').Config} */
module.exports = {
    mode: "jit",
    darkMode: "media",
    content: ["./src/**/*.{html,js}"],
    theme: {
        extend: {
            container: {
                center: true,
                padding: "1rem",
            },
        },
    },
    plugins: [],
};
