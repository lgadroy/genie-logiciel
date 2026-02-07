from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True)
