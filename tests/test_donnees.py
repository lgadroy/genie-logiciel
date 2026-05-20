import pandas as pd

from bdd.creation_bdd import (ajouter_zero_code_postal,get_nonconformite)


# Test ajout du zéro au code postal
def test_ajouter_zero_code_postal():

    assert ajouter_zero_code_postal("7500") == "07500"
    assert ajouter_zero_code_postal("13001") == "13001"


# Test avec une valeur vide
def test_code_postal_vide():

    resultat = ajouter_zero_code_postal(None)

    assert resultat is None


# Test de get_nonconformite
def test_get_nonconformite(tmp_path):

    # creation d un faux csv
    fichier = tmp_path / "test.csv"

    # creation de donnée, une gare avec un taux de conformite
    df = pd.DataFrame({
        "UIC": ["12345"],
        "Taux de conformité moyen": [80]
    })

    df.to_csv(fichier, sep=';', index=False)

    resultat = get_nonconformite(fichier, 2024)

    # verifie le resultat du calcul
    assert resultat.iloc[0]["Taux_nonconformites_2024"] == 20