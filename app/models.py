from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update to your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Artwork Model
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist = db.relationship('User', backref=db.backref('artworks', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    artwork = db.relationship('Artwork', backref=db.backref('reviews', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create all tables
with app.app_context():
    db.create_all()

# User Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users]), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        is_artist=data.get('is_artist', False)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.is_artist = data.get('is_artist', user.is_artist)
        db.session.commit()
        return jsonify({'id': user.id}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

# Artwork Routes
@app.route('/api/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    return jsonify([{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist_id': artwork.artist_id
    } for artwork in artworks]), 200

@app.route('/api/artworks/<int:artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    artwork = Artwork.query.get(artwork_id)
    if artwork:
        return jsonify({
            'id': artwork.id,
            'title': artwork.title,
            'description': artwork.description,
            'price': artwork.price,
            'artist_id': artwork.artist_id
        }), 200
    return jsonify({'error': 'Artwork not found'}), 404

@app.route('/api/artworks', methods=['POST'])
def create_artwork():
    data = request.json
    new_artwork = Artwork(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        artist_id=data['artist_id']
    )
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({'id': new_artwork.id}), 201

@app.route('/api/artworks/<int:artwork_id>', methods=['PUT'])
def update_artwork(artwork_id):
    data = request.json
    artwork = Artwork.query.get(artwork_id)
    if artwork:
        artwork.title = data.get('title', artwork.title)
        artwork.description = data.get('description', artwork.description)
        artwork.price = data.get('price', artwork.price)
        db.session.commit()
        return jsonify({'id': artwork.id}), 200
    return jsonify({'error': 'Artwork not found'}), 404

@app.route('/api/artworks/<int:artwork_id>', methods=['DELETE'])
def delete_artwork(artwork_id):
    artwork = Artwork.query.get(artwork_id)
    if artwork:
        db.session.delete(artwork)
        db.session.commit()
        return jsonify({'message': 'Artwork deleted'}), 200
    return jsonify({'error': 'Artwork not found'}), 404

# Review Routes
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        'id': review.id,
        'content': review.content,
        'rating': review.rating,
        'user_id': review.user_id,
        'artwork_id': review.artwork_id
    } for review in reviews]), 200

@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)
    if review:
        return jsonify({
            'id': review.id,
            'content': review.content,
            'rating': review.rating,
            'user_id': review.user_id,
            'artwork_id': review.artwork_id
        }), 200
    return jsonify({'error': 'Review not found'}), 404

@app.route('/api/reviews', methods=['POST'])
def create_review():
    data = request.json
    new_review = Review(
        content=data['content'],
        rating=data['rating'],
        user_id=data['user_id'],
        artwork_id=data['artwork_id']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'id': new_review.id}), 201

@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.json
    review = Review.query.get(review_id)
    if review:
        review.content = data.get('content', review.content)
        review.rating = data.get('rating', review.rating)
        db.session.commit()
        return jsonify({'id': review.id}), 200
    return jsonify({'error': 'Review not found'}), 404

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted'}), 200
    return jsonify({'error': 'Review not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
