# CSV2ZebraLabel

Web application for generating and printing Zebra labels (ZPL) from CSV or Excel files.

## Features

- CSV and Excel file import
- ZPL label template management
- Label preview via Labelary API
- Zebra printer management
- Single or multiple printing
- Modern and responsive interface with Bulma CSS
- Multilingual support (French, English)

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser
- Zebra printer or emulator

## Installation

### Option A - Using Docker (Recommended)

See [README-DOCKER.md](README-DOCKER.md) for detailed Docker installation instructions.
Docker image is available on Docker Hub: `ralphi2811/csv2zebralabel:latest`

A `docker-compose.yml` file is provided for easy deployment:
```bash
docker-compose up -d
```

### Option B - Local Installation

1. Clone the repository:
```bash
git clone https://github.com/ralphi2811/CSV2ZebraLabel.git
cd CSV2ZebraLabel
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python run.py
```

2. Access the web interface:
- Open your browser
- Go to `http://localhost:5000`

## Printer Emulator (for testing)

A Zebra printer emulator is included to facilitate testing:

1. Install emulator dependencies:
```bash
cd zebra_emulator
pip install -r requirements.txt
```

2. Start the emulator:
```bash
python zebra_server.py
```

The emulator will listen on port 9100 and display received ZPL codes.

## User Guide

### 1. Template Management

- Click on "New Template"
- Fill in the information:
  - Template name
  - Dimensions (width x height)
  - DPI (8, 12, or 24)
  - ZPL code with variables ($1, $2, etc.)

### 2. Printer Configuration

- Click on "New Printer"
- Fill in the information:
  - Printer name
  - IP address
  - Port (default: 9100)

### 3. Data Import

- Drag and drop a CSV/Excel file
- Columns are automatically detected
- Template variables ($1, $2, etc.) correspond to column order

### 4. Printing

- Select a label template
- Select a printer
- Printing options:
  - Single print: print button per row
  - Multiple print: select multiple rows and use "Print Selection"

### 5. Preview

- Click on the "eye" icon to preview a label
- The preview shows:
  - Generated ZPL code
  - Visual label preview
  - Any errors

## Project Structure

```
CSV2ZebraLabel/
├── app/
│   ├── models/         # SQLAlchemy models
│   ├── static/         # Static assets (CSS, JS)
│   │   ├── css/       # CSS files
│   │   ├── js/        # JavaScript files
│   │   └── img/       # Images
│   ├── templates/      # HTML templates
│   ├── translations/   # Translation files
│   │   ├── en/        # English translations
│   │   └── fr/        # French translations
│   ├── utils.py       # Utilities
│   ├── routes.py      # Flask routes
│   └── __init__.py    # Flask configuration
├── zebra_emulator/    # Printer emulator
├── instance/         # SQLite database
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile        # Docker configuration
├── requirements.txt  # Python dependencies
└── run.py           # Entry point
```

## Development

### Database

SQLAlchemy models define three main tables:
- `Template`: Label templates
- `Printer`: Printer configuration
- `PrintHistory`: Print history

### REST API

The application exposes several REST endpoints:
- `/api/templates`: Template management
- `/api/printers`: Printer management
- `/api/preview`: Label preview
- `/api/print`: Label printing
- `/api/upload`: File import

### Translations

The application uses Flask-Babel for translation management. Translation files are located in the `app/translations/` folder.

To update translations:
```bash
# Extract strings to translate
pybabel extract -F babel.cfg -o app/translations/messages.pot .

# Update translation files
pybabel update -i app/translations/messages.pot -d app/translations

# Compile translations
pybabel compile -d app/translations
```

## License

MIT
