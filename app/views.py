from flask import render_template, redirect, request, url_for, flash
from app import app, models, db, login_manager
from .forms import LoginForm, SignUpForm
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
        newUser = User(username, email, password_hash, full_name, street, city, state, country, zipcode)
        newUser.addToDatabase()
        login_user(newUser)
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
    newBook = Book(title, author, thumbnail, short_description, isbn, \
        registeredBy)
    print("do I get here?")
    newBook.addToDatabase()
    current_user.addBook(newBook)
    Print("tried to do second thing")
    return 'Received!'



@app.route('/printLabel', methods=['GET'])
@login_required
def printLabel():
    userID = current_user.id
    requester = request.args['requester']
    requester = getUserByUsername(requester)
    shipper = getUserByID(userID)
    from_address = createAddress(shipper.full_name, shipper.street, shipper.city, \
        shipper.state, shipper.zipcode, shipper.country)
    to_address = createAddress(requester.full_name, requester.street, requester.city, \
        requester.state, requester.zipcode, requester.country)
    parcel = createParcel()
    customsForm = createCustomsForm()
    shipment = createAndBuyShipment(to_address, from_address, parcel, customsForm)
    print(shipment.postage_label.label_url)
    json_data = json.dumps(shipment.postage_label.label_url)
    print(json_data)
    return json_data


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/getMap', methods=['GET'])
@login_required
def creatingMap():
    book_id = request.args['book_id']
    book = getBookById(book_id)
    users = book.getHistory()
    data = []
    for userId in users:
        user = getUserByID(userId)
        lat, lon = user.getLocationGeocode()
        data.append([lon, lat])
    json_data = json.dumps(data)
    return json_data

@app.route('/getMapForUser', methods=['GET'])
@login_required
def creatingMapForUser():
    user_id = request.args['user']
    user = getUserByID(user_id)
    books = user.uploadedBooks()
    data = []
    for bookId in books:
        book = getBookById(bookId)
        currentPossessor = book.getPossessor()
        lat, lon = currentPossessor.getLocationGeocode()
        data.append([lon, lat])
    json_data = json.dumps(data)
    return json_data


@app.route('/getUser', methods=['GET'])
@login_required
def getUser():
    username = current_user.username
    data = []
    data.append(username,)
    json_data = json.dumps(data)
    return json_data



@app.route('/book/<book_id>', methods=['GET','POST'])
@login_required
def book(book_id):
    book = getBookById(book_id)
    possessor = book.getPossessor()
    print(possessor.id)
    location = book.getLocationString()
    average_rating = book.getAverageRating()
    average_rating = format(average_rating, '.1f')
    review = book.nytReview()
    comments = book.getComments()
    stops = len(book.getHistory())
    currentUser = current_user
    userRating = book.getRating(currentUser)
    blockRequest = 0
    print(currentUser.id)
    print(possessor == currentUser)
    if possessor == currentUser or currentUser.hasRequested(book):
        print("block request 1")
        blockRequest = 1
    return render_template('book.html', book_id = book_id, title = book.title, author = book.author, \
        thumbnail = book.thumbnail, short_description = Markup(book.short_description), uploader = book.registeredBy, \
        location = location, average_rating= average_rating, stops=stops, review = review, blockRequest = blockRequest, \
        comments = comments, userRating = userRating)



@app.route('/user/<user_id>', methods=['GET','POST'])
@login_required
def profile(user_id):
    profileUser = getUserByID(user_id)
    profileUserName = profileUser.username
    # comments = 
    uploadedBooks = profileUser.uploadedBooks()
    lstUploadedBooks = []
    for bookId in uploadedBooks:
        book = getBookById(bookId)
        lstUploadedBooks.append([book.title, book.author, book.thumbnail])
    return render_template('profile.html', uploaded_books = lstUploadedBooks, username = profileUserName)




@app.route('/acknowledgeReceipt', methods=['POST'])
@login_required
def acknowledgingReceipt():
    book_id = request.form['book_id']
    book = getBookById(book_id)
    current_user.acknowledgeReceipt(book)
    return 'acknowledged'


@app.route('/requestBook', methods=['POST'])
@login_required
def toRequestBook():
    requester = current_user
    book_id = request.form['book_id']
    book = getBookById(book_id)
    possessor = book.getPossessor()
    if possessor.getId() != requester.getBookById() and not requester.hasRequested(book):
        requester.requestBook(book)
    return "requested"


@app.route('/addReview', methods=['POST'])
@login_required
def addingReview():
    comment = request.form['comment']
    book_id = request.form['book_id']
    book = getBookById(book_id)
    user = current_user
    book.addReview(user, comment)
    return 'added review'

@app.route('/addRating', methods=['POST'])
@login_required
def addingRating():
    rating = request.form['rating']
    book_id = request.form['book_id']
    user = current_user
    book = getBookById(book_id)
    book.addRating(user, rating)
    return 'added rating'


