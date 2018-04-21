import unittest
from app.models import *


def test_createUser():
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
	assert username == testUser.username and email == testUser.email and password_hash == testUser.password_hash


