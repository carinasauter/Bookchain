drop table if exists users;
CREATE TABLE users (
    user_id integer PRIMARY KEY,
    username text not null,
    email text not null,
    password_hash text not null
);