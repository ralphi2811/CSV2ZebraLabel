from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from app.models import Template, Printer, PrintHistory
from app.utils import read_file_data, send_to_printer, replace_variables
from app import db
import requests
import json
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page principale de l'application"""
    return render_template('index.html')

@main_bp.route('/zpl-doc')
def zpl_doc():
    """Documentation du langage ZPL"""
    return render_template('zpl_doc.html')

@main_bp.route('/print-history')
def print_history():
    """Historique des impressions"""
    history = PrintHistory.query.order_by(PrintHistory.created_at.desc()).all()
    return render_template('print_history.html', history=history)

@main_bp.route('/change-lang/<lang>')
def change_lang(lang):
    """Change la langue de l'interface"""
    session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/api/templates', methods=['GET', 'POST', 'DELETE'])
def handle_templates():
    """Gestion des modèles ZPL"""
    if request.method == 'POST':
        data = request.json
        template = Template(
            name=data['name'],
            zpl_code=data['zpl_code'],
            variables_count=data['variables_count'],
            width=data['width'],
            height=data['height'],
            dpmm=data['dpmm']
        )
        db.session.add(template)
        db.session.commit()
        return jsonify({"id": template.id, "message": "Modèle créé avec succès"})
    
    templates = Template.query.all()
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "variables_count": t.variables_count,
        "width": t.width,
        "height": t.height,
        "dpmm": t.dpmm,
        "zpl_code": t.zpl_code
    } for t in templates])

@main_bp.route('/api/preview', methods=['POST'])
def preview_label():
    """Prévisualisation d'une étiquette via l'API Labelary"""
    data = request.json
    
    if not data:
        return jsonify({"success": False, "error": "Données manquantes"}), 400

    # Récupération du template et de ses paramètres
    template_id = data.get('template_id')
    if template_id:
        template = Template.query.get_or_404(template_id)
        zpl = template.zpl_code
        dpmm = template.dpmm
        width = template.width
        height = template.height
    else:
        # Cas de la prévisualisation directe depuis l'éditeur
        template_data = data.get('template')
        if not template_data:
            return jsonify({"success": False, "error": "Données du template manquantes"}), 400
        zpl = template_data['zpl_code']
        dpmm = template_data['dpmm']
        width = template_data['width']
        height = template_data['height']

    # Remplacement des variables si présentes
    if 'data' in data:
        zpl = replace_variables(zpl, data['data'])
    
    try:
        response = requests.post(
            f'http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{width}x{height}/0/',
            headers={'Accept': 'image/png'},
            data=zpl.encode('utf-8')
        )
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "image": response.content.decode('latin1')
            })
        return jsonify({
            "success": False,
            "error": "Erreur lors de la génération de l'aperçu"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@main_bp.route('/api/templates/<int:template_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_template(template_id):
    """Gestion d'un modèle spécifique"""
    template = Template.query.get_or_404(template_id)
    
    if request.method == 'GET':
        return jsonify({
            "id": template.id,
            "name": template.name,
            "variables_count": template.variables_count,
            "width": template.width,
            "height": template.height,
            "dpmm": template.dpmm,
            "zpl_code": template.zpl_code
        })
    
    elif request.method == 'PUT':
        data = request.json
        template.name = data['name']
        template.zpl_code = data['zpl_code']
        template.variables_count = data['variables_count']
        template.width = data['width']
        template.height = data['height']
        template.dpmm = data['dpmm']
        db.session.commit()
        return jsonify({"success": True, "message": "Modèle mis à jour avec succès"})
    
    elif request.method == 'DELETE':
        db.session.delete(template)
        db.session.commit()
        return jsonify({"success": True, "message": "Modèle supprimé avec succès"})

@main_bp.route('/api/printers', methods=['GET', 'POST', 'DELETE'])
def handle_printers():
    """Gestion des imprimantes"""
    if request.method == 'POST':
        data = request.json
        printer = Printer(
            name=data['name'],
            ip_address=data['ip_address'],
            port=data.get('port', 9100)
        )
        db.session.add(printer)
        db.session.commit()
        return jsonify({"id": printer.id, "message": "Imprimante ajoutée avec succès"})
    
    printers = Printer.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "ip_address": p.ip_address,
        "port": p.port,
        "status": p.status
    } for p in printers])

@main_bp.route('/api/printers/<int:printer_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_printer(printer_id):
    """Gestion d'une imprimante spécifique"""
    printer = Printer.query.get_or_404(printer_id)
    
    if request.method == 'GET':
        return jsonify({
            "id": printer.id,
            "name": printer.name,
            "ip_address": printer.ip_address,
            "port": printer.port,
            "status": printer.status
        })
    
    elif request.method == 'PUT':
        data = request.json
        printer.name = data['name']
        printer.ip_address = data['ip_address']
        printer.port = data.get('port', 9100)
        db.session.commit()
        return jsonify({"success": True, "message": "Imprimante mise à jour avec succès"})
    
    elif request.method == 'DELETE':
        db.session.delete(printer)
        db.session.commit()
        return jsonify({"success": True, "message": "Imprimante supprimée avec succès"})

@main_bp.route('/api/upload', methods=['POST'])
def upload_file():
    """Traitement des fichiers CSV/Excel"""
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été envoyé"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Aucun fichier n'a été sélectionné"}), 400
    
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        return jsonify({"error": "Format de fichier non supporté"}), 400
    
    # Récupération du paramètre include_header (par défaut True)
    include_header = request.form.get('include_header', 'true').lower() == 'true'
    
    try:
        headers, rows = read_file_data(file, include_header)
        return jsonify({
            "success": True,
            "headers": headers,
            "rows": rows
        })
    except Exception as e:
        return jsonify({"error": f"Erreur lors du traitement du fichier: {str(e)}"}), 500

@main_bp.route('/api/print', methods=['POST'])
def print_label():
    """Impression d'étiquettes"""
    data = request.json
    template_id = data['template_id']
    printer_id = data['printer_id']
    print_data = data['data']
    copies = data.get('copies', 1)
    
    template = Template.query.get_or_404(template_id)
    printer = Printer.query.get_or_404(printer_id)
    
    # Génération du ZPL avec les variables remplacées
    zpl = replace_variables(template.zpl_code, print_data)
    
    # Tentative d'impression
    success = send_to_printer(printer.ip_address, printer.port, zpl)
    
    if not success:
        return jsonify({
            "success": False,
            "message": "Erreur lors de l'envoi à l'imprimante"
        }), 500
    
    # Enregistrement dans l'historique
    history = PrintHistory(
        template_id=template_id,
        printer_id=printer_id,
        print_data=print_data,
        copies=copies,
        status='completed' if success else 'failed'
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Impression envoyée avec succès",
        "history_id": history.id
    })

@main_bp.route('/api/print-history/<int:history_id>', methods=['GET'])
def get_print_history(history_id):
    """Récupération des détails d'un historique d'impression"""
    history = PrintHistory.query.get_or_404(history_id)
    return jsonify({
        "id": history.id,
        "template_id": history.template_id,
        "printer_id": history.printer_id,
        "print_data": history.print_data,
        "copies": history.copies,
        "status": history.status,
        "created_at": history.created_at.isoformat()
    })

@main_bp.route('/api/print-history/purge', methods=['DELETE'])
def purge_print_history():
    """Purge de l'historique des impressions"""
    try:
        PrintHistory.query.delete()
        db.session.commit()
        return jsonify({"success": True, "message": "Historique purgé avec succès"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
