import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm, CSRFProtectForm
from auth_utils import check_for_unique_username

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():
    """Redirects user to the register page. """

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """GET: Shows a form that allows a user to register as a new user.
       POST: Processes the registration of a new user and sends it to the database. Redirect to
      '/users/username' """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        is_unique = check_for_unique_username(username)
        if not is_unique:
            form.username.errors = [f'{username} is not unique!']
            return render_template('register.html', form=form)
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)
        # TODO: Add try/catch (is the user unique or not?)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(f'/users/{username}')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    """On GET Show login form that allows the user to login.
    On POST Processes the login of a user and sends it to the session"""

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
# TODO: Change variable name to user
        authenticate_user = User.authenticate(username, password)

        if authenticate_user:
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Bad name/password"]
    
    return render_template('login.html', form=form)
    

@app.get('/users/<username>')
def display_user_profile(username):
    """Displays users profile and includes logout button. Redirects user to their page if 
    attempting to access another users page, redirects a user that is not logged in."""

    form = CSRFProtectForm()

    this_user = session.get('username')

    if this_user == None:
        return redirect('/')
    elif this_user != username:
        return redirect (f'/users/{this_user}')

    user = User.query.get_or_404(username)
    
    unique_username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    user_details = [unique_username, email, first_name, last_name]

    return render_template('user_profile.html', user_details=user_details, form=form)


@app.post("/logout")
def handle_logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # TODO: Remove None from line below
        session.pop("username", None)
        print(session, 'this is the session')
    # Add flash message notifying user they have logged out.
    return redirect("/")
