import os
import time
from datetime import date
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    engine = create_engine(database_path)
    if not database_exists(engine.url):
    	create_database(engine.url)

    db.create_all()


'''
Movie_items
'''
movie_items = db.Table('movie_items',
                       db.Column('movie_id', db.Integer, db.ForeignKey(
                           'movie.id'), primary_key=True),
                       db.Column('actor_id', db.Integer, db.ForeignKey(
                           'actor.id'), primary_key=True)
                       )


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    actors = db.relationship('Actor', secondary=movie_items,
                             backref=db.backref('movies'))

    def __init__(self, title, date):
        self.title = title
        self.date = date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'actors': [actor.name for actor in self.actors]
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer())
    gender = db.Column(db.String())

    def __init__(self, name, age, gender):
        self.name = name,
        self.age = age,
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
