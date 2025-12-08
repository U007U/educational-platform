document.addEventListener('DOMContentLoaded', function () {
    console.log('📊 Dashboard loaded');

    const token = localStorage.getItem('access_token');
    const userEmail = localStorage.getItem('userEmail');

    if (!token || !userEmail) {
        window.location.href = '/auth/login';  // ✅ На логин!
        return;
    }

    // Загрузка данных пользователя
    loadDashboardData();

    // Инициализация графика
    initProgressChart();

    // Загрузка курсов
    loadUserCourses();

    async function loadDashboardData() {
        try {
            // Получение статистики
            const stats = await window.apiRequest('/api/stats'); // Нужно создать endpoint
            if (stats.success) {
                updateStats(stats.data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    function updateStats(data) {
        document.getElementById('activeCourses').textContent = data.active_courses || 0;
        document.getElementById('completedLessons').textContent = data.completed_lessons || 0;
        document.getElementById('learningHours').textContent = data.learning_hours || 0;
        document.getElementById('achievements').textContent = data.achievements || 0;
    }

    async function loadUserCourses() {
        try {
            const response = await window.apiRequest('/api/users/me/courses'); // Нужно создать endpoint
            if (response.success) {
                renderCourses(response.data);
            }
        } catch (error) {
            console.error('Error loading courses:', error);
        }
    }

    function renderCourses(courses) {
        const container = document.getElementById('coursesList');
        if (!courses || courses.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-book-open"></i>
                    <p>Вы еще не записаны на курсы</p>
                </div>
            `;
            return;
        }

        container.innerHTML = courses.map(course => `
            <div class="course-item">
                <div class="course-info">
                    <h4>${course.title}</h4>
                    <p class="course-desc">${course.description.substring(0, 100)}...</p>
                    <div class="course-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${course.progress || 0}%"></div>
                        </div>
                        <span class="progress-text">${course.progress || 0}%</span>
                    </div>
                </div>
                <button class="btn btn-sm btn-outline" onclick="continueCourse(${course.id})">
                    Продолжить
                </button>
            </div>
        `).join('');
    }

    function initProgressChart() {
        const ctx = document.getElementById('progressCanvas').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                datasets: [{
                    label: 'Часы обучения',
                    data: [2, 3, 1, 4, 2, 3, 5],
                    borderColor: 'var(--primary-color)',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'var(--border-color)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'var(--border-color)'
                        }
                    }
                }
            }
        });
    }

    // Глобальные функции
    window.continueCourse = function (courseId) {
        showNotification('Переход к курсу...', 'info');
        setTimeout(() => {
            window.location.href = `/courses/${courseId}`;
        }, 500);
    };

    console.log('✅ Dashboard initialized');
});