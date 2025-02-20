import pandas as pd
import socket
from typing import Tuple, List, Dict, Any

def read_file_data(file) -> Tuple[List[str], List[List[Any]]]:
    """Lit un fichier CSV ou Excel et retourne les en-têtes et les données"""
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:  # Excel
        df = pd.read_excel(file)
    
    return df.columns.tolist(), df.values.tolist()

def send_to_printer(ip: str, port: int, zpl: str) -> bool:
    """Envoie le code ZPL à l'imprimante"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Timeout de 5 secondes
            s.connect((ip, port))
            s.send(zpl.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Erreur d'impression: {str(e)}")
        return False

def replace_variables(zpl: str, data: Dict[str, str]) -> str:
    """Remplace les variables dans le code ZPL avec les données"""
    result = zpl
    for i, value in data.items():
        result = result.replace(f"${i}", str(value))
    return result
