document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const errorDiv = document.getElementById('loginError');
    
    // Демо данные
    document.getElementById('email').value = 'test@example.com';
    document.getElementById('password').value = '123456';
    
    loginForm.addEventListener('submit', async function(e) {
        // Полная блокировка браузерного поведения
        e.preventDefault();
        e.stopPropagation();
        
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        
        // ВАЛИДАЦИЯ НА КЛИЕНТЕ
        let errors = [];
        
        if (!email) errors.push('Введите email');
        else if (!email.includes('@') || !email.includes('.')) errors.push('Неверный формат email');
        
        if (!password) errors.push('Введите пароль');
        else if (password.length < 3) errors.push('Пароль слишком короткий');
        
        if (errors.length > 0) {
            // Показываем ошибки через 50ms (после возможного окна браузера)
            setTimeout(() => {
                CustomAlert.error(errors.join('\n'), 'Ошибка ввода');
            }, 50);
            return;
        }
        
        // Блокируем кнопку
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
                
                // Успех - перенаправляем
                window.location.href = '/dashboard';
            } else {
                const error = await response.json();
                const errorMsg = error.detail || 'Неверный логин/пароль';
                
                setTimeout(() => {
                    CustomAlert.error(errorMsg, 'Ошибка входа');
                }, 50);
            }
        } catch (error) {
            setTimeout(() => {
                CustomAlert.error('Ошибка соединения с сервером', 'Сетевая ошибка');
            }, 50);
        } finally {
            loginBtn.textContent = 'Войти';
            loginBtn.disabled = false;
        }
    });
});