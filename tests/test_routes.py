import pytest
from app import app


# creation du client de test Flask
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


# Test de la page d'accueil
def test_route_accueil():
    with app.test_client() as client:
        response = client.get('/')

        assert response.status_code == 200


# Test de la page carte
def test_route_carte():
    with app.test_client() as client:
        response = client.get('/carte')

        assert response.status_code == 200


# Test de la page chiffres
def test_route_chiffres():
    with app.test_client() as client:
        response = client.get('/chiffre')

        assert response.status_code == 200


