// ГАМБУРГЕР МЕНЮ (работает на всех страницах)
document.querySelector('.hamburger')?.addEventListener('click', toggleMenu);

function toggleMenu() {
    document.querySelector('.hamburger').classList.toggle('active');
    document.querySelector('.menu').classList.toggle('active');
    document.body.classList.toggle('no-scroll');
}

// ЗАКРЫТИЕ МЕНЮ при клике на item
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelector('.hamburger').classList.remove('active');
        document.querySelector('.menu').classList.remove('active');
        document.body.classList.remove('no-scroll');
    });
});

// LOGIN (только на главной)
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const btn = document.querySelector('.btn');
        
        try {
            btn.textContent = '⏳ Вход...'; btn.disabled = true;
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
            });
            
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                window.location.href = '/dashboard';
            } else {
                alert('❌ Неверный логин/пароль');
            }
        } catch (error) {
            alert('❌ Ошибка сервера');
        } finally {
            btn.textContent = 'Войти в систему'; btn.disabled = false;
        }
    });
}

// DASHBOARD (только на дашборде)
if (window.location.pathname === '/dashboard') {
    const token = localStorage.getItem('token');
    if (!token) window.location.href = '/';
    
    fetch('/protected/profile', {
        headers: {'Authorization': `Bearer ${token}`}
    }).then(r => r.json()).then(user => {
        document.getElementById('userEmail').textContent = user.email;
    }).catch(() => window.location.href = '/');
    
    window.logout = function() { 
        localStorage.removeItem('token'); 
        window.location.href = '/'; 
    }
    
    window.loadCourses = function() { alert('🔥 Курсы CRUD - следующий шаг!'); }
    window.loadLessons = function() { alert('📚 Lessons CRUD - делаем сейчас!'); }
    window.loadProfile = function() { alert('⚙️ Настройки - скоро!'); }
}
