from flask import render_template, redirect, request, url_for, flash
from app import app, models, db, login_manager
from .forms import LoginForm, SignUpForm, CommentForm
from .models import *
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import json
from markupsafe import Markup



@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        country = form.country.data
        zipcode = form.zipcode.data
        user = getUserByUsername(username) #checks if user already exists
        if user is not None:
            # in this case user with this username exists already
            flash("Username already exists. Please pick a different one.")
            return render_template('signup.html', title = "Sign Up", form = form)
        # in case it does not exist
        password_hash = generate_password_hash(password)
        create_user(username, email, password_hash, full_name, street, city, state, country, zipcode) # creates user in database
        userID = getUserID(username)
        user = User(userID, username, email, password_hash, full_name, street, city, state, country, zipcode)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html', title = "Sign Up", form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        comparedUser = getUserByUsername(username)
        if comparedUser is None or not check_password_hash(comparedUser.password_hash, password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(comparedUser, remember = form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Log In', form = form)



@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username


@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET'])
@login_required
def register():
    return render_template('register.html')

@app.route('/registerBook', methods=['POST'])
@login_required
def registerbook():
    title = request.form['title']
    author = request.form['author']
    thumbnail = request.form['thumbnail']
    short_description = request.form['short_description']
    isbn = request.form['isbn']
    registeredBy = current_user.username
    status = 'available'
    # print(title, author, thumbnail, short_description, isbn, registeredBy, status)
    bookID = registerBookInDatabase(title, author, thumbnail, short_description, isbn, \
        registeredBy, status)
    addBookToUser(current_user.username, bookID, 'uploader')
    return 'Received!'



@app.route('/printLabel', methods=['POST'])
@login_required
def printLabel():
    userID = current_user.id
    requester = request.form['requester']
    requester = getUserByUsername(requester)
    shipper = getUserByID(userID)
    print(shipper.username + " wants to ship a book!")
    print(requester.username + " wants to receive a book!")
    from_address = createAddress(shipper.full_name, shipper.street, shipper.city, \
        shipper.state, shipper.zipcode, shipper.country)
    to_address = createAddress(requester.full_name, requester.street, requester.city, \
        requester.state, requester.zipcode, requester.country)
    parcel = createParcel()
    customsForm = createCustomsForm()
    shipment = createAndBuyShipment(to_address, from_address, parcel, customsForm)
    print(shipment.postage_label.label_url)
    return redirect(shipment.postage_label.label_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/getMap', methods=['GET'])
@login_required
def creatingMap():
    book_id = request.args['book_id']
    # print("This is the book ID that's being passed: ")
    # print(book_id)
    users = getBookHistory(book_id)
    data = []
    for user in users:
        user_info = getUserByID(user)
        # print("this is the user whose info is used for the map")
        # print(user_info.username)
        lat, lon = getGeocodedAddressFromUser(user_info)
        data.append([lon, lat])
    json_data = json.dumps(data)
    return json_data


@app.route('/getUser', methods=['GET'])
@login_required
def getUser():
    userID = current_user.id
    user = getUserByID(userID)
    username = user.username
    data = []
    data.append(username,)
    json_data = json.dumps(data)
    return json_data



@app.route('/book/<book_id>', methods=['GET','POST'])
@login_required
def book(book_id):
    form = CommentForm()
    title, author, thumbnail, short_description, isbn, uploader, location = getBookDetails(book_id)
    # average_rating = getGoodReadsReviews(isbn)
    review = nyt_reviews(isbn)
    stops = len(getBookHistory(book_id))
    currentUser = current_user.id
    haver = hasBook(book_id)
    blockRequest = 0
    if int(currentUser) == int(haver):
        blockRequest = 1
    return render_template('book.html', book_id = book_id, title = title, author = author, \
        thumbnail = thumbnail, short_description = Markup(short_description), uploader = uploader, \
        location = location, average_rating= 2.34, stops=stops, review = review, form=form, blockRequest = blockRequest)


@app.route('/acknowledgeReceipt', methods=['POST'])
@login_required
def acknowledgingReceipt():
    book_id = request.form['book_id']
    acknowledgeReceipt(book_id)


@app.route('/requestBook', methods=['POST'])
@login_required
def toRequestBook():
    requester = current_user.id
    book_id = request.form['book_id']
    book_haver = hasBook(book_id)
    if book_haver != requester:
        requestBook(requester, book_id)
    return "requested"


@app.route('/addReview', methods=['POST'])
@login_required
def addingReview():
    comment = request.form['comment']
    book_id = request.form['book_id']
    user_id = current_user.id
    addReviewToDB(book_id, user_id, comment)
    return 'added review'

@app.route('/addRating', methods=['POST'])
@login_required
def addingRating():
    print("received rating registration request")
    rating = request.form['rating']
    book_id = request.form['book_id']
    user_id = current_user.id
    addRatingToDB(book_id, user_id, rating)
    return 'added rating'


