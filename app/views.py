from flask import render_template, redirect, request, url_for, flash
from app import app, models, db, login_manager
from .forms import LoginForm, SignUpForm
from .models import *
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')  
def hello_world():
      form = LoginForm()   
      return render_template('search.html', form = form)  



# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         return redirect(url_for('main'))
#     else:
#         # we should have a landing page for user who have not logged in or signed up
#         return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = getUserByUsername(username) #checks if user already exists
        if user is not None:
            # in this case user with this username exists already
            flash("Username already exists. Please pick a different one.")
            return render_template('signup.html', title = "Sign Up", form = form)
        # in case it does not exist
        password_hash = generate_password_hash(password)
        create_user(username, email, password_hash) # creates user in database
        userID = getUserID(username)
        user = User(userID, username, email, password_hash)
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
    return render_template('login.html', title='Log In', form=form)



@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username


@app.route('/main')
@login_required
def main():
    return 'this is the main page.'


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
