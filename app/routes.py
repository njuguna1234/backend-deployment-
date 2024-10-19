from flask import Blueprint, jsonify, request
from .models import User, Artwork, Review, db

main = Blueprint('main', __name__)

@main.route('/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    return jsonify([{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist': artwork.artist.name
    } for artwork in artworks])

@main.route('/artworks', methods=['POST'])
def create_artwork():
    data = request.get_json()
    new_artwork = Artwork(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        artist_id=data['artist_id']
    )
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork created successfully!'}), 201

@main.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    new_review = Review(
        content=data['content'],
        rating=data['rating'],
        user_id=data['user_id'],
        artwork_id=data['artwork_id']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully!'}), 201
