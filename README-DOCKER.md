# Docker - CSV2ZebraLabel

This document explains how to use the CSV2ZebraLabel application with Docker.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Option A - Using Docker Hub Image:

You can use this optimized docker-compose.yml for the Docker Hub image:
```yaml
version: '3.8'

services:
  web:
    # Using the official Docker Hub image
    image: ralphi2811/csv2zebralabel:latest
    container_name: csv2zebralabel
    ports:
      - "5000:5000"
    volumes:
      # Volume for SQLite database persistence
      - db_data:/app/instance
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=production
      # Database configuration (SQLite by default)
      - DATABASE_URL=sqlite:///db.sqlite
    restart: unless-stopped

# Docker named volume definition for better management
volumes:
  db_data:
    name: csv2zebralabel_db
```

Then launch with:
```bash
docker compose up -d
```

2. Option B - Build Locally:
```bash
git clone https://github.com/ralphi2811/CSV2ZebraLabel.git
cd CSV2ZebraLabel
docker compose up -d --build
```

The application will be accessible at: http://localhost:5000

## Architecture

The application is containerized without the Zebra emulator (which is reserved for development testing):
- Flask application (port 5000)
- Persistent SQLite database

## Volume

- `./instance:/app/instance`: Persistent storage for SQLite database

## Useful Commands

### Start the application
```bash
docker compose up -d
```

### Stop the application
```bash
docker compose down
```

### View logs
```bash
docker compose logs -f
```

### Restart the application
```bash
docker compose restart
```

## Printer Configuration

To configure a printer in the application:
- Use the actual IP address of your Zebra printer
- The standard port is usually 9100
- Ensure the printer is accessible from the network where the Docker container is deployed

## Database Configuration

By default, the application uses SQLite as the database:
- The database file is stored in `./instance/db.sqlite`
- Data is persistent thanks to the mounted Docker volume
- No additional configuration is needed

To use another database (PostgreSQL, MySQL, etc.):
1. Modify the `DATABASE_URL` environment variable in `docker-compose.yml`
2. Format: `postgresql://user:password@host:port/dbname` or `mysql://user:password@host:port/dbname`
3. Make sure to install the necessary Python dependencies in the Dockerfile (psycopg2 for PostgreSQL, pymysql for MySQL)

## Important Notes

- The SQLite database is persistent thanks to the volume mounted in ./instance/
- The Zebra emulator is not included as it is intended for development only
- The application is configured to restart automatically in case of error
