-- Insert code to create Database Schema
-- This will create your .db database file for use
-- drop table if exists trips;
-- CREATE TABLE trips (
--     trip_id integer PRIMARY KEY,
--     tripname text not null,
--     destination text not null
-- );
drop table if exists users;
CREATE TABLE users (
    user_id integer PRIMARY KEY,
    username text not null,
    email text not null,
    password_hash text not null
);

-- drop table if exists users_on_trips;
-- CREATE TABLE users_on_trips (
-- 	user_trip_id integer PRIMARY KEY,
-- 	user_id integer NOT NULL, 
--     trip_id integer NOT NULL,
--     -- the on delete cascade does not seem to work or do anything...
-- 	FOREIGN KEY(trip_id) REFERENCES trips (trip_id) ON DELETE CASCADE
-- );
