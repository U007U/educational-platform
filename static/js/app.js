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
