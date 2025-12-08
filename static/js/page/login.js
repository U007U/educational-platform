document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const errorDiv = document.getElementById('loginError');
    
    // Демо данные
    document.getElementById('email').value = 'test@example.com';
    document.getElementById('password').value = '123456';
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        loginBtn.textContent = '⏳ Вход...';
        loginBtn.disabled = true;
        errorDiv.style.display = 'none';
        
        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
            });
            
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('userEmail', email);
                document.cookie = `auth_user=${email}; path=/; max-age=86400`;
                localStorage.setItem('isAuthenticated', 'true');
                window.location.href = '/dashboard';
            } else {
                const error = await response.json();
                showError(error.detail || 'Неверный логин/пароль');
            }
        } catch (error) {
            showError('Ошибка сервера. Проверьте подключение.');
        } finally {
            loginBtn.textContent = 'Войти';
            loginBtn.disabled = false;
        }
    });
    
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
});
