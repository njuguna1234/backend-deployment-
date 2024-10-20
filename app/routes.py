from flask import Blueprint, request, jsonify
from .models import User, Artwork, Review, Purchase, db

main = Blueprint('main', __name__)

# --- Users ---
@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=data['password'], is_artist=data.get('is_artist', False))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# --- Artworks ---
@main.route('/api/artworks', methods=['POST'])
def create_artwork():
    data = request.get_json()
    artist = User.query.get(data['artist_id'])
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    new_artwork = Artwork(title=data['title'], description=data['description'], price=data['price'], artist=artist)
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork created'}), 201

# --- Reviews ---
@main.route('/api/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    artwork = Artwork.query.get(data['artwork_id'])
    if not user or not artwork:
        return jsonify({'error': 'User or Artwork not found'}), 404
    new_review = Review(content=data['content'], rating=data['rating'], user=user, artwork=artwork)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created'}), 201

# --- Purchases ---
@main.route('/api/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    artwork = Artwork.query.get(data['artwork_id'])
    if not user or not artwork:
        return jsonify({'error': 'User or Artwork not found'}), 404
    new_purchase = Purchase(user=user, artwork=artwork)
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({'message': 'Purchase created'}), 201
