# Route pour consulter un client par nom
@app.route('/fiche_nom/<string:nom>')
def NomFiche(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
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

# Route pour consulter tous les livres
@app.route('/consultation_livre/')
def consultation_livre():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data_livre.html', data=data)

# Route pour afficher le formulaire d'enregistrement de client
@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire de client

# Route pour enregistrer un client
@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect(url_for('ReadBDD'))

# Route pour afficher le formulaire d'enregistrement de livre
@app.route('/enregistrer_livre', methods=['GET'])
def formulaire_livre():
    return render_template('formulaire_livre.html')  # afficher le formulaire de livre

# Route pour enregistrer un livre
@app.route('/enregistrer_livre', methods=['POST'])
def enregistrer_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livres (titre, auteur) VALUES (?, ?)', (titre, auteur))
    conn.commit()
    conn.close()
    return redirect(url_for('consultation_livre'))

# Route pour supprimer un livre
@app.route('/supprimer_livre', methods=['GET', 'POST'])
def supprimer_livre():
    message = ""

    if request.method == 'POST':
        livre_id = request.form['id']
        
        # Connexion à la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Vérifier si le livre existe
        cursor.execute('SELECT * FROM livres WHERE id = ?', (livre_id,))
        livre = cursor.fetchone()
        
        if livre:
            # Supprimer le livre
            cursor.execute('DELETE FROM livres WHERE id = ?', (livre_id,))
            conn.commit()
            message = f"Le livre avec l'ID {livre_id} a été supprimé."
        else:
            message = f"Aucun livre trouvé avec l'ID {livre_id}."

        conn.close()

    return render_template('supprimer_livre.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)






