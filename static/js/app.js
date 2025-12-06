// ГАМБУРГЕР МЕНЮ
function toggleMenu() {
    document.querySelector('.hamburger').classList.toggle('active');
    document.querySelector('.menu').classList.toggle('active');
}

// LOGIN
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
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
            throw new Error('Неверный логин/пароль');
        }
    } catch (error) {
        alert('❌ ' + error.message);
    } finally {
        btn.textContent = 'Войти в систему'; btn.disabled = false;
    }
});

// DASHBOARD
if (window.location.pathname === '/dashboard') {
    if(!localStorage.getItem('token')) window.location.href='/';
    
    fetch('/protected/profile', {
        headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
    }).then(r=>r.json()).then(user=> {
        document.getElementById('userEmail').textContent = user.email;
    }).catch(()=>window.location.href='/');
    
    function logout() { localStorage.removeItem('token'); window.location.href='/'; }
    function loadCourses() { alert('Курсы скоро!'); }
    function loadLessons() { alert('Уроки скоро!'); }
    function loadProfile() { alert('Настройки скоро!'); }
}
