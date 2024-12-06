from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Clé secrète pour la session

def est_authentifie():
    return session.get('authentifie')

# Route pour l'accueil
@app.route('/')
def accueil():
    return render_template('hello.html')  # Assure-toi que 'hello.html' existe dans le répertoire templates

# Route pour l'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connexion à la base de données
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()

        # Vérification des identifiants
        cursor.execute("SELECT * FROM utilisateurs WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            session['authentifie'] = True
            return redirect(url_for('accueil'))  # Redirection vers l'accueil
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Route pour l'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connexion à la base de données
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()

        # Vérification si l'utilisateur existe déjà
        cursor.execute("SELECT * FROM utilisateurs WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return "Nom d'utilisateur déjà pris. Essayez un autre.", 400  # Erreur utilisateur existant

        # Inscription de l'utilisateur (mot de passe en clair)
        cursor.execute("INSERT INTO utilisateurs (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('authentification'))  # Rediriger vers la page de connexion après l'inscription

    return render_template('formulaire_inscription.html')

# Route pour enregistrer un livre
@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        categorie = request.form['categorie']
        annee = request.form.get('annee_publication', None)
        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO livres (titre, auteur, categorie, annee_publication) VALUES (?, ?, ?, ?)",
            (titre, auteur, categorie, annee)
        )
        conn.commit()
        conn.close()
        return "Livre enregistré avec succès."
    return render_template('formulaire_livre.html')

if __name__ == "__main__":
    app.run(debug=True)
