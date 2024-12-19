from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.api_service import APIService
from datetime import datetime

bp = Blueprint('ofertas', __name__, url_prefix='/ofertas')

@bp.route('/')
def index():
    ofertas = APIService.get_all('ofertas')
    
    # Obtener información de proveedores y licitaciones para mostrar nombres en lugar de IDs
    proveedores = {p['id']: p for p in APIService.get_all('proveedores')}
    licitaciones = {l['id']: l for l in APIService.get_all('licitaciones')}
    
    # Formatear las ofertas para la vista
    for oferta in ofertas:
        # Convertir la fecha a formato más legible
        fecha = datetime.fromisoformat(oferta['fecha_oferta'].replace('Z', '+00:00'))
        oferta['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
        
        # Agregar información del proveedor y licitación si está disponible
        proveedor = proveedores.get(oferta['proveedor_id'], {})
        oferta['proveedor_nombre'] = proveedor.get('nombre', f'Proveedor {oferta["proveedor_id"]}')
        
        licitacion = licitaciones.get(oferta['licitacion_id'], {})
        oferta['licitacion_titulo'] = licitacion.get('titulo', f'Licitación {oferta["licitacion_id"]}')
    
    return render_template('ofertas/index.html', ofertas=ofertas)

@bp.route('/<int:id>')
def detail(id):
    oferta = APIService.get_by_id('ofertas', id)
    if not oferta:
        flash('Oferta no encontrada', 'error')
        return redirect(url_for('ofertas.index'))
    
    # Obtener información adicional
    proveedor = APIService.get_by_id('proveedores', oferta['proveedor_id'])
    licitacion = APIService.get_by_id('licitaciones', oferta['licitacion_id'])
    
    # Formatear fecha
    fecha = datetime.fromisoformat(oferta['fecha_oferta'].replace('Z', '+00:00'))
    oferta['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
    
    return render_template('ofertas/detail.html', 
                         oferta=oferta,
                         proveedor=proveedor,
                         licitacion=licitacion)