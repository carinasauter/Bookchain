import sqlite3 as sql
from app import login_manager, db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import requests
import json
import easypost

class User(UserMixin):

	def __init__(self, id_number, username, email, password_hash, full_name, street, city, state, country, zipcode):
		self.id = id_number;
		self.username = username
		self.email = email
		self.password_hash = password_hash
		self.full_name = full_name
		self.street = street
		self.city = city
		self.state = state
		self.country = country
		self.zipcode = zipcode


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
			user = User(row[0], query, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
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
			user = User(query, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
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

@login_manager.user_loader
def load_user(id):
     return getUserByID(id)


def create_user(username, email, password_hash, full_name, street, city, state, country, zipcode):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO users (username, email, password_hash, full_name, street,\
		city, state, country, zipcode) VALUES (?,?,?,?,?,?,?,?,?)",(username, email, password_hash, \
		full_name, street, city, state, country, zipcode))
		connection.commit()

def registerBookInDatabase(title, author, thumbnail, short_description, isbn, \
        registeredBy, status):
	with sql.connect('database.db') as connection:
		cursor1 = connection.cursor()
		cursor2 = connection.cursor()
		cursor1.execute("INSERT INTO books (title, author, thumbnail, short_description, isbn,\
		uploader, status) VALUES (?,?,?,?,?,?,?)",(title, author, thumbnail, \
		short_description, isbn, registeredBy, status))
		cursor2.execute("SELECT LAST_INSERT_ROWID()")
		bookID = cursor2.fetchall()
		bookID = bookID[0][0]
		connection.commit()
		return bookID


def addBookToUser(userinfo, book_id, relationship):
	user_id = getUserID(userinfo)
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO books_users (user_id, book_id, relationship) VALUES (?,?,?)",(user_id, book_id, relationship))
		connection.commit()


# Print shipping label
easypost.api_key = '3So8pVF6yhYekwW91WrP5g'

def createAddress(full_name, street, city, state, zipcode, country):
	return easypost.Address.create(verify=["delivery"],name = full_name,\
		street1 = street, street2 = "", city = city, state = state, zip = zipcode,\
		country = country)


def createParcel():
	try:
	    parcel = easypost.Parcel.create(
	        predefined_package = "Parcel",
	        weight = 21.2
	    )
	except easypost.Error as e:
	    print(str(e))
	    if e.param is not None:
	        print('Specifically an invalid param: %r' % e.param)

	parcel = easypost.Parcel.create(
	    length = 10.2,
	    width = 7.8,
	    height = 4.3,
	    weight = 21.2
	)
	return parcel

# create customs_info form for intl shipping
def createCustomsForm():
	customs_item = easypost.CustomsItem.create(
	    description = "book from BookChain",
	    hs_tariff_number = 123456,
	    origin_country = "US",
	    quantity = 2,
	    value = 96.27,
	    weight = 21.1
	)
	customs_info = easypost.CustomsInfo.create(
	    customs_certify = 1,
	    customs_signer = "Hector Hammerfall",
	    contents_type = "gift",
	    contents_explanation = "",
	    eel_pfc = "NOEEI 30.37(a)",
	    non_delivery_option = "return",
	    restriction_type = "none",
	    restriction_comments = "",
	    customs_items = [customs_item])
	return customs_info


# create shipment
def createAndBuyShipment(to_address, from_address, parcel, customs_info):
	shipment = easypost.Shipment.create(
	    to_address = to_address,
	    from_address = from_address,
	    parcel = parcel,
	    customs_info = customs_info)
	shipment.buy(rate = shipment.lowest_rate())
	return shipment

# get book uploader - takes book_id and returns user_id
def getBookUploader(book_id):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT user_id FROM books_users WHERE book_id=? and relationship=?", (book_id, 'uploader'))
		result = cursor.fetchall()
		return result[0][0]


"""
takes a book_id and returns a list of the users in the history of the book.
Ignores those users that just have relationship 'requester'
"""
def getBookHistory(book_id):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT user_id FROM books_users WHERE book_id=? AND relationship!=?", (book_id, 'requester'))
		result = cursor.fetchall()
		users = []
		for entry in result:
			users.append(entry[0])	
		return users

"""
registers a user_id book_id pair in the database. Relationship status is set to 'requester'
"""
def requestBook(user_id, bookID):
	relationship = 'requester'
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor1 = connection.cursor()
		cursor2 = connection.cursor()
		cursor1.execute("INSERT INTO books_users (user_id, book_id, relationship) VALUES (?,?,?)",(user_id, bookID, relationship))
		cursor2.execute("UPDATE books SET status = ? WHERE book_id = ?", ('requested' ,bookID))
		connection.commit()


"""
checks who currently has the book. The person who has the book is defined as the 
last person be associated with the book in a relationship that is not 'requester. 
Takes book_id and returns user_id
"""
def hasBook(book_id):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		result = cursor.execute("SELECT user_id FROM books_users WHERE book_id=? AND relationship !=?", (book_id, 'requester')).fetchall()
		return result[-1][0]




googleGeocodingAPIKey = 'AIzaSyAVu5x4ezPVUSr6BEQ8I41BN65R6w8D5uI'


"""
takes a user object and returns the lon and lat for the user's city, state and country.
Further accuracy not provided due to privacy considerations.
"""
def getGeocodedAddressFromUser(user):
	city = user.city
	city = city.replace(" ", "+")
	state = user.state
	state = state.replace(" ", "+")
	country = user.country
	country = country.replace(" ", "+")
	googleBaseURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	apiKey = "&key=" + googleGeocodingAPIKey
	query = googleBaseURL + city + ",+" + state + ",+" + country + apiKey
	result = requests.get(query)
	result = json.loads(result.text)
	result_parsed = result['results'][0]['geometry']['location']
	# print(result_parsed)
	user_lat = result_parsed['lat']
	user_lon = result_parsed['lng']
	return user_lat, user_lon


"""
acknowledges receipt of a book.
"""
def acknowledgeReceipt(book_id):
	relationship = 'reading'
	user_id = current_user.id
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("INSERT INTO books_users (user_id, book_id, relationship) VALUES (?,?,?)",(user_id, book_id, relationship))
		connection.commit()


"""
takes a bookID and returns all details about the book
"""

def getBookDetails(book_id):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		result = cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,)).fetchall()
		title = result[0][1]
		author = result[0][2]
		thumbnail = result[0][3]
		short_description = result[0][4]
		isbn = result[0][5]
		uploader = result[0][6]
		current_user_id = hasBook(book_id)
		current_user = getUserByID(current_user_id)
		location = current_user.city + ", " + current_user.state + ", " + current_user.country
		return title, author, thumbnail, short_description, isbn, uploader, location


