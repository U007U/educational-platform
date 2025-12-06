document.addEventListener('DOMContentLoaded', function() {
    console.log('JS загружен!');
    
    // ГАМБУРГЕР МЕНЮ
    const hamburger = document.querySelector('.hamburger');
    const menu = document.querySelector('.menu');
    
    if (hamburger && menu) {
        console.log('Гамбургер найден!');
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            hamburger.classList.toggle('active');
            menu.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
            console.log('Гамбургер клик!');
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
            console.log('Логин отправлен!');
            // ... остальной код логина
        });
    }
});
