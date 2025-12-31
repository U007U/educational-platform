/**
 * Custom Alerts for EduPlatform
 * Красивые стилизованные alert вместо стандартных
 */

const CustomAlert = {
    // Показать алерт
    show: function({ title, message, type = 'info', timeout = 0, onConfirm = null }) {
        return new Promise((resolve) => {
            // Создаем оверлей
            const overlay = document.createElement('div');
            overlay.className = 'custom-alert-overlay';
            
            // Определяем иконку по типу
            const iconMap = {
                success: '✓',
                error: '✗',
                warning: '⚠',
                info: 'ℹ'
            };
            
            // Создаем алерт
            const alertHTML = `
                <div class="custom-alert ${type}">
                    <div class="custom-alert-header">
                        <div class="custom-alert-icon">${iconMap[type]}</div>
                        <div class="custom-alert-title">${title}</div>
                        <button class="custom-alert-close">×</button>
                    </div>
                    <div class="custom-alert-body">
                        ${message}
                    </div>
                    <div class="custom-alert-buttons">
                        <button class="custom-alert-btn custom-alert-btn-primary">OK</button>
                    </div>
                </div>
            `;
            
            overlay.innerHTML = alertHTML;
            document.body.appendChild(overlay);
            
            // Функция закрытия
            const closeAlert = () => {
                overlay.style.animation = 'fadeOut 0.2s ease-out';
                setTimeout(() => {
                    if (overlay.parentNode) {
                        overlay.remove();
                    }
                    resolve(true);
                    if (onConfirm) onConfirm();
                }, 200);
            };
            
            // Назначаем обработчики
            const okBtn = overlay.querySelector('.custom-alert-btn-primary');
            const closeBtn = overlay.querySelector('.custom-alert-close');
            
            okBtn.addEventListener('click', closeAlert);
            closeBtn.addEventListener('click', closeAlert);
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) closeAlert();
            });
            
            // Авто-закрытие по таймауту
            if (timeout > 0) {
                setTimeout(closeAlert, timeout);
            }
            
            // Фокус на кнопке OK
            setTimeout(() => okBtn.focus(), 100);
        });
    },
    
    // Быстрые методы
    success: function(message, title = 'Успешно!') {
        return this.show({
            title: title,
            message: message,
            type: 'success',
            timeout: 3000
        });
    },
    
    error: function(message, title = 'Ошибка!') {
        return this.show({
            title: title,
            message: message,
            type: 'error'
        });
    },
    
    warning: function(message, title = 'Внимание!') {
        return this.show({
            title: title,
            message: message,
            type: 'warning'
        });
    },
    
    info: function(message, title = 'Информация') {
        return this.show({
            title: title,
            message: message,
            type: 'info',
            timeout: 3000
        });
    },
    
    confirm: function({ title, message, confirmText = 'Да', cancelText = 'Отмена' }) {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'custom-alert-overlay';
            
            overlay.innerHTML = `
                <div class="custom-alert info">
                    <div class="custom-alert-header">
                        <div class="custom-alert-icon">?</div>
                        <div class="custom-alert-title">${title}</div>
                        <button class="custom-alert-close">×</button>
                    </div>
                    <div class="custom-alert-body">
                        ${message}
                    </div>
                    <div class="custom-alert-buttons">
                        <button class="custom-alert-btn custom-alert-btn-secondary">${cancelText}</button>
                        <button class="custom-alert-btn custom-alert-btn-primary">${confirmText}</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(overlay);
            
            const closeAlert = (result) => {
                overlay.style.animation = 'fadeOut 0.2s ease-out';
                setTimeout(() => {
                    if (overlay.parentNode) {
                        overlay.remove();
                    }
                    resolve(result);
                }, 200);
            };
            
            const confirmBtn = overlay.querySelector('.custom-alert-btn-primary');
            const cancelBtn = overlay.querySelector('.custom-alert-btn-secondary');
            const closeBtn = overlay.querySelector('.custom-alert-close');
            
            confirmBtn.addEventListener('click', () => closeAlert(true));
            cancelBtn.addEventListener('click', () => closeAlert(false));
            closeBtn.addEventListener('click', () => closeAlert(false));
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) closeAlert(false);
            });
            
            setTimeout(() => confirmBtn.focus(), 100);
        });
    }
};

// Переопределяем стандартный alert
window.originalAlert = window.alert;
window.alert = function(message, title = 'Сообщение') {
    CustomAlert.info(message, title);
    return true;
};

// Глобальный доступ
window.CustomAlert = CustomAlert;

// Добавляем стиль для fadeOut
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);