import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create cables table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            connection TEXT NOT NULL,
            length INTEGER,
            material TEXT
        )
    ''')

    # Create connections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            direction TEXT CHECK(direction IN ('AtoB', 'BtoA', 'both')) NOT NULL,
            connectiontype TEXT
        )
    ''')

    # Create parts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cable_id INTEGER,
            FOREIGN KEY (cable_id) REFERENCES cables (id)
        )
    ''')

    # Insert sample data into cables table
    cursor.executemany('''
        INSERT INTO cables (name, connection, length, material)
        VALUES (?, ?, ?, ?)
    ''', [
        ('Cable1', 'Connection1', 100, 'Copper'),
        ('Cable2', 'Connection2', 200, 'Fiber'),
        ('Cable3', 'Connection3', 150, 'Aluminum')
    ])

    # Insert sample data into connections table
    cursor.executemany('''
        INSERT INTO connections (name, direction, connectiontype)
        VALUES (?, ?, ?)
    ''', [
        ('Connection1', 'AtoB', 'Type1'),
        ('Connection2', 'BtoA', 'Type2'),
        ('Connection3', 'both', 'Type3')
    ])

    # Insert sample data into parts table
    cursor.executemany('''
        INSERT INTO parts (name, cable_id)
        VALUES (?, ?)
    ''', [
        ('PartA', 1),
        ('PartB', 1),
        ('PartC', 2),
        ('PartD', 2),
        ('PartE', 3),
        ('PartF', 3)
    ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()