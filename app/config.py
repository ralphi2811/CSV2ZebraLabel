"""
Configuration de l'application
"""

# Version de l'application
APP_VERSION = "1.0.2"

# Configuration de la base de données
DATABASE_CONFIG = {
    'default_uri': 'sqlite:///db.sqlite'
}

# Configuration des imprimantes
PRINTER_CONFIG = {
    'default_port': 9100
}

# Configuration des étiquettes
LABEL_CONFIG = {
    'default_width': 4,  # pouces
    'default_height': 6,  # pouces
    'default_dpi': 8     # 8 dpmm (203 dpi)
}
