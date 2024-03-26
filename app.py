from flask import Flask, jsonify, request

app = Flask(__name__)

class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

class BookService:
    def __init__(self):
        self.books = []

    def create_book(self, id, title, author):
        book = Book(id,title, author)
        self.books.append(book)
        return book

    def get_book(self, id):
        for book in self.books:
            if id != None and book.id == id:
                return book
        return None

    def update_book(self, id=None, new_title=None, new_author=None):
        book = self.get_book(id)
        if book:
            if new_title:
                book.title = new_title
            if new_author:
                book.author = new_author
            return True
        return False

    def delete_book(self, id):
        book = self.get_book(id=id)
        if book:
            self.books.remove(book)
            return True
        return False

book_service = BookService()
book_service.create_book("1","Book 1","Author 1")

# Routes for CRUD operations

@app.route('/books', methods=['GET'])
def get_books():
    books = [{'title': book.title, 'author': book.author, 'id': book.id} for book in book_service.books]
    return jsonify({'books': books})

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = book_service.get_book(id=id)
    if book:
        return jsonify({'title': book.title, 'author': book.author, 'id': book.id})
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    id = data.get('id')
    title = data.get('title')
    author = data.get('author')
    if title and author and id:
        book = book_service.create_book(id ,title, author)
        return jsonify({'message': 'Book created successfully', 'title': book.title}), 201
    else:
        return jsonify({'error': 'Incomplete data provided'}), 400

@app.route('/books/<title>', methods=['PUT'])
def update_book(title):
    data = request.json
    new_id = data.get('id')
    new_title = data.get('title')
    new_author = data.get('author')
    if book_service.update_book(title, new_id, new_title, new_author):
        return jsonify({'message': 'Book updated successfully', 'title': new_title}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<title>', methods=['DELETE'])
def delete_book(title):
    if book_service.delete_book(title):
        return jsonify({'message': 'Book deleted successfully', 'title': title}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
