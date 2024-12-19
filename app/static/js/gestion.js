let licitanteModal = null;

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el modal
    licitanteModal = new bootstrap.Modal(document.getElementById('licitanteModal'));
    
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

// Función para mostrar el modal de nuevo licitante
function showLicitanteForm() {
    // Limpiar el formulario
    document.getElementById('licitanteForm').reset();
    // Cambiar el título del modal
    document.querySelector('#licitanteModal .modal-title').textContent = 'Nuevo Licitante';
    // Mostrar el modal
    licitanteModal.show();
}

// Función para guardar licitante
async function guardarLicitante(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch('/gestion/crear/licitante', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            licitanteModal.hide();
            // Recargar la página para mostrar el nuevo licitante
            window.location.reload();
        } else {
            alert(result.message || 'Error al guardar el licitante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al guardar el licitante');
    }
}

// Función para editar licitante
async function editarLicitante(id) {
    try {
        const response = await fetch(`/api/licitantes/${id}`);
        const licitante = await response.json();
        
        // Llenar el formulario con los datos
        document.getElementById('nombre').value = licitante.nombre;
        document.getElementById('correo').value = licitante.correo;
        document.getElementById('telefono').value = licitante.telefono;
        document.getElementById('direccion').value = licitante.direccion;
        
        // Cambiar el título del modal
        document.querySelector('#licitanteModal .modal-title').textContent = 'Editar Licitante';
        
        // Modificar el formulario para la edición
        const form = document.getElementById('licitanteForm');
        form.onsubmit = (e) => guardarEdicionLicitante(e, id);
        
        // Mostrar el modal
        licitanteModal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los datos del licitante');
    }
}

// Función para guardar la edición de un licitante
async function guardarEdicionLicitante(event, id) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`/gestion/actualizar/licitante/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            licitanteModal.hide();
            window.location.reload();
        } else {
            alert(result.message || 'Error al actualizar el licitante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar el licitante');
    }
}

// Función para eliminar licitante
async function eliminarLicitante(id) {
    if (!confirm('¿Está seguro de que desea eliminar este licitante?')) {
        return;
    }
    
    try {
        const response = await fetch(`/gestion/eliminar/licitante/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            window.location.reload();
        } else {
            alert(result.message || 'Error al eliminar el licitante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar el licitante');
    }
}