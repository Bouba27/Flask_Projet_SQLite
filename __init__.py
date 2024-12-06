from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

# Route pour l'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # Code de l'inscription


# Route pour l'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password':  
            session['authentifie'] = True
            return redirect(url_for('hello_world'))
        else:
            return "Échec de l'authentification, veuillez réessayer."
    return render_template('formulaire_authentification.html')

# Route pour enregistrer un nouveau livre
@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.form['titre']
        auteur = request.form['auteur']
        categorie = request.form['categorie']
        annee = request.form['annee']

        # Ajouter le livre à la base de données (exemple SQLite)
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO livres (titre, auteur, categorie, annee) VALUES (?, ?, ?, ?)", 
            (titre, auteur, categorie, annee)
        )
        conn.commit()
        conn.close()
        return "Livre enregistré avec succès."
    
    return render_template('formulaire_livre.html')

if __name__ == "__main__":
    app.run(debug=True)



