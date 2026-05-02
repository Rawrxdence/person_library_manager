import unittest
import sqlite3
import app
import models

class TestLibraryLogic(unittest.TestCase):
    def setUp(self):
        """Set up a temporary in-memory database for every test."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        # Initialize your tables here (mirroring your database.py logic)
        self.cursor.execute('CREATE TABLE books (book_id INTEGER PRIMARY KEY, title TEXT, author TEXT, is_borrowed BOOLEAN)')

    def test_add_personal_book(self):
        """Verify that a personal book is correctly saved to the DB."""
        result = app.add_book(self.cursor, "The Hobbit", "J.R.R. Tolkien", False)
        
        self.assertTrue(result) # Check if function returned True
        self.cursor.execute("SELECT title FROM books WHERE title='The Hobbit'")
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        self.assertEqual(book[0], "The Hobbit")

    def tearDown(self):
        """Close the connection after each test."""
        self.conn.close()

if __name__ == '__main__':
    unittest.main()