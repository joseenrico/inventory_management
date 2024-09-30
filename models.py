import sqlite3

def connect_db():
    return sqlite3.connect('inventory.db')

# setup database
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()

    # tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    ''')

    # tabel Item relasi ke Category
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES Category (id)
        );
    ''')

    # index untuk optimasi pencarian
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_item_name ON Item (name);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_item_category_id ON Item (category_id);')

    conn.commit()
    conn.close()
