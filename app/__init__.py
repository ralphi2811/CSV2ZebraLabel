from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from pathlib import Path
import os
from app.config import APP_VERSION, DATABASE_CONFIG

# Initialisation des extensions
db = SQLAlchemy()
babel = Babel()

def get_locale():
    # Utiliser la langue stockée en session si elle existe
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(['en', 'fr'])

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuration Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']
    
    # Initialisation des extensions
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    # Ajouter la version de l'application aux templates
    @app.context_processor
    def inject_app_version():
        return {'app_version': APP_VERSION}
    
    # Import et enregistrement des blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
    
    return app
