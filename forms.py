from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""
# TODO: Add validators for to check user class constraints 
    username = StringField('Input Username',
                           validators=[InputRequired(message='Please add a username!')])

    password = PasswordField('Input Password',
                             validators=[InputRequired(message='What, you want anyone to get in? Add a password, fool!')])

    email = EmailField('Input email', validators=[
                       InputRequired(message='Add a valid email!'), Email()])

    first_name = StringField('Input first name', validators=[
                             InputRequired(message='Input first name')])

    last_name = StringField('Input last name', validators=[
                            InputRequired(message='Input last name.')])


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField('Input Username',
                       validators=[InputRequired(message='Please add a username!')])
    password = PasswordField('Input Password',
                         validators=[InputRequired(message='What, you want anyone to get in? Add a password, fool!')])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
