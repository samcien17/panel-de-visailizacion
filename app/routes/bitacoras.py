from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.api_service import APIService
from datetime import datetime

bp = Blueprint('bitacoras', __name__, url_prefix='/bitacoras')

@bp.route('/')
def index():
    bitacoras = APIService.get_all('bitacoras')
    licitaciones = {l['id']: l for l in APIService.get_all('licitaciones')}
    
    # Procesar cada bitácora para incluir información adicional
    for bitacora in bitacoras:
        # Formatear fecha
        fecha = datetime.fromisoformat(bitacora['fecha'].replace('Z', '+00:00'))
        bitacora['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
        
        # Agregar información de la licitación relacionada
        licitacion = licitaciones.get(bitacora['licitacion_id'], {})
        bitacora['licitacion_info'] = licitacion
    
    return render_template('bitacoras/index.html', bitacoras=bitacoras)

@bp.route('/<int:id>')
def detail(id):
    bitacora = APIService.get_by_id('bitacoras', id)
    if not bitacora:
        flash('Bitácora no encontrada', 'error')
        return redirect(url_for('bitacoras.index'))
    
    # Formatear fecha
    fecha = datetime.fromisoformat(bitacora['fecha'].replace('Z', '+00:00'))
    bitacora['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
    
    # Obtener información de la licitación relacionada
    licitacion = APIService.get_by_id('licitaciones', bitacora['licitacion_id'])
    
    return render_template('bitacoras/detail.html',
                         bitacora=bitacora,
                         licitacion=licitacion)