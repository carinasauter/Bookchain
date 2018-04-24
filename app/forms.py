from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FormField
from wtforms.validators import DataRequired, Required
from wtforms.fields.html5 import EmailField
from .models import *
from flask_material import Material 

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
	
