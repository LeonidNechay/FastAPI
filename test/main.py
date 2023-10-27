import pymysql
import sqlalchemy.sql.expression
from fastapi import FastAPI, Depends, status
import re

import models
from models import Book
from models import Author, AuthorList

from session import get_session

app = FastAPI()

connection = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='',
    database='pythondb',
)

@app.post("/create_table_books")
def  create_table_books():
    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            CREATE TABLE IF NOT EXISTS books
            (
            id INT,
            name VARCHAR(255)
            )
            """
            cursor.execute(sql)
        connection.commit()


@app.get("/")
def read_root():
    return {"Hello World"}


@app.get("/home/{text}")
def home(text: str):
    count = 0
    numbers = []

    numbers = re.findall(r'\+38(?: |)0(?: |)(?:95|66|99|50)(?: |)\d{3}(?: |-|)\d{2}(?: |-|)\d{2}', text)

    count = len(numbers)

    return {
        "numbers": numbers,
        "count": count
    }

@app.get("/books")
def get_books(db=Depends(get_session)):
    return db.query(Book).all()

@app.post("/insert_to_book")
def insert_to_books(item: Book):
        with connection.cursor() as cursor:
            sql = f"""
                INSERT INTO `books` (`id`, `name`, `author_id`) VALUES (NULL, %s, %s);
            """
            cursor.execute(sql, (item.name, item.author_id))
            connection.commit()

@app.post("/insert_to_book_orm")
def insert_to_books_orm(item: Book, db=Depends(get_session)):
    if not db.query(models.Authors).filter(models.Authors.name == item.author_name):
        db_author = models.Authors(name = item.author_name)
        db.add(db_author)
        db.commit()
    author = db.query(models.Authors).filter(models.Authors.name == item.author_name)
    db_book = models.Books(name = item.name, author_id = author.id)
    db.add(db_book)
    db.commit()
    return db_book

@app.post("/insert_to_author")
def insert_to_authors(item: Author):
    with connection.cursor() as cursor:
        sql = f"""
            INSERT INTO `authors` (`id`, `name`) VALUES (NULL, %s);
        """
        cursor.execute(sql, item.name)
        connection.commit()
    return item


@app.post("/insert_to_author_list")
def insert_to_authors_list(item: AuthorList):
    sql = "INSERT INTO `authors` (`id`, `name`) VALUES "
    for el in item.data:
        sql += f"(NULL, '{el.name}'),"

    sql = sql[slice(-1)]
    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()

    return item.data

@app.put("/update_book/{id}")
def insert_to_book(id, item: Book):
    with connection.cursor() as cursor:
        sql = f"""
            UPDATE `books` SET name = %s, author_id = %s WHERE id = %s;
        """
        cursor.execute(sql, (item.name, item.author_id, id))
        connection.commit()
    return item

@app.put("/update_book_orm/{id}")
def update_books_orm(id, item: Book, db=Depends(get_session)):
    db_book = db.query(models.Books).filter(id = id)
    db_book.name = item.name
    db_book.author_id = item.author_id
    db.commit()
    return db_book

@app.delete("/delete_book/{id}")
def delete_book(id):
    with connection.cursor() as cursor:
        sql = f"""
            DELETE FROM `books` WHERE id = %s;
        """
        cursor.execute(sql, id)
        connection.commit()

@app.delete("/delete_book_orm/{id}")
def delete_book_orm(id, db=Depends(get_session)):
    db.query(models.Books).filter(id = id).delete()


@app.get("/array")
def array():
    array = []
    for i in range(100):
        array.append(i)
    t = tuple(array)

    t_1 = (t[:2], 8, t[2:])
    return t_1