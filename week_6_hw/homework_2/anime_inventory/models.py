from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
import uuid 
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

from flask_login import login_manager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    anime = db.relationship('Anime', backref = 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'


class Anime(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    year_released = db.Column(db.String(150), nullable = True)
    watch_time = db.Column(db.String(100), nullable = True)
    number_episodes = db.Column(db.String(100))
    number_of_seasons = db.Column(db.String(100))
    rating = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    animation = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, year_released, watch_time, number_episodes, number_of_seasons, rating, cost_of_production, animation, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.year_released = year_released
        self.watch_time = watch_time
        self.number_episodes = number_episodes
        self.number_of_seasons = number_of_seasons
        self.rating = rating
        self.cost_of_prod = cost_of_production
        self.animation = animation
        self.user_token = user_token


    def __repr__(self):
        return f'The following Anime has been added: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())


class AnimeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'price', 'year_released', 'watch_time', 'number_episodes', 'number_of_seasons', 'rating', 'cost_of_production', 'animation']


anime_schema = AnimeSchema()
animes_schema = AnimeSchema(many = True)