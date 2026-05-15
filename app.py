from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('bdd/gares.db')
    c = conn.cursor()

    # Nombre total de gares dans la base
    c.execute("SELECT COUNT(*) FROM Gare")
    # fetchone() retourne une tuple, on prend le premier élément
    home_nombre_gares = c.fetchone()[0]

    # Nombre de départements différents représentés dans la base
    c.execute("SELECT COUNT(DISTINCT SUBSTR(Code_postal, 1, 2)) FROM Gare")
    home_nombre_departements = c.fetchone()[0]

    # Moyenne de propreté sur 2024, transformée en pourcentage lisible
    c.execute("""
        SELECT AVG(100 - Taux_nonconformites_2024)
        FROM ControleProprete
        WHERE Taux_nonconformites_2024 IS NOT NULL
    """)
    home_moyenne_proprete = c.fetchone()[0]
    home_moyenne_proprete = f"{home_moyenne_proprete:.2f}%"

    # Total des voyageurs en 2024
    c.execute("SELECT SUM(Nb_voyageurs_2024) FROM Gare WHERE Nb_voyageurs_2024 IS NOT NULL")
    home_total_voyageurs = c.fetchone()[0]
    # On formate le nombre total de voyageurs avec des espaces pour les milliers
    home_total_voyageurs = f"{int(home_total_voyageurs):,}".replace(',', ' ')

    # Gare la plus propre : on récupère son nom, son score et son département
    c.execute("""
        SELECT
            g.Nom_gare AS nom_gare,
            100 - cp.Taux_nonconformites_2024 AS score_proprete,
            SUBSTR(g.Code_postal, 1, 2) AS code_departement
        FROM Gare g
        JOIN ControleProprete cp ON g.ID_gare = cp.ID_gare
        WHERE cp.Taux_nonconformites_2024 IS NOT NULL
        ORDER BY score_proprete DESC
        LIMIT 1
    """)
    plus_propre = c.fetchone()
    home_gare_plus_propre = plus_propre[0]
    home_score_plus_propre = f"{plus_propre[1]:.1f}%"
    home_departement_plus_propre = plus_propre[2]

    # Gare la plus fréquentée : on récupère aussi son score de propreté
    c.execute("""
        SELECT Nom_gare, Nb_voyageurs_2024,
               (SELECT 100 - Taux_nonconformites_2024
                FROM ControleProprete cp
                WHERE cp.ID_gare = g.ID_gare)
        FROM Gare g
        WHERE Nb_voyageurs_2024 IS NOT NULL
        ORDER BY Nb_voyageurs_2024 DESC
        LIMIT 1
    """)
    frequentee = c.fetchone()
    home_gare_plus_frequentee = frequentee[0]
    home_nombre_voyageurs_plus_frequentee = f"{int(frequentee[1]):,}".replace(',', ' ')
    home_proprete_gare_plus_frequentee = f"{frequentee[2]:.2f}%"

    conn.close()

    return render_template(
        'home.html',
        home_nombre_gares=home_nombre_gares,
        home_nombre_departements=home_nombre_departements,
        home_moyenne_proprete=home_moyenne_proprete,
        home_total_voyageurs=home_total_voyageurs,
        home_gare_plus_propre=home_gare_plus_propre,
        home_score_plus_propre=home_score_plus_propre,
        home_departement_plus_propre=home_departement_plus_propre,
        home_gare_plus_frequentee=home_gare_plus_frequentee,
        home_nombre_voyageurs_plus_frequentee=home_nombre_voyageurs_plus_frequentee,
        home_proprete_gare_plus_frequentee=home_proprete_gare_plus_frequentee,
    )

@app.route('/carte')
def carte():
    return render_template('carte.html')

@app.route('/gare')
def gare():
    return render_template('gare.html')

@app.route('/chiffre')
def chiffre():
    annee = request.args.get("annee", "2024")

    conn = sqlite3.connect('bdd/gares.db')
    c = conn.cursor()

    # liste tous les départements
    c.execute("SELECT DISTINCT SUBSTR(Code_postal, 1, 2) FROM Gare ORDER BY SUBSTR(Code_postal, 1, 2)")
    liste_departements = c.fetchall()

    # Evolution fréquentation (voyageurs)
    c.execute("""
        SELECT 
            SUM(Nb_voyageurs_2022),
            SUM(Nb_voyageurs_2023),
            SUM(Nb_voyageurs_2024)
        FROM Gare
    """)
    total_voy_22, total_voy_23, total_voy_24 = c.fetchone()

    # Evolution propreté (moyenne)
    c.execute("""
        SELECT 
            AVG(100 - Taux_nonconformites_2022),
            AVG(100 - Taux_nonconformites_2023),
            AVG(100 - Taux_nonconformites_2024)
        FROM ControleProprete
    """)
    moy_prop_22, moy_prop_23, moy_prop_24 = c.fetchone()

    # Liste de toutes les gares selon année choisie
    c.execute(f"""
        SELECT 
            g.Nom_gare,
            g.Nb_voyageurs_{annee},
            (100 - cp.Taux_nonconformites_{annee}) AS proprete,
            SUBSTR(g.Code_postal, 1, 2) AS departement
        FROM Gare g
        LEFT JOIN ControleProprete cp ON g.ID_gare = cp.ID_gare
        WHERE g.Nb_voyageurs_{annee} IS NOT NULL
        ORDER BY g.Nb_voyageurs_{annee} DESC
    """)
    gares = c.fetchall()

    conn.close()

    return render_template(
        "chiffre.html",
        annee=annee,
        liste_departements=[row[0] for row in liste_departements],


        total_voy_22=total_voy_22,
        total_voy_23=total_voy_23,
        total_voy_24=total_voy_24,

        moy_prop_22=moy_prop_22,
        moy_prop_23=moy_prop_23,
        moy_prop_24=moy_prop_24,

        gares=gares
    )

@app.route('/api/gares')
def get_gares():
    annee = request.args.get('annee', '2022')  
    conn = sqlite3.connect('bdd/gares.db')
    c = conn.cursor()
    query = f"""
        SELECT g.ID_gare, g.Nom_gare, g.Code_postal,
               g.Nb_voyageurs_{annee},
               cp.Taux_nonconformites_{annee}
        FROM Gare g
        LEFT JOIN ControleProprete cp
        ON g.ID_gare = cp.ID_gare
    """
    c.execute(query)

    rows = c.fetchall()
    conn.close()

    # transformer en dictionnaire
    gares = []
    for row in rows:
        gares.append({
            "id": row[0],
            "nom": row[1],
            "cp": row[2],
            "voyageurs": row[3],
            "nonconformites": row[4]
        })

    return jsonify(gares)

# Exemple de route pour tester la base de données
@app.route('/testbdd')
def test_bdd():
    gares = test_get_gares()
    return render_template('testbdd.html', gares=gares)

def test_get_gares():
    conn = sqlite3.connect('bdd/gares.db')
    c = conn.cursor()
    c.execute("SELECT ID_gare, Nom_gare FROM Gare")
    gares = c.fetchall()
    conn.close()
    return gares

if __name__ == '__main__':
    app.run(debug=True)
