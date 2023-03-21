from models import User

def check_for_unique_username(username):
    """Checks input username in db to see if unique"""

    users = User.query.all()
    usernames = []
    for user in users:
        usernames.append(user.username)
    if username in usernames:
        return False
    else:
        return True


