import csv
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost/good')
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")

reader = csv.reader(file)

for isbn, title, author, pubyear in reader:

    db.execute("INSERT INTO books (isbn, title, author, pubyear) VALUES (:isbn, :title, :author, :pubyear)", 
        {"isbn": isbn,
         "title":title,
         "author":author,
         "pubyear":pubyear})
    
    #print(f"added book {title} to db")
    db.commit()





# def main():
#     f = open("books.csv")
#     reader = csv.reader(f)
#     for isbn, title, author, pubyear in reader:
#         db.execute("INSERT INTO books (isbn, title, author, pubyear) VALUES(:isbn, :title, :author, :pubyear)",
#                     {"isbn":isbn, "title":title, "author":author,"pubyear":pubyear})
#         db.commit()
# if __name__ == "__main__":
#     main()
