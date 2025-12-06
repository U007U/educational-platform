document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const menu = document.getElementById('menu');
    const userEmail = localStorage.getItem('userEmail') || 'user@example.com';
    const initial = userEmail.charAt(0).toUpperCase();
    const userInitial = document.getElementById('userInitial');
    
    if (userInitial) {
        userInitial.textContent = initial;
        userInitial.title = `Пользователь: ${userEmail}`;
    }
    
    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        document.body.classList.toggle('menu-open');
        hamburger.classList.toggle('active');
        menu.classList.toggle('active');
    });
    
    document.addEventListener('click', function(e) {
        if (!hamburger.contains(e.target) && !menu.contains(e.target)) {
            document.body.classList.remove('menu-open');
            hamburger.classList.remove('active');
            menu.classList.remove('active');
        }
    });

    // ВСПЛЫВАЮЩЕЕ МЕНЮ ТЕМ
    window.toggleThemeMenu = function(event) {
        event.preventDefault();
        document.getElementById('themeCard').classList.toggle('active');
    };

    // ЛОГИКА ПЕРЕКЛЮЧАТЕЛЕЙ ТЕМ
    document.querySelectorAll('.toggle-switch input').forEach(input => {
        input.addEventListener('change', function() {
            const theme = this.dataset.theme;
            
            if (theme === 'system') {
                localStorage.removeItem('theme');
                const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.documentElement.setAttribute('data-theme', systemDark ? 'dark' : 'light');
            } else {
                localStorage.setItem('theme', theme);
                document.documentElement.setAttribute('data-theme', theme);
            }
            
            document.getElementById('themeCard').classList.remove('active');
        });
    });

    // ЗАКРЫТИЕ МЕНЮ ТЕМ ПРИ КЛИКЕ НАДВОЕ
    document.getElementById('themeCard')?.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    window.setTheme = function(theme) {
        if (theme === 'system') localStorage.removeItem('theme');
        else localStorage.setItem('theme', theme);
        document.documentElement.setAttribute('data-theme', theme);
    };

    window.loadCourses = window.loadLessons = window.loadProfile = function() {
        document.body.classList.remove('menu-open');
        document.getElementById('hamburger').classList.remove('active');
        document.getElementById('menu').classList.remove('active');
    };
    
    window.logout = function() { 
        localStorage.clear(); 
        window.location.href = '/'; 
    };
});
