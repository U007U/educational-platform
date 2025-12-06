document.addEventListener('DOMContentLoaded', function() {
    // ГАМБУРГЕР МЕНЮ
    const hamburger = document.querySelector('.hamburger');
    const menu = document.querySelector('.menu');
    
    if (hamburger && menu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            menu.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
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
    
    // LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
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
    
    // DASHBOARD
    if (window.location.pathname === '/dashboard') {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/';
            return;
        }
        
        fetch('/protected/profile', {
            headers: {'Authorization': `Bearer ${token}`}
        }).then(r => r.json()).then(user => {
            document.getElementById('userEmail').textContent = user.email;
        }).catch(() => window.location.href = '/');
    }
});
