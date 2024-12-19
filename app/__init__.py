from flask import Flask
from flask_bootstrap import Bootstrap5
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    bootstrap = Bootstrap5(app)
    
    # Importar blueprints
    from app.routes import main, licitantes, proveedores, licitaciones, ofertas, bitacoras, gestion
    
    # Registrar blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(licitantes.bp)
    app.register_blueprint(proveedores.bp)
    app.register_blueprint(licitaciones.bp)
    app.register_blueprint(ofertas.bp)
    app.register_blueprint(bitacoras.bp)
    app.register_blueprint(gestion.bp)
    
    return app