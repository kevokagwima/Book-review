import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

if not ('mssql://KEVINKAGWIMA/project1?driver=sql server?trusted_connection=yes'):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine('mssql://KEVINKAGWIMA/project1?driver=sql server?trusted_connection=yes')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registration():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if db.execute("SELECT username, email FROM users WHERE username=:username or email=:email",
        {"username":username, "email":email}).rowcount != 0:
        return render_template("error.html", message="A user already exists with those credentials. Try again.")

    db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
        {"username":username, "email":email, "password":password})

    db.commit()
    return render_template("success.html", message="User registered.")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    username = request.form.get("username")
    password = request.form.get("password")

    if session.get("username") is None:
        session["user_id"] = []

    if db.execute("SELECT username, password FROM users WHERE username=:username and password=:password",
        {"username":username, "password":password}).rowcount == 0:
        return render_template("error.html", message="Invalid login details. try again", text="If not you register first.")

    session["user_id"].append(username)
    return render_template("success1.html", name=username)

@app.route("/active")
def active():
    return render_template("active.html", username=session["user_id"])

@app.route("/search", methods=["POST", "GET"])
def search():
    name = request.form.get("name")

    if db.execute("SELECT * FROM books WHERE (isbn_number = :name) or (publication_year = :name) or (title = :name) or (author = :name)", {"name":name}).rowcount == 0:
        return render_template("search.html", message="No result")

    books = db.execute("SELECT * FROM books WHERE (isbn_number = :name) or (publication_year = :name) or (title = :name) or (author = :name)", {"name":name}).fetchall()

    return render_template("search.html", books=books)

@app.route("/search/<int:book_id>", methods=["GET"])
def books(book_id):
    global book
    book = db.execute("SELECT * FROM books WHERE id = :id",{"id":book_id}).fetchone()
    
    rating = db.execute("SELECT rating FROM reviews WHERE book_number = :id", {"id":book_id}).fetchone()

    if book is None:
        return render_template("book_detail.html", book=book, rating=rating, message="No such book")

    if rating is None:
        return render_template("book_detail.html", book=book, rating=rating, error="No rating")

    return render_template("book_detail.html", book=book, rating=rating)

@app.route("/review/search/<int:book_id>", methods=["POST"])
def review(book_id):
    name = request.form.get("name")
    review = request.form.get("review")
    rating = request.form.get("rating")

    if db.execute("SELECT name FROM reviews WHERE name = :name", {"name":name}).rowcount != 0:
        return render_template("book_detail.html", book=book, rating=rating, text="Cannot write more than one review")

    db.execute("INSERT INTO reviews (name, review, rating, book_number) VALUES (:name, :review, :rating, :book_number)",{"name":name, "review":review, "rating":rating, "book_number":book_id})

    db.commit()
    return render_template("book_detail.html", book=book, rating=rating, texts="Review saved.")

@app.route("/api/search/<int:book_id>")
def book_api(book_id):
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id":book_id}).fetchone()

    rating = db.execute("SELECT rating FROM reviews WHERE book_number = :id", {"id":book_id}).fetchone()

    if book is None:
        return jsonify({"error": "Invalid book"})

    return jsonify({
        "ISBN NUMBER": book.isbn_number,
        "Title": book.title,
        "Author": book.author,
        "Publication Year": book.publication_year,
        "Rating": rating
    })
