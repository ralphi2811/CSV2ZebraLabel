# CSV2ZebraLabel - Cahier des Charges

## Description du Projet
CSV2ZebraLabel est une application web permettant de générer et d'imprimer des étiquettes Zebra (ZPL) à partir de fichiers CSV ou Excel. L'application permet de gérer des modèles d'étiquettes ZPL et de les associer avec les données importées pour une impression unique ou en masse.

## Fonctionnalités Principales

### 1. Gestion des Modèles ZPL
- Création, modification et suppression de modèles ZPL
- Paramétrage des variables dans le modèle ($1, $2, $3, etc.)
- Association des variables avec les colonnes du fichier d'import
- Prévisualisation du modèle

### 2. Import de Données
- Support des fichiers CSV
- Support des fichiers Excel
- Validation automatique des colonnes
- Correspondance automatique avec les variables du modèle
- Gestion des colonnes excédentaires (ignorées)

### 3. Prévisualisation des Étiquettes
- Intégration avec l'API Labelary
- Prévisualisation en PNG pour chaque ligne de données
- Affichage moderne en modal/popup
- URL de l'API : `http://api.labelary.com/v1/printers/{dpmm}/labels/{width}x{height}/{index}/{zpl}`

### 4. Gestion des Imprimantes
- Configuration des imprimantes Zebra
- Gestion des paramètres IP
- Test de connexion
- Statut de l'imprimante

### 5. Impression
- Impression unique par ligne avec nombre de copies configurable
- Impression en masse avec nombre de copies par étiquette
- File d'attente d'impression
- Historique des impressions avec détail des quantités

## Interface Utilisateur

### Page Principale
1. Zone d'import de fichiers
   - Glisser-déposer
   - Sélection de fichier
   - Validation du format

2. Tableau des Données
   - Affichage des lignes importées
   - Bouton de prévisualisation par ligne
   - Bouton d'impression par ligne avec champ quantité
   - Sélection multiple pour impression en masse avec quantités configurables

3. Gestion des Modèles
   - Liste des modèles disponibles
   - Éditeur de modèle
   - Configuration des variables

4. Configuration des Imprimantes
   - Liste des imprimantes
   - Paramètres de connexion
   - État de la connexion

## Gestion des Données

### Structure de la Base de Données

1. Table Modèles
   - ID
   - Nom
   - Code ZPL
   - Nombre de variables
   - Dimensions (largeur x hauteur)
   - DPI/DPMM
   - Date de création/modification

2. Table Imprimantes
   - ID
   - Nom
   - Adresse IP
   - Port
   - État
   - Date dernière connexion

3. Table Historique
   - ID
   - Date d'impression
   - Modèle utilisé
   - Imprimante utilisée
   - Données imprimées
   - Nombre de copies
   - Statut

## Spécifications Techniques

### Technologies
- Frontend : 
  - HTML5, JavaScript moderne
  - Framework CSS : Bulma
  - Composants réactifs avec Bulma modals, cards, et tables
- Backend : 
  - Python avec Flask
  - Templates Jinja2 pour le rendu serveur
  - Serveur de développement : Flask built-in server
  - Serveur de production : Gunicorn
- Base de données : SQLite pour le développement, PostgreSQL pour la production
- API RESTful pour la communication client-serveur

### Sécurité
- Validation des entrées
- Sanitization des données
- Protection contre les injections
- Gestion des erreurs

### Performance
- Optimisation des requêtes
- Mise en cache des prévisualisations
- Gestion asynchrone des impressions
- Limitation de la taille des fichiers d'import

## API et Intégrations

### API Labelary
- Endpoint : `http://api.labelary.com/v1/printers/{dpmm}/labels/{width}x{height}/{index}/{zpl}`
- Paramètres :
  - dpmm : Densité de l'imprimante (8, 12, 24)
  - width : Largeur de l'étiquette
  - height : Hauteur de l'étiquette
  - index : Index de l'étiquette
  - zpl : Code ZPL encodé

### Communication Imprimante
- Protocole : TCP/IP
- Port standard : 9100
- Format : ZPL II
- Gestion des erreurs et statuts

## Évolutions Futures Possibles
- Support d'autres formats d'import (JSON, XML)
- Interface mobile responsive
- Mode hors ligne
- Export des statistiques d'impression
- Gestion des utilisateurs et des droits
- API publique pour intégration externe
