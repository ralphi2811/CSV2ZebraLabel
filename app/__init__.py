from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

# Initialisation de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation des extensions
    db.init_app(app)
    
    # Import et enregistrement des blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
    
    return app
