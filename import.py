import csv
from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)

def main():
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn_number, title, author, publication_year in reader:
    new_book = Books(
      isbn_number = isbn_number,
      title = title,
      author=author,
      year = publication_year
    )
    db.session.add(new_book)
    db.session.commit()

if __name__ == '__main__':
  with app.app_context():
    main()
