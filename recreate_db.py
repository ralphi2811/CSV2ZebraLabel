from app import create_app, db

app = create_app()

with app.app_context():
    # Supprimer toutes les tables existantes
    db.drop_all()
    
    # Recréer les tables avec les nouvelles contraintes
    db.create_all()
    
    print("Base de données recréée avec succès!")
