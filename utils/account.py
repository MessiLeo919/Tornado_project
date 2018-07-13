from datetime import datetime
import hashlib
from models.account import User, session, Post


def hash_it(password):
    return hashlib.md5(password.encode('utf8')).hexdigest()


def authenticate(username, passsword):
    if username and passsword:
        hash_pass = User.get_pass(username)
        if hash_pass and hash_it(passsword) == hash_pass:
            return True
    return False


def login_time_update(username):
    t = datetime.now()
    # print("user:{} login at {}".format(username, t))
    session.query(User).filter_by(name=username).update({
        User.last_login : t
    })


def register(username, password, email):
    if User.is_exists(username):
        return {'msg': 'username exists'}
    hash_pass = hash_it(password)
    User.add_user(username, hash_pass, email)
    return {'msg': 'OK'}

def add_post_for(username, image_url, thumb_url):
    '''
    保存特定用户的图片
    '''
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url,  user=user)
    session.add(post)
    session.commit()
    return post.id


def get_post_for(username):
    user = session.query(User).filter_by(name=username).first()
    posts = session.query(Post).filter_by(user=user)
    return posts

def get_post(post_id):
    """
    获取指定id的post
    :param post_id:
    :return:
    """
    post = session.query(Post).get(post_id)
    return post

def get_all_posts():
    """
    得到所有的用户
    :return:
    """
    posts = session.query(Post).order_by(Post.id.desc()).all()
    return posts

