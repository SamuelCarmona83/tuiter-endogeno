from flask_sqlalchemy import SQLAlchemy
import arrow
import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Tweet(db.Model): #Query

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(280), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    #author_id
    def __init__(self, content):
        self.content = content
        self.date = datetime.datetime.today()

    def __repr__(self):
        return '<Tweet => %r>' % self.idW
    
    def serialize(self):
        return {
            "content": self.content,
            "date": arrow.get(self.date).humanize()
        }