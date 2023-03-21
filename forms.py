from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Email
from wtforms.validators import InputRequired



class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField('Input Username', 
                           validators=[InputRequired(message='Please add a username!')])
    
    password = PasswordField('Input Password', 
                             validators=[InputRequired(message='What, you want anyone to get in? Add a password, fool!')])

    email = StringField('Input email', validators=[InputRequired(message='Add a valid email!'), Email()])

    first_name = StringField('Input first name', validators=[InputRequired(message='Input first name')])

    last_name = StringField('Input last name', validators=[InputRequired(message='Input last name.')])

class LoginForm(FlaskForm):
    """Form for logging in a user"""


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""