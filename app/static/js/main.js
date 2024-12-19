function deleteLicitacion(id) {
    if (confirm('¿Está seguro de que desea eliminar esta licitación?')) {
        fetch(`/licitaciones/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Error al eliminar la licitación');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar la licitación');
        });
    }
}

// Función para inicializar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});