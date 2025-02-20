#!/usr/bin/env python3
import socket
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ZebraEmulator:
    def __init__(self, host='0.0.0.0', port=9100):
        """
        Initialise l'émulateur d'imprimante Zebra
        :param host: Adresse d'écoute (0.0.0.0 pour toutes les interfaces)
        :param port: Port d'écoute (9100 par défaut pour les imprimantes Zebra)
        """
        self.host = host
        self.port = port
        self.socket = None
        
    def start(self):
        """Démarre le serveur d'émulation"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permet la réutilisation de l'adresse
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            logger.info(f"Émulateur Zebra démarré sur {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                logger.info(f"Nouvelle connexion de {address}")
                self.handle_client(client_socket, address)
                
        except Exception as e:
            logger.error(f"Erreur serveur: {e}")
            if self.socket:
                self.socket.close()
                
    def handle_client(self, client_socket, address):
        """
        Gère une connexion client
        :param client_socket: Socket du client
        :param address: Adresse du client
        """
        try:
            # Reçoit les données ZPL
            data = client_socket.recv(4096)
            if data:
                # Décode les données reçues
                zpl_data = data.decode('utf-8', errors='ignore')
                logger.info(f"ZPL reçu de {address}:")
                logger.info(zpl_data)
                
                # Simule un traitement
                logger.info("Simulation du traitement de l'impression...")
                
                # Envoie une réponse positive
                response = "^RS,1,1\r\n"  # Statut OK en format Zebra
                client_socket.send(response.encode())
                logger.info("Réponse envoyée: Impression simulée avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement du client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connexion fermée avec {address}")

if __name__ == "__main__":
    # Crée et démarre l'émulateur
    emulator = ZebraEmulator()
    try:
        emulator.start()
    except KeyboardInterrupt:
        logger.info("Arrêt de l'émulateur...")
        if emulator.socket:
            emulator.socket.close()
