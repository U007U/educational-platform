document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();  // ✅ БЛОКИРУЕТ GET!
        
        const formData = new FormData(registerForm);
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        submitBtn.textContent = '⏳ Регистрация...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                alert('✅ Регистрация успешна! Переходим к входу.');
                window.location.href = '/auth/login';
            } else {
                const error = await response.json();
                alert('❌ ' + (error.detail || 'Ошибка регистрации'));
            }
        } catch (error) {
            alert('❌ Ошибка сервера');
        } finally {
            submitBtn.textContent = 'Зарегистрироваться';
            submitBtn.disabled = false;
        }
    });
});
