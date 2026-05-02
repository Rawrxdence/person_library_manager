import sqlite3

def initialize_db(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            is_borrowed BOOLEAN,
            status TEXT
        )
''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libraries (
            library_id INTEGER PRIMARY KEY,
            name TEXT,
            co_period INTEGER,
            renewal_period INTEGER    
        )
''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_info (
            book_id INTEGER,
            library_id INTEGER,
            co_date TEXT,
            due_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (book_id),
            FOREIGN KEY (library_id) REFERENCES libraries (library_id)
        )
''')
