from datetime import datetime
from app import db

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zpl_code = db.Column(db.Text, nullable=False)
    variables_count = db.Column(db.Integer, default=0)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    dpmm = db.Column(db.Integer, nullable=False)  # 8, 12, ou 24
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Printer(db.Model):
    __tablename__ = 'printers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, default=9100)
    status = db.Column(db.String(50), default='disconnected')
    last_connection = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PrintHistory(db.Model):
    __tablename__ = 'print_history'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    printer_id = db.Column(db.Integer, db.ForeignKey('printers.id'), nullable=False)
    print_data = db.Column(db.JSON, nullable=False)  # Données utilisées pour l'impression
    copies = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    template = db.relationship('Template', backref=db.backref('print_history', lazy=True))
    printer = db.relationship('Printer', backref=db.backref('print_history', lazy=True))
