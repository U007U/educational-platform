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

    // BOOTSTRAP THEME SWITCHER
    function setTheme(mode = 'auto') {
        const userMode = localStorage.getItem('bs-theme');
        const sysMode = window.matchMedia('(prefers-color-scheme: light)').matches;
        const useSystem = mode === 'system' || (!userMode && mode === 'auto');
        const modeChosen = useSystem ? 'system' : mode === 'dark' || mode === 'light' ? mode : userMode;

        if (useSystem) localStorage.removeItem('bs-theme');
        else localStorage.setItem('bs-theme', modeChosen);

        document.documentElement.setAttribute('data-bs-theme', useSystem ? (sysMode ? 'light' : 'dark') : modeChosen);
        document.querySelectorAll('.btn-theme').forEach(e => e.classList.remove('text-primary'));
        document.getElementById(modeChosen)?.classList.add('text-primary');
    }

    setTheme();
    document.querySelectorAll('.btn-theme').forEach(e => e.addEventListener('click', () => setTheme(e.id)));
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => setTheme());

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
