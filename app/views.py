from flask import render_template, redirect, request, url_for, flash
from app import app, models, db, login_manager
from .forms import LoginForm, SignUpForm
from .models import *
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))


# @app.route('/submit', methods=('GET', 'POST'))
# def submit():
#     form = MyForm()
#     if form.validate_on_submit():
#         return render_template("search.html")
#     return render_template('signup.html')


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
    return render_template('register.html')


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
    registeredBy = current_user.username
    status = 'available'
    bookID = registerBookInDatabase(title, author, thumbnail, short_description, \
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

# def createAndBuyShipment(to_address, from_address, parcel, customs_info):

    shipment = createAndBuyShipment(to_address, from_address, parcel, customsForm)
    # print(shipment.tracking_code)
    print(shipment.postage_label.label_url)
    return redirect(shipment.postage_label.label_url)



# @app.route('/main', methods=['POST'])
# @login_required
# def main2():
#     text = request.form['search_query']
#     print(text)
#     results = callBooksAPI(text)
#     print(results.text)
#     return render_template('searchresults.html')


# @app.route('/create_trip', methods=['GET', 'POST'])
# @login_required
# def create_trip():
#     form = TripForm()
#     form.set_choices();
#     if form.validate_on_submit():
#         destination = form.destination.data
#         friend = form.friend.data
#         tripname = form.tripname.data
#         insert_trip(tripname, destination)
#         tripID = lookupLatestTripID()
#         creatorID = int (current_user.id)
#         friendID = getUserByUsername(friend).id #might break if not exists! need dropdown
#         insert_user_trip(tripID, creatorID, friendID)
#         return redirect('/trip_detail') 

#     return render_template('trips.html', form = form) # this is what gets called without form


# @app.route('/trip_detail')
# @login_required
# def display_trip():
#     trips = lookUpTripsForCurrentUser()
#     return render_template('TripDetail.html', trips = trips)


# @app.route('/delete-trip', methods=['GET', 'POST'])
# @login_required
# def deleteTrip():
#     tripname = request.form.get('tripname')
#     destination = request.form.get('destination')
#     tripID = lookUpTripID(tripname, destination)
#     delete_trip(tripID)
#     return redirect('/trip_detail') 


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

@app.route('/book')
def book():
    return render_template('book.html')

# @app.route('/create_order/<value>', methods=['GET', 'POST'])
# def create_order(value):
#     form = OrderForm()
#     if form.validate_on_submit():
#         name_of_part = form.name_of_part.data
#         manufacturer_of_part = form.manufacturer_of_part.data
#         insert_order(name_of_part, manufacturer_of_part, value)
#         order_id = retrieve_order_id()
#         insert_customer_order(value, order_id)
#         return redirect('/customers')
#     return render_template('order.html', form = form)



