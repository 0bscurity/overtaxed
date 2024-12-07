module.exports = {
    mode: "jit",
    content: [
        './templates/**/*.html', // Django templates
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('daisyui'),
    ],
    daisyui: {
        themes: ["light", "dark", "sunset"],
    },
};
