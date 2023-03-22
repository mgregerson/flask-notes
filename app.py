import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNote, EditNote
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
        return redirect(f'/users/{this_user}')

    user = User.query.get_or_404(username)
    print('I am the user!!!!!!!!!', user)
    notes = user.notes

    return render_template('user_profile.html', user=user, form=form, notes=notes)


@app.post("/logout")
def handle_logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)
        print(session, 'this is the session')
    # Add flash message notifying user they have logged out.
    return redirect("/")


@app.delete('/users/<username>/delete')
def delete_user_and_notes(username):
    """do me"""
    form = CSRFProtectForm()

    this_user = session.get('username')

    if this_user == None:
        return redirect('/')
    elif this_user != username:
        return redirect(f'/users/{this_user}')

    user = User.query.get_or_404(username)
    db.session.delete(user.notes)
    db.session.delete(user)
    db.session.commit()

    session.pop("username", None)
    return redirect('/')


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def show_add_note_form(username):
    """do"""
    this_user = session.get('username')

    if this_user == None:
        return redirect('/')
    elif this_user != username:
        return redirect(f'/users/{this_user}')

    form = AddNote()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = username

        note = Note(title=title, content=content, owner=owner)
        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('add_note.html', form=form)


@app.route('/notes/<int:id>/update', methods=['GET', 'POST'])
def edit_note(id):
    """do this you pig"""
    print('We are in the edit note function')
    note = Note.query.get_or_404(id)
    this_user = session.get('username')
    print('I am from the edit note thing', this_user, note)

    if this_user == None:
        return redirect('/')
    elif this_user != note.user.username:
        return redirect(f'/users/{this_user}')


    form = EditNote(obj=note)
    print(form, 'I am the form in edit note')

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        print(title, content, "I am the title in validate")

        note.title = title
        note.content = content

        db.session.commit()
        return redirect(f'/users/{note.user.username}')

    return render_template('edit_note.html', form=form)


