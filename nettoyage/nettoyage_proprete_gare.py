import pandas as pd

# Années à traiter
years = ['22', '23', '24']

for year in years:
    # Chargement du fichier
    df = pd.read_csv(f'nettoyage/proprete-en-gare-{year}.csv', sep=';')

    # Calcul de la moyenne du taux de conformité par gare
    df_grouped = df.groupby(['UIC', 'Nom gare'], as_index=False)['Taux de conformité'].mean()

    # Renommer la colonne pour plus de clarté
    df_grouped = df_grouped.rename(columns={'Taux de conformité': 'Taux de conformité moyen'})

    # Arrondir la moyenne à 2 chiffres après la virgule
    df_grouped['Taux de conformité moyen'] = df_grouped['Taux de conformité moyen'].round(2)

    # Sauvegarde du résultat
    df_grouped.to_csv(f'nettoyage/proprete-en-gare-{year}-clean.csv', index=False, sep=';')
    print(f"Fichier pour {year} sauvegardé")
