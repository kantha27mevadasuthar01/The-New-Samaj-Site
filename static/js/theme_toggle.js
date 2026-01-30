document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const icon = toggleBtn ? toggleBtn.querySelector('i') : null;

    // Check saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
        if (icon) icon.className = 'fas fa-sun'; // Show sun if currently dark
    } else {
        htmlElement.removeAttribute('data-theme');
        if (icon) icon.className = 'fas fa-moon'; // Show moon if currently light
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            if (htmlElement.getAttribute('data-theme') === 'dark') {
                // Switch to Light
                htmlElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                if (icon) icon.className = 'fas fa-moon';
            } else {
                // Switch to Dark
                htmlElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                if (icon) icon.className = 'fas fa-sun';
            }
        });
    }
});
