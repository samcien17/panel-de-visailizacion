from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.api_service import APIService
from datetime import datetime

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@bp.route('/')
def index():
    proveedores = APIService.get_all('proveedores')
    
    # Formatear fechas y obtener ofertas relacionadas
    for proveedor in proveedores:
        fecha = datetime.fromisoformat(proveedor['fecha_registro'].replace('Z', '+00:00'))
        proveedor['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
        
        # Obtener el conteo de ofertas para cada proveedor
        ofertas = APIService.get_all(f'proveedores/{proveedor["id"]}/ofertas')
        proveedor['total_ofertas'] = len(ofertas) if ofertas else 0
    
    return render_template('proveedores/index.html', proveedores=proveedores)

@bp.route('/<int:id>')
def detail(id):
    proveedor = APIService.get_by_id('proveedores', id)
    if not proveedor:
        flash('Proveedor no encontrado', 'error')
        return redirect(url_for('proveedores.index'))
    
    # Formatear fecha
    fecha = datetime.fromisoformat(proveedor['fecha_registro'].replace('Z', '+00:00'))
    proveedor['fecha_formateada'] = fecha.strftime('%d/%m/%Y %H:%M')
    
    # Obtener ofertas del proveedor
    ofertas = APIService.get_all(f'proveedores/{id}/ofertas')
    
    return render_template('proveedores/detail.html', 
                         proveedor=proveedor,
                         ofertas=ofertas)