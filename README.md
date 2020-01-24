# Clinton's CS50W Project 1

## Web Programming with Python and JavaScript
### https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/

## Use the app on Heroku



Persistent information is stored in an internal Postgres DB with three tables:
- Users
- Books
- Review


The tables have been created as follows:
    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR  NOT NULL,
    othernames VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    passwordkey VARCHAR NOT NULL
);
    CREATE TABLE books (
    id SERIAL PRIMARY KEY,
   isbn VARCHAR NOT NULL,
   title VARCHAR NOT NULL,
   author VARCHAR NOT NULL,
   pubyear INTEGER  NOT NULL
   );

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    rating SMALLINT NOT NULL CONSTRAINT Invalid_Rating CHECK (rating <=5 AND rating>=1),
    comment VARCHAR
);

The website provides the following functions:
- Register username and password (username must be unique, enforced in the DB)
- Login and Logout
- When logged in ability to use a Search function (/search), which provides a combination of results (/results)
- Leave a review
- An API function (/api<isbn>)