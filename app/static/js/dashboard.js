document.addEventListener('DOMContentLoaded', function() {
    // Función para formatear números con separadores de miles
    function formatNumber(num) {
        return new Intl.NumberFormat('es-MX').format(num);
    }
    
    // Función para formatear moneda
    function formatCurrency(amount) {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(amount);
    }

    // Actualización en tiempo real de las estadísticas
    function updateStats() {
        fetch('/api/dashboard/stats')
            .then(response => response.json())
            .then(data => {
                // Actualizar números con animación
                document.querySelectorAll('.stat-number').forEach(el => {
                    const target = parseInt(el.dataset.target);
                    const current = parseInt(el.textContent);
                    const increment = target / 20;
                    if(current < target) {
                        el.textContent = Math.ceil(current + increment);
                        setTimeout(() => requestAnimationFrame(updateStats), 50);
                    }
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // Inicialización de tooltips
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Manejador para el hover en las cards de estadísticas
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.querySelector('.stat-number').classList.add('highlight');
        });
        
        card.addEventListener('mouseleave', function() {
            this.querySelector('.stat-number').classList.remove('highlight');
        });
    });

    // Función para actualizar gráficos en tiempo real
    function updateCharts() {
        const charts = {
            ofertas: window.ofertasChart,
            actividad: window.actividadChart
        };

        fetch('/api/dashboard/chart-data')
            .then(response => response.json())
            .then(data => {
                Object.keys(charts).forEach(chartKey => {
                    if (charts[chartKey]) {
                        charts[chartKey].data.datasets[0].data = data[chartKey];
                        charts[chartKey].update();
                    }
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // Configuración de los observers para lazy loading
    const observerOptions = {
        root: null,
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chart = entry.target;
                if (chart.dataset.chart && !chart.classList.contains('initialized')) {
                    initializeChart(chart);
                    chart.classList.add('initialized');
                }
            }
        });
    }, observerOptions);

    // Observar elementos de gráficos
    document.querySelectorAll('[data-chart]').forEach(chart => {
        observer.observe(chart);
    });

    // Inicializar tablas con ordenamiento
    document.querySelectorAll('.table-sortable').forEach(table => {
        new Tablesort(table);
    });

    // Actualizaciones periódicas
    setInterval(updateStats, 60000); // Cada minuto
    setInterval(updateCharts, 300000); // Cada 5 minutos
});

// Función para manejar el resize de los gráficos
window.addEventListener('resize', function() {
    if (window.ofertasChart) {
        window.ofertasChart.resize();
    }
    if (window.actividadChart) {
        window.actividadChart.resize();
    }
});