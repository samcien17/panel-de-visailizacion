from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.api_service import APIService
from datetime import datetime

bp = Blueprint('licitantes', __name__, url_prefix='/licitantes')

@bp.route('/')
def index():
    licitantes = APIService.get_all('licitantes')
    
    # Formatear las fechas para cada licitante
    for licitante in licitantes:
        fecha = datetime.fromisoformat(licitante['fecha_registro'].replace('Z', '+00:00'))
        licitante['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
    
    return render_template('licitantes/index.html', licitantes=licitantes)

@bp.route('/<int:id>')
def detail(id):
    licitante = APIService.get_by_id('licitantes', id)
    if not licitante:
        flash('Licitante no encontrado', 'error')
        return redirect(url_for('licitantes.index'))
    
    # Formatear la fecha
    fecha = datetime.fromisoformat(licitante['fecha_registro'].replace('Z', '+00:00'))
    licitante['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
    
    # Obtener licitaciones relacionadas si existe un endpoint para ello
    # licitaciones = APIService.get_all(f'licitantes/{id}/licitaciones')
    
    return render_template('licitantes/detail.html', 
                         licitante=licitante)