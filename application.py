from operator import or_
from flask import Flask, session, render_template, request, jsonify, flash,redirect, url_for
from flask_login import current_user, login_manager, LoginManager, login_user
from flask_session import Session
from sqlalchemy import or_
from form import *
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "asecretkeythatissupposedtobeasecret"
Session(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_views = '/login'
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return User.query.filter_by(phone=user_id).first()
  except:
    flash(f"Could not load user into session", category="danger")

@app.route("/")
@app.route("/home")
def index():
  return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def registration():
  form = user_registration()
  if form.validate_on_submit():
    user = User(
      username = form.username.data,
      email = form.email_address.data,
      phone = form.phone_number.data,
      passwords = form.password.data
    )
    db.session.add(user)
    db.session.commit()
    flash(f"Registration successfull", category="success")
    return redirect(url_for('login'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")

  return render_template("register.html", form=form)
  
@app.route("/login", methods=["POST", "GET"])
def login():
  form = user_login()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email_address.data).first()
    if user and user.check_password_correction(attempted_password=form.password.data):
      login_user(user, remember=True)
      flash(f"Login successfull", category="success")
      return redirect(url_for('index'))
    if user is None:
      flash(f"No user with that email address", category="danger")
      return redirect(url_for('login'))
    else:
      flash(f"Invalid credentials", category="danger")
      return redirect(url_for('login'))

  return render_template("login.html", form=form)

@app.route("/all-books")
def all_books():
  books = Books.query.limit(100).all()

  return render_template("books.html", books=books)

@app.route("/search-book", methods=["POST", "GET"])
def search():
  search_text = request.form.get("search")
  search = search_text.title()
  books = Books.query.filter(or_(Books.author.like(search), Books.year.like(search), Books.isbn_number.like(search), Books.title.like(search))).all()
  if len(books) == 0 or search == "all":
    flash(f"Search was complete. Found {len(books)} results. Now viewing all books", category="success")
    return redirect(url_for('all_books'))
  if len(books) == 1:
    flash(f"Search was complete. Found {len(books)} result", category="success")
  else:
    flash(f"Search was complete. Found {len(books)} results", category="success")

  return render_template("books.html", books=books)

@app.route("/api/search/<int:book_id>")
def book_api(book_id):
  book = db.session.query(Books).filter(Books.id == book_id).first()
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

if __name__ == '__main__':
    app.run(debug=True, port=5005)
