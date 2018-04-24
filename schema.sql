drop table if exists users;


CREATE TABLE users (
    user_id integer PRIMARY KEY,
    username text not null,
    email text not null,
    password_hash text not null,
    full_name text not null,
    street text not null,
    city text not null,
    state text not null,
    country text not null,
    zipcode integer not null
);

drop table if exists books;
CREATE TABLE books (
    book_id integer PRIMARY KEY,
    title text not null,
    author text not null,
    thumbnail text,
    short_description text,
    isbn integer,
    uploader text not null,
    holder text not null,
    status text not null
);

drop table if exists comments;
CREATE TABLE comments (
    comment_id integer PRIMARY KEY,
    book_id integer not null, 
    user_id integer not null, 
    comment text not null,
    FOREIGN KEY(book_id) REFERENCES books (book_id) ON DELETE CASCADE
    FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

drop table if exists books_users;
CREATE TABLE books_users (
    user_book_id integer PRIMARY KEY,
    user_id integer not null, 
    book_id integer not null, 
    relationship text not null,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP not null,
    FOREIGN KEY(book_id) REFERENCES books (book_id) ON DELETE CASCADE
    FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

drop table if exists ratings;
CREATE TABLE ratings (
    rating_id integer PRIMARY KEY,
    book_id integer not null, 
    user_id integer not null, 
    rating integer not null,
    FOREIGN KEY(book_id) REFERENCES books (book_id) ON DELETE CASCADE
    FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

drop table if exists history;
CREATE TABLE history (
    history_id integer PRIMARY KEY,
    book_id integer not null, 
    user_id integer not null, 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP not null,
    FOREIGN KEY(book_id) REFERENCES books (book_id) ON DELETE CASCADE
    FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);