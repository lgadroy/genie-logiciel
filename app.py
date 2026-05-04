from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/carte')
def carte():
    return render_template('carte.html')

@app.route('/gare')
def gare():
    return render_template('gare.html')

@app.route('/chiffre')
def chiffre():
    return render_template('chiffre.html')

@app.route('/api/gares')
def get_gares():
    conn = sqlite3.connect('bdd/gares.db')
    c = conn.cursor()

    c.execute("""
        SELECT g.ID_gare, g.Nom_gare, g.Code_postal,
               g.Nb_voyageurs_2023,
               cp.Taux_nonconformites_2023
        FROM Gare g
        LEFT JOIN ControleProprete cp
        ON g.ID_gare = cp.ID_gare
    """)

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
