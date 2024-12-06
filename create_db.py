
import sqlite3

def init_db():
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    
    # Create tables from schema.sql
    with open('schema_updated.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de données initialisée avec succès.")
