document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JS загружен!');
    
    // ТЕМА ПО УМОЛЧАНИЮ
    const savedTheme = localStorage.getItem('theme');
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (systemDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
    console.log('Тема:', theme);
    
    // ГАМБУРГЕР МЕНЮ
    const hamburger = document.querySelector('.hamburger');
    const menu = document.querySelector('.menu');
    
    if (hamburger && menu) {
        console.log('✅ Гамбургер найден!');
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            hamburger.classList.toggle('active');
            menu.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
            console.log('☰ Гамбургер КЛИК!');
        });
        
        // Закрытие по клику вне меню
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !menu.contains(e.target)) {
                hamburger.classList.remove('active');
                menu.classList.remove('active');
                document.body.classList.remove('no-scroll');
            }
        });
    }
    
    // ТЕМА ПЕРЕКЛЮЧАТЕЛЬ (в меню настроек)
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            document.getElementById('themeIcon').textContent = newTheme === 'dark' ? '☀️' : '🌙';
            console.log('Тема изменена:', newTheme);
        });
    }
    
    // LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('🔐 Логин...');
            // ... код логина из предыдущего сообщения
        });
    }
});
