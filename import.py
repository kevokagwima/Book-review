import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mssql://KEVINKAGWIMA/project1?driver=sql server?trusted_connection=yes')
db = scoped_session(sessionmaker(bind=engine))

def main():
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn_number, title, author, publication_year in reader:
    db.execute("INSERT INTO books (isbn_number, title, author, publication_year) VALUES (:isbn_number, :title, :author, :publication_year)", 
      {"isbn_number":isbn_number, "title":title, "author":author, "publication_year":publication_year})
    print(f"Added book {isbn_number} by {author} titled {title} published in {publication_year}")

  db.commit()

if __name__ == "__main__":
  main()
