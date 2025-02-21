# Docker - CSV2ZebraLabel

Ce document explique comment utiliser l'application CSV2ZebraLabel avec Docker.

## Prérequis

- Docker
- Docker Compose

## Installation

1. Option A - Utiliser l'image Docker Hub :
```bash
docker pull ralphi2811/csv2zebralabel:latest
docker compose up -d
```

2. Option B - Construire localement :
```bash
git clone https://github.com/ralphi2811/CSV2ZebraLabel.git
cd CSV2ZebraLabel
docker compose up -d --build
```

L'application sera accessible à l'adresse : http://localhost:5000

## Architecture

L'application est conteneurisée sans l'émulateur Zebra (qui est réservé aux tests en développement) :
- Application Flask (port 5000)
- Base de données SQLite persistante

## Volume

- `./instance:/app/instance` : Stockage persistant pour la base de données SQLite

## Commandes utiles

### Démarrer l'application
```bash
docker compose up -d
```

### Arrêter l'application
```bash
docker compose down
```

### Voir les logs
```bash
docker compose logs -f
```

### Redémarrer l'application
```bash
docker compose restart
```

## Configuration des imprimantes

Pour configurer une imprimante dans l'application :
- Utilisez l'adresse IP réelle de votre imprimante Zebra
- Le port standard est généralement 9100
- Assurez-vous que l'imprimante est accessible depuis le réseau où le conteneur Docker est déployé

## Configuration de la base de données

Par défaut, l'application utilise SQLite comme base de données :
- Le fichier de base de données est stocké dans `./instance/db.sqlite`
- Les données sont persistantes grâce au volume Docker monté
- Aucune configuration supplémentaire n'est nécessaire

Pour utiliser une autre base de données (PostgreSQL, MySQL, etc.) :
1. Modifiez la variable d'environnement `DATABASE_URL` dans le `docker-compose.yml`
2. Format : `postgresql://user:password@host:port/dbname` ou `mysql://user:password@host:port/dbname`
3. Assurez-vous d'installer les dépendances Python nécessaires dans le Dockerfile (psycopg2 pour PostgreSQL, pymysql pour MySQL)

## Notes importantes

- La base de données SQLite est persistante grâce au volume monté dans ./instance/
- L'émulateur Zebra n'est pas inclus car il est destiné uniquement au développement
- L'application est configurée pour redémarrer automatiquement en cas d'erreur
