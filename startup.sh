#!/bin/bash

echo "Exécution de build.py..."
python build.py

echo "Démarrage de l'application..."
gunicorn --bind=0.0.0.0 --timeout 600 app:app