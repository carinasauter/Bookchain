drop table if exists users;
CREATE TABLE users (
    user_id integer PRIMARY KEY,
    username text not null,
    email text not null,
    password_hash text not null
);

drop table if exists books;
CREATE TABLE books (
    book_id integer PRIMARY KEY,
    title text not null,
    author text not null,
    year_published integer,
    ISBN integer,
    ISBN_10 integer,
    thumbnail text,
    short_description text,
    current_location text not null,
    uploader text not null,
    current_reader text not null,
    status text not null
);

drop table if exists books_users;
CREATE TABLE users (
    user_book_id integer PRIMARY KEY,
    user_id integer not null, 
    book_id integer not null, 
    relationship text not null
    FOREIGN KEY(book_id) REFERENCES books (book_id) ON DELETE CASCADE
    FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);