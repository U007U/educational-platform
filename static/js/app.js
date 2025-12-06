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

    // ✅ ИСПРАВЛЕННЫЙ BOOTSTRAP THEME SWITCHER
    function setTheme(mode = 'auto') {
        const userMode = localStorage.getItem('bs-theme');
        const sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const useSystem = mode === 'system' || (!userMode && mode === 'auto');
        const modeChosen = useSystem ? 'system' : (mode === 'dark' || mode === 'light' ? mode : userMode);

        if (useSystem) {
            localStorage.removeItem('bs-theme');
        } else {
            localStorage.setItem('bs-theme', modeChosen);
        }

        // ✅ ФИКС: data-theme вместо data-bs-theme + правильная логика
        const theme = useSystem ? (sysDark ? 'dark' : 'light') : modeChosen;
        document.documentElement.setAttribute('data-theme', theme);
        
        // Подсветка активной кнопки
        document.querySelectorAll('.btn-theme').forEach(e => e.classList.remove('text-primary'));
        const activeBtn = document.getElementById(modeChosen);
        if (activeBtn) activeBtn.classList.add('text-primary');
    }

    // Инициализация + обработчики тем
    setTheme();
    document.querySelectorAll('.btn-theme').forEach(e => {
        e.addEventListener('click', () => setTheme(e.id));
    });
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => setTheme());

    // ✅ ЛОГИН → ДАШБОРД
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const btn = loginForm.querySelector('button, .btn');
            
            btn.textContent = '⏳ Вход...';
            btn.disabled = true;
            
            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
                });
                
                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('userEmail', email);
                    window.location.href = '/dashboard';  // ✅ РЕДИРЕКТ!
                } else {
                    alert('❌ Неверный логин/пароль');
                }
            } catch (error) {
                alert('❌ Ошибка сервера');
            } finally {
                btn.textContent = 'Войти';
                btn.disabled = false;
            }
        });
    }

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
