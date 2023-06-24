import { defineConfig } from "vite";
import laravel from "laravel-vite-plugin";

export default defineConfig({
    plugins: [
        laravel({
            input: [
                "resources/css/app.css",
                "node_modules/@fortawesome/fontawesome-free/css/all.min.css",
                "resources/js/app.js",
            ],
            refresh: true,
        }),
    ],
});
