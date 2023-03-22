"""Seed file to make sample data for users db."""

from models import User, db, connect_db, Note
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

db.session.commit()

# Create Notes

note1 = Note(title='a good title', content='dope content', owner='Vaughn')
note2 = Note(title='a cool title', content='chill content', owner='mgregerson')
note3 = Note(title='a great title', content='high content', owner='Vaughn')

db.session.add(note1)
db.session.add(note2)
db.session.add(note3)

db.session.commit()