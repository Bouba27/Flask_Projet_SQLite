from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Clé secrète pour les sessions

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permet de retourner les lignes sous forme de dictionnaire
    return conn

# Page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Route pour afficher le formulaire d'enregistrement d'un client
@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # Affiche le formulaire d'ajout de client

# Route pour traiter l'enregistrement d'un client
@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    adresse = request.form['adresse']

    # Connexion à la base de données et insertion du client
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, adresse))
    conn.commit()
    conn.close()

    # Redirige vers la page de consultation après l'ajout
    return redirect(url_for('consulter_clients'))

# Route pour consulter tous les clients enregistrés
@app.route('/consultation/')
def consulter_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    conn.close()
    
    return render_template('read_data.html', data=clients)

# Fermer la base de données à la fin de chaque requête
@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)


