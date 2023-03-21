import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///users")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():
  """Redirects user to the register page. """

  form = CSRFProtectForm()

  return redirect('/register', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
  """GET: Shows a form that allows a user to register as a new user.
     POST: Processes the registration of a new user and sends it to the database. Redirect to 
    '/secret' """
  
  form = RegisterForm

  if form.validate_on_submit():

    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data

    user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()

    session['username'] = user.username

    return redirect('/secret')
  
  else:
    return render_template('register.html', form=form)



  


