from flask import Blueprint, render_template
from app.services.api_service import APIService
from datetime import datetime
from collections import defaultdict

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Obtener todos los datos necesarios
    licitaciones = APIService.get_all('licitaciones')
    proveedores = APIService.get_all('proveedores')
    licitantes = APIService.get_all('licitantes')
    ofertas = APIService.get_all('ofertas')
    
    # Estadísticas generales
    stats = {
        'total_licitaciones': len(licitaciones),
        'total_proveedores': len(proveedores),
        'total_licitantes': len(licitantes),
        'total_ofertas': len(ofertas),
        'licitaciones_activas': sum(1 for l in licitaciones if l['estado'] == 'Abierta'),
        'promedio_ofertas': len(ofertas) / len(licitaciones) if licitaciones else 0
    }
    
    # Procesar licitaciones
    licitaciones_procesadas = []
    for licitacion in licitaciones:
        # Obtener ofertas de la licitación
        ofertas_licitacion = APIService.get_all(f'licitaciones/{licitacion["id"]}/ofertas')
        
        # Encontrar el licitante
        licitante = next((l for l in licitantes if l['id'] == licitacion['licitante_id']), None)
        
        # Formatear fechas
        fecha_inicio = datetime.fromisoformat(licitacion['fecha_inicio'].replace('Z', '+00:00'))
        fecha_fin = datetime.fromisoformat(licitacion['fecha_fin'].replace('Z', '+00:00'))
        
        licitacion_data = {
            **licitacion,
            'fecha_inicio_formateada': fecha_inicio.strftime('%d/%m/%Y %H:%M'),
            'fecha_fin_formateada': fecha_fin.strftime('%d/%m/%Y %H:%M'),
            'total_ofertas': len(ofertas_licitacion),
            'monto_mayor': max([o['monto_ofrecido'] for o in ofertas_licitacion], default=0),
            'monto_menor': min([o['monto_ofrecido'] for o in ofertas_licitacion], default=0),
            'licitante_nombre': licitante['nombre'] if licitante else 'Desconocido'
        }
        licitaciones_procesadas.append(licitacion_data)
    
    # Datos para gráficos
    chart_data = {
        'ofertas_por_estado': defaultdict(int),
        'licitaciones_por_estado': defaultdict(int),
        'ofertas_timeline': defaultdict(int)
    }
    
    for oferta in ofertas:
        chart_data['ofertas_por_estado'][oferta['estado']] += 1
        fecha = datetime.fromisoformat(oferta['fecha_oferta'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
        chart_data['ofertas_timeline'][fecha] += 1
    
    for licitacion in licitaciones:
        chart_data['licitaciones_por_estado'][licitacion['estado']] += 1
    
    return render_template('dashboard.html',
                         stats=stats,
                         chart_data=dict(chart_data),
                         licitaciones_recientes=sorted(licitaciones_procesadas, 
                                                     key=lambda x: x['fecha_inicio'], 
                                                     reverse=True)[:5],
                         ofertas_recientes=sorted(ofertas, 
                                                key=lambda x: x['fecha_oferta'], 
                                                reverse=True)[:5])