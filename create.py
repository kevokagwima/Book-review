from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)

def main():
  db.create_all()

if __name__ == '__main__':
  with app.app_context():
    main()
