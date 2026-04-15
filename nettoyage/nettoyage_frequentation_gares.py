import pandas as pd

# Charger le fichier CSV chemin absolu
input_path = "nettoyage/frequentation-gares.csv"
df = pd.read_csv(input_path, sep=';', dtype=str)

# Colonnes à supprimer
colonnes_a_supprimer = [
    'Direction Régionale Gares',
    'Segmentation DRG',
    'Segmentation Marketing'
]

# Colonnes voyageurs à supprimer (avant 2022)
colonnes_voyageurs_a_supprimer = [
    col for col in df.columns 
    if (col.startswith('Total Voyageurs') or col.startswith('Total Voyageurs + Non voyageurs'))
    and (
        '2021' in col or '2020' in col or '2019' in col or '2018' in col or '2017' in col or '2016' in col or '2015' in col
    )
]

# Supprimer les colonnes
colonnes_finales = [col for col in df.columns if col not in colonnes_a_supprimer + colonnes_voyageurs_a_supprimer]
df_clean = df[colonnes_finales]

# Sauvegarder le fichier nettoyé
output_path = "nettoyage/frequentation-gares-clean.csv"
df_clean.to_csv(output_path, sep=';', index=False)

print(f"Fichier nettoyé sauvegardé sous : {output_path}")
