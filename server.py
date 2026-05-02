from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import app
import models

server = Flask(__name__)

def get_db():
    conn = sqlite3.connect('data/library.db')
    return conn, conn.cursor()

@server.route('/')
def home():
    conn, cursor = get_db()
    all_books = app.view_all_books(cursor)
    all_libraries = app.list_libraries(cursor)
    conn.close()

    return render_template('index.html', books=all_books, libraries=all_libraries)

@server.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn, cursor = get_db()
    app.remove_book(cursor, book_id)
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@server.route('/return/<int:book_id>')
def return_book(book_id):
    conn, cursor = get_db()
    app.mark_returned(cursor, book_id)
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@server.route('/add', methods=['POST'])
def add_book_route():
    title = request.form.get('title')
    author = request.form.get('author')
    is_borrowed = 'is_borrowed' in request.form
    conn, cursor = get_db()
    if is_borrowed:
        lib_id = request.form.get('library_id')
        co_date = request.form.get('co_date')
        cursor.execute('SELECT name, co_period, renewal_period FROM libraries WHERE library_id = ?', (lib_id,))
        res = cursor.fetchone()
        if res:
            selected_lib = models.SourceLibrary(res[0], res[1], res[2], None)
            selected_lib.library_id = int(lib_id)
            app.add_book(cursor, title, author, True, library_obj=selected_lib, co_date=co_date)
    else:
        app.add_book(cursor, title, author, False)
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ =='__main__':
    server.run(debug=True)