NYTAPIKey = '3070504f115249fc8eedadaa0089f3c6'

def nyt_reviews(isbn):
	nYTimesBaseURI = 'http://api.nytimes.com/svc/books/v3/reviews.json?isbn='
	query = nYTimesBaseURI + str(isbn) + '&api-key=' + NYTAPIKey
	result = requests.get(query)
	if result.status_code == 200:
		result = json.loads(result.text)
		result = result['results']
		if result != []:
			result = result[0]['summary']
			return result
	return ""

def addRatingToDB(book_id, user_id, rating):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("INSERT INTO ratings (book_id, user_id, rating) VALUES (?,?,?)",(book_id, user_id, rating))
		connection.commit()

def addReviewToDB(book_id, user_id, comment):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("INSERT INTO comments (book_id, user_id, comment) VALUES (?,?,?)",(book_id, user_id, comment))
		connection.commit()


def getBookComments(book_id):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		result = cursor.execute("SELECT comment, user_id FROM comments where book_id = ? ORDER BY comment_id DESC LIMIT ?", (book_id, 5)).fetchall()
		lst = []
		for entry in result:
			lst.append([entry[0], getUserByID(entry[1]).username])
		return lst


def getBookRating(book_id, user_id):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT rating FROM ratings where book_id = ? AND user_id = ?", (book_id, user_id)).fetchall()
		print(result)
		if result == []:
			return 0
		return result[0][0]

def getAverageRating(book_id):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		ratings = cursor.execute("SELECT rating FROM ratings where book_id = ?", (book_id,)).fetchall()
		if ratings == []:
			return 0
		sum_ratings = 0
		count_ratings = 0
		for rating in ratings:
			count_ratings += 1
			sum_ratings += rating[0]
		return sum_ratings / count_ratings


def getBooksUploadedByUser(user_id):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT book_id FROM books_users WHERE user_id = ? AND relationship = ?", (user_id, "uploader")).fetchall()
		lst = []
		for entry in result:
			lst.append(entry[0])
		return lst


def hasRequested(user_id, book_id):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT relationship FROM books_users WHERE user_id = ? AND book_id = ? ORDER BY user_book_id DESC LIMIT 1", (user_id, book_id )).fetchall()
		print("this is the has requested result")
		print(result)
		if result == [] or result[0][0] != 'requester':
			print("false")
			return False
		print("true")
		return True
