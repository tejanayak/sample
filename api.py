from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error



app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'database': 'bookstore',
    'user': 'root',
    'password': '*Number1'
}

# Initialize database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create books table if it doesn't exist
def init_db():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publication_year INT
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    publication_year = data.get('publication_year')
    
    if not title or not author:
        return jsonify({'error': 'Title and author are required'}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, publication_year))
        connection.commit()
        return jsonify({'message': 'Book created', 'id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return jsonify(books), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Get a single book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()
        if book:
            return jsonify(book), 200
        return jsonify({'error': 'Book not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    publication_year = data.get('publication_year')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE books SET title = %s, author = %s, publication_year = %s WHERE id = %s"
        cursor.execute(query, (title, author, publication_year, id))
        connection.commit()
        if cursor.rowcount:
            return jsonify({'message': 'Book updated'}), 200
        return jsonify({'error': 'Book not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount:
            return jsonify({'message': 'Book deleted'}), 200
        return jsonify({'error': 'Book not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)