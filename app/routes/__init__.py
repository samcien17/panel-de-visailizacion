from app.routes.main import bp as main_bp
from app.routes.licitantes import bp as licitantes_bp
from app.routes.proveedores import bp as proveedores_bp
from app.routes.licitaciones import bp as licitaciones_bp
from app.routes.ofertas import bp as ofertas_bp
from app.routes.bitacoras import bp as bitacoras_bp
from app.routes.gestion import bp as gestion_bp

# Lista de todos los blueprints para facilitar el registro
blueprints = [
    main_bp,
    licitantes_bp,
    proveedores_bp,
    licitaciones_bp,
    ofertas_bp,
    bitacoras_bp,
    gestion_bp
]