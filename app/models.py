from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)

    # Relationships
    artworks = db.relationship('Artwork', backref='artist', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    purchases = db.relationship('Purchase', backref='user', lazy=True)

    def __init__(self, name, email, password, is_artist=False):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_artist = is_artist

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

class Artwork(db.Model):
    __tablename__ = 'artworks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='artwork', lazy=True)
    purchases = db.relationship('Purchase', backref='artwork', lazy=True)

    def __repr__(self):
        return f'<Artwork {self.title}, Artist {self.artist.name}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Ensure between 1 and 5

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.rating} for Artwork {self.artwork.title} by User {self.user.name}>'

from datetime import datetime

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, default=datetime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)

    def __repr__(self):
        return f'<Purchase of Artwork {self.artwork.title} by User {self.user.name} on {self.purchase_date}>'
