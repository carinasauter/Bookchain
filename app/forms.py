from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FormField
from wtforms.validators import DataRequired, Required
from wtforms.fields.html5 import EmailField
from .models import *
from flask_material import Material 

# class TripForm(Form):
# 	tripname = StringField('tripname', validators=[DataRequired()])
# 	destination = StringField('destination', validators=[DataRequired()])
# 	friend = SelectField('friend', validators=[DataRequired()])
# 	submit = SubmitField('Create Trip')

# 	def set_choices(self):
# 		friends = getAvailableFriends()
# 		self.friend.choices = [(friend[0],friend[0]) for friend in friends]


class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')


class SignUpForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	email = EmailField('Email', validators = [DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	full_name = StringField('Full Name', validators=[DataRequired()])
	street = StringField('Street', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	country = StringField('Country', validators=[DataRequired()])
	zipcode = IntegerField('Zipcode', validators=[DataRequired()])


class CommentForm(Form):
	comment = StringField('Leave a review...', validators=[DataRequired()])
	
