from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.api_service import APIService
from datetime import datetime

bp = Blueprint('licitaciones', __name__, url_prefix='/licitaciones')

@bp.route('/')
def index():
    licitaciones = APIService.get_all('licitaciones')
    
    # Obtener todos los licitantes para mostrar sus nombres
    licitantes = {l['id']: l for l in APIService.get_all('licitantes')}
    
    for licitacion in licitaciones:
        # Formatear fechas
        fecha_inicio = datetime.fromisoformat(licitacion['fecha_inicio'].replace('Z', '+00:00'))
        fecha_fin = datetime.fromisoformat(licitacion['fecha_fin'].replace('Z', '+00:00'))
        
        licitacion['fecha_inicio_formateada'] = fecha_inicio.strftime('%d/%m/%Y %H:%M')
        licitacion['fecha_fin_formateada'] = fecha_fin.strftime('%d/%m/%Y %H:%M')
        
        # Agregar nombre del licitante
        licitante = licitantes.get(licitacion['licitante_id'], {})
        licitacion['licitante_nombre'] = licitante.get('nombre', f'Licitante {licitacion["licitante_id"]}')
        
        # Obtener conteo de ofertas
        ofertas = APIService.get_all(f'licitaciones/{licitacion["id"]}/ofertas')
        licitacion['total_ofertas'] = len(ofertas) if ofertas else 0
        
    return render_template('licitaciones/index.html', licitaciones=licitaciones)

@bp.route('/<int:id>')
def detail(id):
    licitacion = APIService.get_by_id('licitaciones', id)
    if not licitacion:
        flash('Licitación no encontrada', 'error')
        return redirect(url_for('licitaciones.index'))
    
    # Formatear fechas
    fecha_inicio = datetime.fromisoformat(licitacion['fecha_inicio'].replace('Z', '+00:00'))
    fecha_fin = datetime.fromisoformat(licitacion['fecha_fin'].replace('Z', '+00:00'))
    
    licitacion['fecha_inicio_formateada'] = fecha_inicio.strftime('%d/%m/%Y %H:%M')
    licitacion['fecha_fin_formateada'] = fecha_fin.strftime('%d/%m/%Y %H:%M')
    
    # Obtener información del licitante
    licitante = APIService.get_by_id('licitantes', licitacion['licitante_id'])
    
    # Obtener ofertas y bitácoras
    ofertas = APIService.get_all(f'licitaciones/{id}/ofertas')
    bitacoras = APIService.get_all(f'licitaciones/{id}/bitacoras')
    
    return render_template('licitaciones/detail.html',
                         licitacion=licitacion,
                         licitante=licitante,
                         ofertas=ofertas,
                         bitacoras=bitacoras)