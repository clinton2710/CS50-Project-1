import csv
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgres://okthlidymcbtex:86e67aceca357d377393360818029ac090e8ee9926f7bd419f26e1cdcdb43fa8@ec2-54-247-188-107.eu-west-1.compute.amazonaws.com:5432/d1ioo81nm7hp7f')
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
