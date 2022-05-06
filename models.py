from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
  __tablename__ = "Users"
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(length=50), nullable=False, unique=True)
  email = db.Column(db.String(length=100), nullable=False, unique=True)
  phone = db.Column(db.String(length=10), nullable=False, unique=True)
  password = db.Column(db.String(length=50), nullable=False, unique=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class Books(db.Model):
  __tablename__ = "books"
  id = db.Column(db.Integer(), primary_key=True)
  isbn_number = db.Column(db.Integer(), nullable=False, unique=True)
  title = db.Column(db.String(length=100), nullable=False)
  author = db.Column(db.String(length=50), nullable=False)
  year = db.Column(db.Integer(), nullable=False)
