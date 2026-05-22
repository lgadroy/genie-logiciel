# Projet GÉNIE-LOGICIEL

## Interface web pour la visualisation de jeux de données

### Description du projet

Cette application web permet de visualiser des données sur les gares françaises, notamment :

- la fréquentation des gares en 2022, 2023 et 2024,
- la propreté des gares mesurée par le taux de non-conformités pour 2022, 2023 et 2024,
- des pages de synthèse, de carte et de statistiques.

L'application utilise une base de données SQLite (`bdd/gares.db`) et un backend Flask pour générer les pages et les données.

### Fonctionnalités principales

- Page d'accueil avec des indicateurs clés (nombre de gares, nombre de départements, moyenne de propreté, gare la plus propre, gare la plus fréquentée).
- Page de carte pour visualiser les données géographiques.
- Page de détail de gare.
- Page de chiffres et statistiques par année.
- API interne disponible sur `/api/gares` pour récupérer les données de gares au format JSON.

## Installation et exécution

### Prérequis

- Python 3.10 ou supérieur
- `pip`

### Étapes d'installation (Windows)

1. Cloner le dépôt :

```bash
git clone https://github.com/lgadroy/genie-logiciel.git
cd genie-logiciel
```

2. Créer et activer un environnement virtuel (recommandé) :

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate.bat
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Préparer les données et la base :

- Le script `build.py` exécute les étapes de nettoyage et crée/met à jour la base SQLite.
- Exécutez :

```bash
python build.py
```

5. Lancer l'application :

```bash
python app.py
```

6. Ouvrir le navigateur et aller à :

```text
http://127.0.0.1:5000
```

### Architecture

```
genie-logiciel/
├── app.py
├── build.py
├── requirements.txt
├── bdd/
│   ├── creation_bdd.py
│   └── gares.db
├── nettoyage/
│   ├── frequentation-gares.csv
│   ├── nettoyage_frequentation_gares.py
│   ├── nettoyage_proprete_gare.py
│   ├── traitement_donnees.py
│   ├── proprete-en-gare-22.csv
│   ├── proprete-en-gare-23.csv
│   └── proprete-en-gare-24.csv
├── static/
│   ├── CSS/
│   │   └── style.css
│   ├── data/
│   │   └── departements.geojson
│   └── JS/
│       └── map.js
├── templates/
│   ├── carte.html
│   ├── chiffre.html
│   ├── gare.html
│   ├── header&footer.html
│   └── home.html
├── tests/
│   ├── test_donnees.py
│   └── test_routes.py
└── README.MD
```

## Commandes Git utiles

```bash
git add .
git commit -m "message du commit"
git push
git pull
```

## Notes
- `sqlite3` est utilisé en interne, mais vous n'avez pas besoin de l'installer séparément avec Python standard.

## Équipe projet

| Nom                         | Email                                             |
| --------------------------- | ------------------------------------------------- |
| Louis GUERY                 | louis.guery9@etu.univ-lorraine.fr                 |
| Leo GADROY                  | leo.gadroy9@etu.univ-lorraine.fr                  |
| Mariam ZAIM MOUNAJED        | mariam.zaim-mounajed3@etu.univ-lorraine.fr        |
| Dounia KHALFOUNI            | dounia.khalfouni4@etu.univ-lorraine.fr            |
| Mélissandre LOS             | melissandre.los9@etu.univ-lorraine.fr             |
| Maha EL OUATRI              | maha.el-ouatri1@etu.univ-lorraine.fr              |

_Projet développé dans le cadre du module Génie Logiciel._