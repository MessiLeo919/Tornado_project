from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.sql import exists

from .db import Base, DBSession

session = DBSession()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=True)
    created = Column(DateTime, default=datetime.now())
    email = Column(String(50))
    last_login = Column(DateTime)

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(User.name == username)).scalar()

    @classmethod
    def add_user(cls, username, password, email=''):
        user = User(name=username, password=password,
                    email=email, last_login=datetime.now())
        session.add(user)
        session.commit()
    @classmethod
    def get_pass(cls, name):
        user = session.query(cls).filter_by(name=name).first()
        if user:
            return user.password
        else:
            return ''


if __name__ == '__main__':
    Base.metadata.creat_all()