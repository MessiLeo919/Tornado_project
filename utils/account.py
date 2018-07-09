from datetime import datetime
import hashlib
from models.account import User, session


def hash_it(password):
    return hashlib.md5(password.encode('utf8')).hexdigest()

def authenticate(username, passsword):
    if username and passsword:
        hash_pass = User.get_pass(username)
        if hash_pass and hash_it(passsword) == hash_pass:
            return True
    return False

def login(username):
    t = datetime.now()
    print("user:{} login at {}".format(username, t))
    session.query(User).filter_by(name=username).update({
        User.last_login:t
    })

def register(username, password, email):
    if User.is_exists(username):
        return {'msg': 'username exists'}
    hash_pass = hash_it(password)
    User.add_user(username, hash_pass, email)
    return {'msg': 'OK'}
