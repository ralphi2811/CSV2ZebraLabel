# CSV2ZebraLabel

Application web permettant de générer et d'imprimer des étiquettes Zebra (ZPL) à partir de fichiers CSV ou Excel.

## Fonctionnalités

- Import de fichiers CSV et Excel
- Gestion des modèles d'étiquettes ZPL
- Prévisualisation des étiquettes via l'API Labelary
- Gestion des imprimantes Zebra
- Impression unique ou multiple
- Interface moderne et réactive avec Bulma CSS
- Support multilingue (Français, Anglais)

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne
- Imprimante Zebra ou émulateur

## Installation

### Option A - Utilisation avec Docker (Recommandé)

Voir [README-DOCKER.md](README-DOCKER.md) pour les instructions détaillées d'installation avec Docker.
L'image Docker est disponible sur Docker Hub : `ralphi2811/csv2zebralabel:latest`

Un fichier `docker-compose.yml` est fourni pour faciliter le déploiement :
```bash
docker-compose up -d
```

### Option B - Installation locale

1. Cloner le dépôt :
```bash
git clone https://github.com/ralphi2811/CSV2ZebraLabel.git
cd CSV2ZebraLabel
```

2. Créer un environnement virtuel et l'activer :
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Démarrer l'application :
```bash
python run.py
```

2. Accéder à l'interface web :
- Ouvrir votre navigateur
- Aller à `http://localhost:5000`

## Émulateur d'imprimante (pour les tests)

Un émulateur d'imprimante Zebra est inclus pour faciliter les tests :

1. Installer les dépendances de l'émulateur :
```bash
cd zebra_emulator
pip install -r requirements.txt
```

2. Lancer l'émulateur :
```bash
python zebra_server.py
```

L'émulateur écoutera sur le port 9100 et affichera les codes ZPL reçus.

## Guide d'utilisation

### 1. Gestion des modèles

- Cliquer sur "Nouveau modèle"
- Remplir les informations :
  - Nom du modèle
  - Dimensions (largeur x hauteur)
  - DPI (8, 12, ou 24)
  - Code ZPL avec variables ($1, $2, etc.)

### 2. Configuration des imprimantes

- Cliquer sur "Nouvelle imprimante"
- Remplir les informations :
  - Nom de l'imprimante
  - Adresse IP
  - Port (par défaut : 9100)

### 3. Import de données

- Glisser-déposer un fichier CSV/Excel
- Les colonnes sont automatiquement détectées
- Les variables du modèle ($1, $2, etc.) correspondent à l'ordre des colonnes

### 4. Impression

- Sélectionner un modèle d'étiquette
- Sélectionner une imprimante
- Options d'impression :
  - Impression unique : bouton d'impression par ligne
  - Impression multiple : sélectionner plusieurs lignes et utiliser "Imprimer la sélection"

### 5. Prévisualisation

- Cliquer sur l'icône "œil" pour prévisualiser une étiquette
- La prévisualisation montre :
  - Le code ZPL généré
  - L'aperçu visuel de l'étiquette
  - Les éventuelles erreurs

## Structure du projet

```
CSV2ZebraLabel/
├── app/
│   ├── models/         # Modèles SQLAlchemy
│   ├── static/         # Assets statiques (CSS, JS)
│   │   ├── css/       # Fichiers CSS
│   │   ├── js/        # Fichiers JavaScript
│   │   └── img/       # Images
│   ├── templates/      # Templates HTML
│   ├── translations/   # Fichiers de traduction
│   │   ├── en/        # Traductions anglaises
│   │   └── fr/        # Traductions françaises
│   ├── utils.py       # Utilitaires
│   ├── routes.py      # Routes Flask
│   └── __init__.py    # Configuration Flask
├── zebra_emulator/    # Émulateur d'imprimante
├── instance/         # Base de données SQLite
├── docker-compose.yml # Configuration Docker Compose
├── Dockerfile        # Configuration Docker
├── requirements.txt  # Dépendances Python
└── run.py           # Point d'entrée
```

## Développement

### Base de données

Les modèles SQLAlchemy définissent trois tables principales :
- `Template` : Modèles d'étiquettes
- `Printer` : Configuration des imprimantes
- `PrintHistory` : Historique des impressions

### API REST

L'application expose plusieurs endpoints REST :
- `/api/templates` : Gestion des modèles
- `/api/printers` : Gestion des imprimantes
- `/api/preview` : Prévisualisation des étiquettes
- `/api/print` : Impression d'étiquettes
- `/api/upload` : Import de fichiers

### Traductions

L'application utilise Flask-Babel pour la gestion des traductions. Les fichiers de traduction se trouvent dans le dossier `app/translations/`.

Pour mettre à jour les traductions :
```bash
# Extraire les chaînes à traduire
pybabel extract -F babel.cfg -o app/translations/messages.pot .

# Mettre à jour les fichiers de traduction
pybabel update -i app/translations/messages.pot -d app/translations

# Compiler les traductions
pybabel compile -d app/translations
```

## Licence

MIT
