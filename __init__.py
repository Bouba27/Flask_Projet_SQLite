from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié (pour l'admin)
def est_authentifie():
    return session.get('authentifie')

# Fonction pour vérifier si l'utilisateur est authentifié pour /fiche_nom/
def est_user_authentifie():
    return session.get('user') == '12345'

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

    # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants administrateurs
        if request.form['username'] == 'admin' and request.form['password'] == 'password':  # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Nouvelle route d'authentification spécifique pour /fiche_nom/
@app.route('/authentification_user', methods=['GET', 'POST'])
def authentification_user():
    if request.method == 'POST':
        # Vérifie les identifiants pour la route protégée /fiche_nom/
        if request.form['username'] == 'user' and request.form['password'] == '12345':
            session['user'] = '12345'  # Stocke l'authentification dans la session
            return redirect(url_for('recherche_par_nom'))
        else:
            # Retourne un message d'erreur si l'authentification échoue
            return render_template('formulaire_authentification_user.html', error=True)

    return render_template('formulaire_authentification_user.html', error=False)

# Route pour afficher la fiche client par ID
@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# Route pour consulter tous les clients
@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# Route pour afficher le formulaire de création d'un client
@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

# Route pour enregistrer un client dans la base de données
@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page de consultation après l'enregistrement

# Nouvelle route pour rechercher un client par nom
@app.route('/fiche_nom/', methods=['GET'])
def recherche_par_nom():
    # Vérification des identifiants pour la route /fiche_nom/
    if not est_user_authentifie():
        return redirect(url_for('authentification_user'))

    nom = request.args.get('nom')  # Récupère le nom depuis les paramètres de l'URL
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    data = cursor.fetchall()
    conn.close()

    if data:
        return render_template('read_data.html', data=data)
    else:
        return jsonify({"message": "Client non trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True)

