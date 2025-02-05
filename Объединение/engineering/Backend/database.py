import sqlite3

def init_db():
    conn = sqlite3.connect('sport.db')
    c = conn.cursor()
    
    # Таблица инвентаря
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT NOT NULL,
                  quantity INTEGER,
                  condition TEXT,
                  price REAL)''')
    
    # Тестовые данные
    if c.execute("SELECT COUNT(*) FROM inventory").fetchone()[0] == 0:
        test_data = [
            ('Футбольный мяч', 'Мячи', 15, 'Отличное', 2500),
            ('Баскетбольный мяч', 'Мячи', 10, 'Хорошее', 3000)
        ]
        c.executemany('INSERT INTO inventory VALUES (NULL,?,?,?,?,?)', test_data)
    
    conn.commit()
    conn.close()

def get_inventory():
    conn = sqlite3.connect('sport.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    return [dict(item) for item in items]