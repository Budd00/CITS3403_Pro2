# from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
# from hashlib import md5
from app import db

#the tables of sql and related caculations are wirtten here

class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Is_adm = db.Column(db.Integer)
    mark = db.Column(db.Integer)
    answer = db.relationship('answer', backref='author', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return self.id
    


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    

class questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), unique=True)
    stand_answer = db.Column(db.String(500), unique=True)
    mark = db.Column(db.Integer)
    answer = db.relationship('answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<questions {}>'.format(self.body)


class answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id=db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(500), unique=True)    
    def __repr__(self):
        return '<answer {}>'.format(self.body)
       
