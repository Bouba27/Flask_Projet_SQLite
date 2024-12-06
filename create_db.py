import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Création de la table des livres
cursor.execute("""
CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    categorie TEXT,
    annee_publication INTEGER
)
""")

conn.commit()
conn.close()

print("Base de données mise à jour avec succès.")



