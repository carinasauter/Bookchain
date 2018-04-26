import unittest
from app.models import *

username = "testuser"
email = "test@test.com"
password_hash = ""
full_name = "Test User"
street = "2822 Garber Street"
city = "Berkeley"
state = "CA"
country = 'USA'
zipcode = "94705"
testUser = User(username, email, password_hash, full_name, street, city, state, country, zipcode)

title = "Harry Potter and the Chamber of Secrets"
author = "Joanne K Rowling"
thumbnail = "image link"
thumbnail_small = "small image link"
short_description = "great story about a young wizard and his friends"
isbn = "123456789"
registeredBy = "testuser"
holder = "testuser"
status = "available"
book = Book(title, author, thumbnail, thumbnail_small, short_description, isbn, registeredBy, holder, status)

def test_createUser():
	assert username == testUser.username and email == testUser.email and \
	password_hash == testUser.password_hash and full_name == testUser.full_name and \
	street == testUser.street and city == testUser.city and state == testUser.state and \
	country == testUser.country and zipcode == testUser.zipcode


def test_addToDatabase():
	testUser.addToDatabase()
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		check = cursor.execute("SELECT username from users order by user_id desc limit 1").fetchall()
	assert check[0][0] == username


def test_getLocationGeocode():
	lat, lon = testUser.getLocationGeocode()
	assert type(3.34) == type(lat) and type(3.34) == type(lon)

def test_getUserByUsername():
	user = getUserByUsername(username)
	assert user == testUser

# def test_getUserByID():
# 	user = getUserByID(5)
# 	assert user == testUser


def test_createBook():
	assert title == book.title and author == book.author and thumbnail == book.thumbnail \
	and short_description == book.short_description and isbn == book.isbn and \
	registeredBy == book.registeredBy


def test_getStarRating():
	starRating = getStarRating(3.85)
	assert len(starRating) == 4


def test_cleanup():
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("DELETE FROM users WHERE username = ?", (username,))
		connection.commit()
