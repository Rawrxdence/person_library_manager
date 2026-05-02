import sqlite3
import database
import app
import models
from datetime import datetime, timedelta

def seed_data():
    # 1. Initialize and connect
    database.initialize_db()
    conn = sqlite3.connect('data/library.db')
    cursor = conn.cursor()

    # 2. Create a Library (if it doesn't exist)
    wake = models.SourceLibrary('Wake County Public Library', 21, 14, cursor)
    cursor.execute("INSERT OR IGNORE INTO libraries VALUES (?, ?, ?, ?)", 
                   (wake.library_id, wake.name, wake.co_period, wake.renewal_period))

    # 3. List of Books to add
    # Format: (Title, Author, is_borrowed)
    books_to_add = [
        ("The Hobbit", "J.R.R. Tolkien", False),
        ("1984", "George Orwell", False),
        ("The Great Gatsby", "F. Scott Fitzgerald", True),
        ("Dune", "Frank Herbert", False),
        ("The Catcher in the Rye", "J.D. Salinger", True),
        ("To Kill a Mockingbird", "Harper Lee", False),
        ("Brave New World", "Aldous Huxley", True),
        ("Foundation", "Isaac Asimov", False),
        ("Neuromancer", "William Gibson", True),
        ("Pride and Prejudice", "Jane Austen", False),
        ("The Shining", "Stephen King", True),
        ("Project Hail Mary", "Andy Weir", False),
        ("Circe", "Madeline Miller", True),
        ("Slaughterhouse-Five", "Kurt Vonnegut", False),
        ("The Left Hand of Darkness", "Ursula K. Le Guin", True),
        ("Hyperion", "Dan Simmons", False),
        ("Snow Crash", "Neal Stephenson", True),
        ("Good Omens", "Neil Gaiman & Terry Pratchett", False),
        ("The Martian", "Andy Weir", True),
        ("American Gods", "Neil Gaiman", False),
        ("Beloved", "Toni Morrison", True),
        ("The Night Circus", "Erin Morgenstern", False),
        ("The Road", "Cormac McCarthy", True),
        ("The Picture of Dorian Gray", "Oscar Wilde", False),
        ("Frankenstein", "Mary Shelley", True)
    ]

    # 4. Loop and add via your app logic
    today = datetime.now().strftime("%m/%d/%y")
    
    print("Starting the seeding process...")
    for title, author, borrowed in books_to_add:
        if borrowed:
            # Add with checkout date of today
            app.add_book(cursor, title, author, True, library_obj=wake, co_date=today)
        else:
            app.add_book(cursor, title, author, False)

    conn.commit()
    conn.close()
    print("\n--- Seeding Complete: 25 books added to library.db ---")

if __name__ == "__main__":
    seed_data()