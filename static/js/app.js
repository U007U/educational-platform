// ТЕМА ПО УМОЛЧАНИЮ (системная + localStorage)
const isDark = localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
document.querySelector('.theme-toggle').textContent = isDark ? '☀️' : '🌙';

// ПЕРЕКЛЮЧАТЕЛЬ ТЕМЫ
document.querySelector('.theme-toggle').addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    document.querySelector('.theme-toggle').textContent = isDark ? '🌙' : '☀️';
    localStorage.setItem('theme', newTheme);
});

// АВТОРИЗАЦИЯ
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const btn = document.querySelector('.btn');

    try {
        btn.textContent = '⏳ Вход...'; btn.disabled = true;
        const response = await fetch('/auth/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
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
        btn.textContent = '🚀 Войти'; btn.disabled = false;
    }
});
