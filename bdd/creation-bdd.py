import pandas as pd
import sqlite3

# Chemins des fichiers
FREQ_PATH = 'nettoyage/frequentation-gares-clean.csv'
PROP_22 = 'nettoyage/proprete-en-gare-22-clean.csv'
PROP_23 = 'nettoyage/proprete-en-gare-23-clean.csv'
PROP_24 = 'nettoyage/proprete-en-gare-24-clean.csv'
DB_PATH = 'bdd/gares.db'

# Création de la base et des 2 tables
conn = sqlite3.connect(DB_PATH)

# La méthode cursor permet de créer un objet qui va nous permettre d'exécuter des requêtes SQL
# La méthode execute permet d'exécuter une requête SQL
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS Gare (
    ID_gare TEXT PRIMARY KEY,
    Nom_gare TEXT,
    Code_postal TEXT,
    Nb_voyageurs_2022 INTEGER,
    Nb_voyageurs_2023 INTEGER,
    Nb_voyageurs_2024 INTEGER,
    Nb_voyageurs_et_nonvoyageurs_2022 INTEGER,
    Nb_voyageurs_et_nonvoyageurs_2023 INTEGER,
    Nb_voyageurs_et_nonvoyageurs_2024 INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS ControleProprete (
    ID_gare TEXT PRIMARY KEY,
    Taux_nonconformites_2022 REAL,
    Taux_nonconformites_2023 REAL,
    Taux_nonconformites_2024 REAL,
    FOREIGN KEY(ID_gare) REFERENCES Gare(ID_gare)
)
''')

# Import des données de fréquentation
df_freq = pd.read_csv(FREQ_PATH, sep=';')

# Préparer les données pour l'insertion
gares = []
# iterows veut dire "itérer sur les lignes du DataFrame"
for _, row in df_freq.iterrows():
    gares.append((
        str(row['Code UIC']),
        row['Nom de la gare'],
        str(row['Code postal']),
        # Utiliser get pour éviter les erreurs, 0 veut dire "pas de données"
        int(row.get('Total Voyageurs 2022', 0)),
        int(row.get('Total Voyageurs 2023', 0)),
        int(row.get('Total Voyageurs 2024', 0)),
        int(row.get('Total Voyageurs + Non voyageurs 2022', 0)),
        int(row.get('Total Voyageurs + Non voyageurs 2023', 0)),
        int(row.get('Total Voyageurs + Non voyageurs 2024', 0))
    ))

# Insertion dans la table Gare en utilisant "INSERT OR REPLACE" pour éviter les doublons
c.executemany('''
INSERT OR REPLACE INTO Gare VALUES (?,?,?,?,?,?,?,?,?)
''', gares)

# Import des données de propreté
# Détails : on lit le fichier, on calcule le taux de non-conformité (100 - taux de conformité), et on retourne un DataFrame avec l'UIC et le taux de non-conformité
def get_nonconformite(path, annee):
    df = pd.read_csv(path, sep=';')
    df['UIC'] = df['UIC'].astype(str)
    df[f'Taux_nonconformites_{annee}'] = 100 - df['Taux de conformité moyen']
    return df[['UIC', f'Taux_nonconformites_{annee}']]

# Récupérer les taux de non-conformité pour chaque année
df22 = get_nonconformite(PROP_22, 2022)
df23 = get_nonconformite(PROP_23, 2023)
df24 = get_nonconformite(PROP_24, 2024)

# Fusion pour avoir un DataFrame complet avec les taux de non-conformité pour les 3 années
controle = pd.merge(df22, df23, on='UIC', how='outer')
controle = pd.merge(controle, df24, on='UIC', how='outer')
controle = controle.rename(columns={'UIC': 'ID_gare'})

# Remplacer les NaN par None pour que SQLite puisse les gérer correctement
controle = controle.where(pd.notnull(controle), None)

# Insertion dans la table ControleProprete en utilisant "INSERT OR REPLACE" pour éviter les doublons
c.executemany('''
INSERT OR REPLACE INTO ControleProprete VALUES (?,?,?,?)
''', controle.values.tolist())

conn.commit()
conn.close()

print('Base de données créée et remplie avec succès.')
