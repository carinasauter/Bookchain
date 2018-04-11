import sqlite3 as sql
from app import login_manager, db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import requests
import json

class User(UserMixin):

	def __init__(self, id_number, username, email, password_hash):
		self.id = id_number;
		self.username = username
		self.email = email
		self.password_hash = password_hash


""" Takes a username as parameter and checks in the database. If the user exists, 
returns user object. If not, returns None.
"""
def getUserByUsername(query):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (query,))
		result = cursor.fetchall()
		if len(result) == 0:
			return None
		else:
			row = result[0]
			user = User(row[0], query, row[2], row[3])
			return user


""" Takes a userID as parameter and checks in the database. If the user exists, 
returns user object. If not, returns None.
"""
def getUserByID(query):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE user_id=?", (query,))
		result = cursor.fetchall()
		if len(result) == 0:
			return None
		else:
			row = result[0]
			user = User(query, row[1], row[2], row[3])
			return user


""" Takes a username as parameter and 
checks with user ID is associated with that username.
Returns the userID. Assumes the username exists.
"""
def getUserID(query):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (query,))
		result = cursor.fetchall()
		return result[0][0]


"""Gets the users from the database that are not the currently logged in user."""
# def getAvailableFriends():
# 	with sql.connect('database.db') as connection:
# 		connection.row_factory = sql.Row
# 		cursor = connection.cursor()
# 		cursor.execute("SELECT username FROM users WHERE username !=?", (current_user.username,))
# 		result = cursor.fetchall()
# 		return result

@login_manager.user_loader
def load_user(id):
     return getUserByID(id)

# def insert_trip(tripname, destination):
# 	with sql.connect('database.db') as connection:
# 		cursor = connection.cursor()
# 		cursor.execute("INSERT INTO trips (tripname, destination) VALUES (?,?)",(tripname, destination))
# 		connection.commit()


# def lookupLatestTripID():
# 	with sql.connect('database.db') as connection:
# 		cursor = connection.cursor()
# 		result = cursor.execute("SELECT trip_id FROM trips ORDER BY trip_id DESC LIMIT 1").fetchall()
# 		return result[0][0]

# def lookUpTripsForCurrentUser():
# 	with sql.connect('database.db') as connection:
# 		cursor = connection.cursor()
# 		result = cursor.execute("SELECT trips.tripname, trips.destination FROM trips JOIN users_on_trips ON trips.trip_id = users_on_trips.trip_id WHERE users_on_trips.user_id = ?", (current_user.id)).fetchall()
# 		return result

# def insert_user_trip(trip_id, creator, friend):
# 	with sql.connect('database.db') as connection:
# 		cursor1 = connection.cursor()
# 		cursor2 = connection.cursor()
# 		# enter creator 
# 		cursor1.execute("INSERT INTO users_on_trips (user_id, trip_id) VALUES (?,?)",(creator, trip_id))
# 		# enter friend
# 		cursor2.execute("INSERT INTO users_on_trips (user_id, trip_id) VALUES (?,?)",(friend, trip_id))
# 		connection.commit()

# def lookUpTripID(tripName, destiNation):
# 	with sql.connect('database.db') as connection:
# 		cursor = connection.cursor()
# 		result = cursor.execute("SELECT trip_id FROM trips WHERE tripname = ? AND destination = ?", (tripName, destiNation)).fetchall()
# 		return result[0][0]

# def delete_trip(tripID):
# 	with sql.connect('database.db') as connection:
# 		cursor1 = connection.cursor()
# 		cursor1.execute("DELETE FROM trips WHERE trip_id = ?", (tripID,))
# 		# hardcoded second delete in!
# 		cursor2 = connection.cursor()
# 		cursor2.execute("DELETE FROM users_on_trips WHERE trip_id = ?", (tripID,))
# 		connection.commit()

def create_user(username, email, password_hash):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?,?,?)",(username, email, password_hash))
		connection.commit()

def registerBookInDatabase(title, author, thumbnail, short_description, \
        registeredBy, location, currentReader, status):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO books (title, author, thumbnail, short_description, current_location,\
			uploader, current_reader, status) VALUES (?,?,?,?,?,?,?,?)",(title, author, thumbnail, \
				short_description, location, registeredBy, currentReader, status))
		connection.commit()


# def callBooksAPI(query):
# 	url_base = "https://www.googleapis.com/books/v1/volumes?q="
# 	url = url_base + query
# 	response = requests.get(url)
# 	return response




