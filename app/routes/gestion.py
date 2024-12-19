from flask import Blueprint, render_template, request, jsonify
from app.services.api_service import APIService
from datetime import datetime
import json

bp = Blueprint('gestion', __name__, url_prefix='/gestion')

@bp.route('/')
def index():
    try:
        licitantes = APIService.get_all('licitantes')
        print("Licitantes obtenidos:", licitantes)  # Debug
        return render_template('gestion/index.html', licitantes=licitantes)
    except Exception as e:
        print("Error al obtener licitantes:", str(e))  # Debug
        return render_template('gestion/index.html', licitantes=[])

@bp.route('/crear/licitante', methods=['POST'])
def crear_licitante():
    print("Recibiendo solicitud para crear licitante")  # Debug
    try:
        # Obtener y validar datos
        datos = request.get_json()
        print("Datos recibidos:", datos)  # Debug

        if not datos:
            return jsonify({"success": False, "message": "No se recibieron datos"}), 400

        # Preparar datos para la API
        licitante_data = {
            "nombre": datos.get('nombre'),
            "correo": datos.get('correo'),
            "telefono": datos.get('telefono'),
            "direccion": datos.get('direccion'),
            "fecha_registro": datetime.now().isoformat()
        }

        print("Datos a enviar a la API:", licitante_data)  # Debug

        # Crear licitante
        response = APIService.create('licitantes', licitante_data)
        print("Respuesta de la API:", response)  # Debug

        if response:
            return jsonify({"success": True, "data": response})
        return jsonify({"success": False, "message": "Error al crear el licitante"}), 400

    except Exception as e:
        print("Error al crear licitante:", str(e))  # Debug
        return jsonify({"success": False, "message": str(e)}), 500