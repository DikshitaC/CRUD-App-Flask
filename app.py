from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'dikshita'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'bookstore'

mysql = MySQL(app)


def create_books_table():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                   title VARCHAR(255) NOT NULL,
                   author VARCHAR(255) NOT NULL,
                   pages INT)''')
    mysql.connection.commit()
    cur.close()


@app.route('/create_table')
def create_table():
    create_books_table()
    return 'Table created successfully'

@app.route('/')
def index():
    create_books_table()  
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        print(request.form)
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, pages) VALUES (%s, %s, %s)", (title, author, pages))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
        return render_template('add_book.html')


@app.route('/read/<int:id>')
def read(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    
    if book is None:
        return render_template('book_not_found.html')
    
    return render_template('read.html', book=book)


@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
