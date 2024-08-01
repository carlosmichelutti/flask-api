from flask import Flask, jsonify, make_response, request
from sqlalchemy import select, func, delete, update
from resources.database import DB_CONNECTION
from resources.models import Books
import pandas as pd

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", methods=["GET"])
def index():
    return "Hello, World! This is my first api."

@app.route(r'/add_books/', methods=['POST'])
def add_books():

    try:
        books = request.json
        books_list = []
        for book in books:
            books_list.append(
                Books(
                    category=book['category'],
                    title=book['title'],
                    price=book['price']
                )
            )

        with DB_CONNECTION.session as session:
            session.add_all(books_list)
            session.commit()
        
    except Exception as e:
        return make_response('Unable to add books. Please review the parameters and send a valid json in this format: {"category": "category", "title": "title", "price": "price"}.', 400)
    else:
        return make_response(f"Books added: {request.json}", 201)

@app.route(r'/books/<string:category>/', methods=['GET'])
@app.route(r'/books/', methods=['GET']) 
def get_books(category: str = 'all'):

    categorys = select(
        Books.category
    ).distinct()

    categorias = [category.lower() for category in pd.read_sql(categorys, DB_CONNECTION.engine)['category'].to_list()]
    
    if category.lower() in categorias or category == 'all':
        if category == 'all':

            books = select(
                Books
            )

            dataframe = pd.read_sql(books, DB_CONNECTION.engine)

        else:
            books = select(
                Books
            ).where(
                func.lower(Books.category) == category.lower()
            )

            dataframe = pd.read_sql(books, DB_CONNECTION.engine)
        
        return dataframe.to_json(orient='records', force_ascii=False)
    else:
        return make_response('Category not found', 404)

@app.route(r'/book/<int:book_id>/', methods=['GET'])
def get_book(book_id: int):

    try:
        book = select(
            Books
        ).where(
            Books.id == book_id
        )

        dataframe = pd.read_sql(book, DB_CONNECTION.engine)

        return make_response(dataframe.iloc[0, :].to_json(force_ascii=False))

    except Exception as e:
        return make_response('Book not found', 404)

@app.route(r'/categorys/', methods=['GET'])
def get_categorys():

    query = select(
        Books.category
    ).distinct()

    dataframe = pd.read_sql(query, DB_CONNECTION.engine)
    
    return {'categorys': dataframe['category'].to_list()}

@app.route(r'/delete_books/', methods=['DELETE'])
def delete_books():

    books = request.json
    books_list = []
    for book in books:
        books_list.append(book['id'])
    
    result = (
        delete(Books)
        .where(Books.id.in_(books_list))
    )

    with DB_CONNECTION.session as session:
        session.execute(result)
        session.commit()

    return make_response(f"Livros deletados {request.json}")

app.run(port=5000, host='localhost', debug=True)