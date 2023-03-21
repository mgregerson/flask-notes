"""Seed file to make sample data for users db."""

from models import User, db, connect_db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# User.query.delete()

# Add Users
matt = User.register(username='mgregerson', password='password', email='testemail@google.com', first_name='Matt', last_name='Gregerson')
vaughn = User.register(username='Vaughn', password='password', email='anothertestemail@google.com', first_name='Vaugn', last_name='Seekamp')
theRock = User.register(username='HUGEGUY', password='password2', email='itsaboutfamily@google.com', first_name='The', last_name='Rock')

# Add new objects to session, so they'll persist
db.session.add(matt)
db.session.add(vaughn)
db.session.add(theRock)
