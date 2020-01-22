from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask import Flask, g, render_template, session, url_for,logging, request, redirect,flash,json,jsonify
engine = create_engine('postgresql://postgres:12345@localhost/good')
db = scoped_session(sessionmaker(bind=engine))
from passlib.hash import sha256_crypt
from helpers import login_required
import requests



app= Flask(__name__)

app.secret_key= "1234567oshiosecret"


@app.route("/")
@login_required
def index():
        return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", login)
    return redirect (url_for("login"))

# register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        othernames = request.form.get("othernames")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        passwordkey = sha256_crypt.hash(str(password))



        usernames = db.execute("SELECT * FROM users WHERE username = :username",{"username":username}).fetchone()
        db.commit()
             # check if username exist 
          
        if usernames:
            flash("username already exist", "danger")
            return render_template("register.html")  
    
        if password == confirm:
            db.execute("INSERT INTO users(othernames, username, email, passwordkey) VALUES(:othernames,:username, :email, :passwordkey)",
                                     {"othernames":othernames, "username":username, "email":email,
                                     "passwordkey":passwordkey})
            db.commit()
            flash("your registered and you can login", "success")
            return redirect(url_for('login'))
        else:
            flash("password does not match","danger")
            return render_template("register.html")               

    return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM users WHERE username= :username",{"username":username}).fetchone()
        passworddata = db.execute("SELECT passwordkey FROM users WHERE username= :username",{"username":username}).fetchone()
        userid = db.execute("SELECT id FROM users WHERE username= :username",{"username":username}).fetchone()
        if usernamedata is None:
            flash("username does not exist","danger")
            return render_template("login.html")
        else:
            for password_data in passworddata:
                if sha256_crypt.verify(password,password_data):
                    flash("you are now login", "success")
                    session['username'] = username
                    session['logged_in'] = True
                    return redirect(url_for('index'))

                else: 
                    flash("incorrect password","danger")  
                    return render_template("login.html")
                
           

    return render_template("login.html")

@app.route("/search", methods=["GET","POST"]) 
@login_required
def search():
    # take input and add wildcard
        book = "%" + request.form.get("book") + "%"
        book = book.title()
        results = db.execute("SELECT  *FROM books WHERE title LIKE :book OR isbn LIKE :book OR author LIKE :book ",{"book":book}).fetchall() 
        if not results:
            return render_template("error.html", message="no book") 
        return render_template("result.html", search=True, results=results)

 
@app.route("/result")
@login_required
def result():
    return render_template("result.html")

@app.route("/book/<isbn>", methods=["POST", "GET"])
@login_required
def book(isbn):
    data = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
    db.commit()

    # goodreads API
    key = "otvHOafjr0TlNmNHjHekA"
    
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key , "isbns": isbn }).json()


    isbn = res['books'][0]['isbn']
    work_ratings_count = res['books'][0]['work_ratings_count']

    avg_rate = res['books'][0]['average_rating']

    

   
        # review and comment section

    data2 = db.execute("SELECT * FROM reviews JOIN  users ON users.id= user_id JOIN books ON books.id= book_id WHERE books.isbn= :isbn ", {"isbn":isbn}).fetchall()
    
    
    
    
    if request.method == "POST":
        currentUser = session["username"]
        userid = db.execute("SELECT id FROM users WHERE username =:username ", {"username":currentUser}).fetchone()[0]
        bookid = db.execute("SELECT id FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()[0]

        rating = request.form.get("rating")
        comment = request.form.get("comment")



        row = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",{"user_id":userid, "book_id":bookid}).fetchall()
        if row:
            flash("you have already made a comment","danger")
        else:
            review = db.execute("INSERT INTO reviews (user_id, book_id, rating, comment) VALUES (:user_id, :book_id, :rating, :comment)",{"user_id":userid, "book_id":bookid, "rating":rating, "comment":comment })
            db.commit()
            flash("your comment has been added", "success")
            return redirect("/book/" +isbn)
        
   
    return render_template("book.html", search=True, avg_rate=avg_rate, isbn=isbn, work_ratings_count=work_ratings_count, data=data, data2=data2,  )  
@app.route("/api/<isbn>", methods=["GET"])
@login_required
def api(isbn):
    row = db.execute("SELECT title, author, pubyear, isbn, \
                    COUNT(reviews.id) as review_count, \
                    AVG(reviews.rating) as average_score \
                    FROM books \
                    INNER JOIN reviews \
                    ON books.id = reviews.book_id \
                    WHERE isbn = :isbn \
                    GROUP BY title, author, pubyear, isbn",
                    {"isbn": isbn})
    if row.rowcount != 1:
        return jsonify({"Error": "Invalid book ISBN"}), 404

     # Fetch result from RowProxy    
    tmp = row.fetchone()

    # Convert to dict
    result = dict(tmp.items())

    # Round Avg Score to 2 decimal. This returns a string which does not meet the requirement.
    # https://floating-point-gui.de/languages/python/
    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)
               
    
if __name__ == "__main__":
    app.run(debug=True)   