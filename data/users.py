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
        
    def check_password(self, password):
        return check_password_hash(password)
    
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
#jobs = orm.relationship("Jobs", back_populates='user')