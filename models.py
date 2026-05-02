import random
from datetime import datetime, timedelta
import sqlite3

class Book:
    def __init__(self, title, author, is_borrowed, cursor):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        if cursor is not None:
            self.book_id = self.generate_id(cursor)

    def __str__(self):
        return f"\033[3m{self.title}\033[0m by {self.author}"
    
    @staticmethod
    def generate_id(cursor):
        is_valid = False

        while not is_valid:
            new_id = random.randint(10000, 99999)

            cursor.execute("SELECT book_id FROM books WHERE book_id = ?", (new_id,))

            result = cursor.fetchone()

            if result is None:
                is_valid = True
        return new_id
    
    def update_status(self, new_status):
        self.status = new_status

    def save_to_db(self, cursor):
        query = "INSERT INTO books (book_id, title, author, is_borrowed) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.book_id, self.title, self.author, self.is_borrowed))
    
class SourceLibrary():

    def __init__(self, name, co_period, renewal_period, cursor):
        self.name = name
        self.co_period = co_period
        self.renewal_period = renewal_period
        if cursor is not None:
            self.library_id = self.generate_id()
    
    @staticmethod
    def generate_id(self, cursor):
        is_valid = False

        while not is_valid:
            new_id = random.randint(100,999)
            cursor.execute("SELECT library_id FROM libraries WHERE library_id = ?", (new_id,))

            result = cursor.fetchone()
            if result is None:
                is_valid = True
        return new_id
    
    def save_to_db(self, cursor):
        query = "INSERT INTO libraries (library_id, name, co_period, renewal_period) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.library_id, self.name, self.co_period, self.renewal_period))

class PersonalBook(Book):

    def __init__(self, title, author, is_borrowed, cursor):
        super().__init__(title, author, is_borrowed, cursor)


class BorrowedBook(Book):

    def __init__(self, title, author, is_borrowed, source_library, co_date, cursor):
        try:
            datetime.strptime(co_date, "%m/%d/%y")
        except ValueError:
            raise ValueError(f"Invalid date formate for \033[3m{title}\033[0m, Expected MM/DD/YY")
        
        super().__init__(title, author, is_borrowed, cursor)
        self.source_library = source_library
        self.co_date = co_date
        self.due_date = self.get_due_date()

    def get_due_date(self):
        co_date_obj = datetime.strptime(self.co_date, "%m/%d/%y")
        due_date = co_date_obj + timedelta(days = self.source_library.co_period)
        return due_date.strftime('%m/%d/%y')

    def calculate_days_left(self):
        due_date_obj = datetime.strptime(self.due_date, '%m/%d/%y').date()
        today = datetime.now.date()
        days_left = due_date_obj - today
        return days_left

    def record_renewal(self):
        today = datetime.now()
        self.due_date = today + timedelta(days = self.source_library.renewal_period)
        self.due_date = self.due_date.strftime('%m/%d/%y')
    
    def __str__(self):
        return f"\033[3m{self.title}\033[0m by {self.author}| (DUE: {self.due_date})"
    
    def save_to_db(self, cursor):
        super().save_to_db(cursor)

        query = "INSERT INTO borrowed_info (book_id, library_id, co_date, due_date) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.book_id, self.source_library.library_id, self.co_date, self.due_date))
