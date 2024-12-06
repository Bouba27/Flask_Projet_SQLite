
-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'  -- 'admin' or 'user'
);

-- Table des livres
CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    categorie TEXT,
    annee_publication INTEGER,
    quantite INTEGER DEFAULT 1
);

-- Table des prêts
CREATE TABLE IF NOT EXISTS prets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_pret DATE DEFAULT (DATE('now')),
    date_retour DATE,
    statut TEXT DEFAULT 'en cours',  -- 'en cours' or 'retourne'
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(livre_id) REFERENCES livres(id)
);
