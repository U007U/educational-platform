document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const passwordError = document.getElementById('passwordError');
    
    registerForm.addEventListener('submit', async function(e) {
        // Блокируем все
        e.preventDefault();
        e.stopPropagation();
        
        // Сбрасываем ошибки
        passwordError.textContent = '';
        
        // Получаем данные
        const formData = new FormData(registerForm);
        const password = formData.get('password');
        const confirmPassword = formData.get('password_confirm');
        const email = formData.get('username');
        
        // ВАЛИДАЦИЯ
        let errors = [];
        
        // Email
        if (!email) errors.push('Введите email');
        else if (!email.includes('@') || !email.includes('.')) errors.push('Неверный формат email');
        
        // Пароль
        if (!password) errors.push('Введите пароль');
        else if (password.length < 6) errors.push('Пароль должен быть не менее 6 символов');
        else if (password !== confirmPassword) errors.push('Пароли не совпадают');
        
        if (errors.length > 0) {
            passwordError.textContent = errors[0];
            setTimeout(() => {
                CustomAlert.error(errors.join('\n'), 'Ошибка ввода');
            }, 50);
            return;
        }
        
        // Блокируем кнопку
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        submitBtn.textContent = '⏳ Регистрация...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/auth/register-html', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                setTimeout(() => {
                    CustomAlert.success('Регистрация успешна! Выполняется вход...', 'Поздравляем!');
                    window.location.href = '/dashboard';
                }, 50);
            } else {
                const error = await response.json();
                setTimeout(() => {
                    CustomAlert.error(error.detail || 'Ошибка регистрации', 'Ошибка');
                }, 50);
            }
        } catch (error) {
            setTimeout(() => {
                CustomAlert.error('Ошибка сервера', 'Сетевая ошибка');
            }, 50);
        } finally {
            submitBtn.textContent = 'Зарегистрироваться';
            submitBtn.disabled = false;
        }
    });
});