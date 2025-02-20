# Émulateur d'Imprimante Zebra

Un émulateur simple d'imprimante Zebra qui écoute sur le port TCP 9100 et simule la réception d'impressions ZPL.

## Fonctionnalités

- Écoute sur le port TCP 9100 (port standard Zebra)
- Accepte les connexions entrantes
- Reçoit et affiche le code ZPL
- Simule une réponse positive d'impression
- Logging détaillé des opérations

## Utilisation

1. Assurez-vous d'avoir Python 3.x installé

2. Lancez l'émulateur :
```bash
python3 zebra_server.py
```

L'émulateur écoutera sur toutes les interfaces (0.0.0.0) sur le port 9100.

## Test

Pour tester l'émulateur, vous pouvez utiliser netcat pour envoyer du code ZPL :

```bash
echo "^XA^FO50,50^A0N,50,50^FDHello World^FS^XZ" | nc localhost 9100
```

## Logs

L'émulateur enregistre toutes les opérations dans la console avec horodatage.
