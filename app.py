import models
import sqlite3

def add_book(cursor, title, author, is_borrowed, **kwargs):
    try:
        if is_borrowed:
            new_book = models.BorrowedBook(
                title, author, True,
                kwargs['library_obj'],
                kwargs['co_date'],
                cursor
            )
        else:
            new_book = models.PersonalBook(title, author, False, cursor)
        
        new_book.save_to_db(cursor)
        print (f"Successfully added: \033[3m{new_book.title}\033[0m (ID: {new_book.book_id})")
        return True
    except Exception as e:
        print(f"Error adding book: {e}")
        return False
    
def add_library(cursor, name, co_period, renewal_period):
    new_library = models.SourceLibrary(name, co_period, renewal_period, cursor)
    new_library.save_to_db(cursor)

def view_all_books(cursor):
    cursor.execute('SELECT books.book_id, title, author, co_date, is_borrowed, status, libraries.name, libraries.co_period, borrowed_info.library_id, due_date FROM books LEFT JOIN borrowed_info ON books.book_id = borrowed_info.book_id LEFT JOIN libraries ON borrowed_info.library_id = libraries.library_id')

    books_list = []

    for row in cursor.fetchall():
        if row[4]:
            temp_library = models.SourceLibrary(row[6], row[7], 0, None)
            temp_library.library_id = row[8]
            next_book = models.BorrowedBook(row[1], row[2], True, temp_library, row[3], None)
            next_book.book_id = row[0]
            next_book.due_date = row[9]
        else:
            next_book = models.PersonalBook(row[1], row[2], False, None)
            next_book.book_id = row[0]
        books_list.append(next_book)
    
    return books_list

def list_libraries(cursor):
    cursor.execute('SELECT library_id, name, co_period, renewal_period FROM libraries')

    libraries_list = []

    for row in cursor.fetchall():
        next_library = models.SourceLibrary(row[1], row[2], row[3], None)
        next_library.library_id = row[0]
        libraries_list.append(next_library)
    
    return libraries_list

def view_borrowed_books(cursor):
    cursor.execute('SELECT books.book_id, title, author, co_date, is_borrowed, status, libraries.name, libraries.co_period, borrowed_info.library_id, due_date FROM books INNER JOIN borrowed_info ON books.book_id = borrowed_info.book_id INNER JOIN libraries ON borrowed_info.library_id = libraries.library_id')

    books_list = []

    for row in cursor.fetchall():
        temp_library = models.SourceLibrary(row[6], row[7], 0, None)            
        temp_library.library_id = row[8]
        next_book = models.BorrowedBook(row[1], row[2], True, temp_library, row[3], None)
        next_book.book_id = row[0]
        next_book.due_date = row[9]
        books_list.append(next_book)
    
    return books_list

def mark_returned(cursor, book_id):
    try:
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        cursor.execute("DELETE FROM borrowed_info WHERE book_id = ?", (book_id,))
        return True
    except Exception as e:
        print(f"Error returning book: {e}")
        return False

def remove_book(cursor, book_id):
    try:
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        cursor.execute("DELETE FROM borrowed_info WHERE book_id = ?", (book_id,))
        return True
    except Exception as e:
        print(f"Error deleting book: {e}")
        return False