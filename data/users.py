import sqlalchemy
from sqlalchemy import orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from . import db_session


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__  = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    
    def __repr__(self):
        return f"<User> {self.id} {self.surname} {self.name}"
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        
    def check_password(self, phash, password):
        return check_password_hash(phash, password)
    
    def add_user(self, login, password, email):
        session = db_session.create_session()
        if session.query(User).filter(User.login == login).first() or session.query(User).filter(User.email == email).first():
            return False
        self.login = login
        self.set_password(password)
        self.email = email
        session.add(self)
        session.commit()
        return True
    
    def login_user(self, login, password):
        session = db_session.create_session()
        if session.query(User).filter(User.login == login).first():
            user = session.query(User).filter(User.login == login).first()
            if user.check_password(user.hashed_password, password):
                return True # user logged in
            else:
                print("incorrect password")
                return False # incorrect password
        else:
            print("user not found")
            return False # user not found
#jobs = orm.relationship("Jobs", back_populates='user')