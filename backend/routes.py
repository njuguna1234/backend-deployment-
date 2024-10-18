from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, jwt_refresh_token_required
from models import User, Artwork, Review, Purchase, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

# User Registration
@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    is_artist = data.get('is_artist', False)

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists."}), 400

    # Create a new user
    new_user = User(name=name, email=email, password=password, is_artist=is_artist)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully."}), 201

# User Login
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={"id": user.id, "is_artist": user.is_artist})
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password."}), 401

# Get all Artworks
@routes.route('/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    return jsonify([artwork.to_dict() for artwork in artworks]), 200

# Add Artwork
@routes.route('/artworks', methods=['POST'])
@jwt_required()
def add_artwork():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')

    current_user = get_jwt_identity()
    artist_id = current_user['id']

    new_artwork = Artwork(title=title, description=description, price=price, artist_id=artist_id)
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({"msg": "Artwork added successfully."}), 201

# Update Artwork
@routes.route('/artworks/<int:artwork_id>', methods=['PUT'])
@jwt_required()
def update_artwork(artwork_id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(artwork_id)

    # Ensure the current user is the artist of the artwork
    current_user = get_jwt_identity()
    if artwork.artist_id != current_user['id']:
        return jsonify({"msg": "You are not authorized to update this artwork."}), 403

    artwork.title = data.get('title', artwork.title)
    artwork.description = data.get('description', artwork.description)
    artwork.price = data.get('price', artwork.price)
    db.session.commit()
    return jsonify({"msg": "Artwork updated successfully."}), 200

# Delete Artwork
@routes.route('/artworks/<int:artwork_id>', methods=['DELETE'])
@jwt_required()
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)

    # Ensure the current user is the artist of the artwork
    current_user = get_jwt_identity()
    if artwork.artist_id != current_user['id']:
        return jsonify({"msg": "You are not authorized to delete this artwork."}), 403

    db.session.delete(artwork)
    db.session.commit()
    return jsonify({"msg": "Artwork deleted successfully."}), 200

# Add Review
@routes.route('/artworks/<int:artwork_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(artwork_id):
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')

    current_user = get_jwt_identity()
    user_id = current_user['id']

    new_review = Review(content=content, rating=rating, user_id=user_id, artwork_id=artwork_id)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"msg": "Review added successfully."}), 201

# Get Reviews for an Artwork
@routes.route('/artworks/<int:artwork_id>/reviews', methods=['GET'])
def get_reviews(artwork_id):
    reviews = Review.query.filter_by(artwork_id=artwork_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Purchase Artwork
@routes.route('/artworks/<int:artwork_id>/purchase', methods=['POST'])
@jwt_required()
def purchase_artwork(artwork_id):
    current_user = get_jwt_identity()
    user_id = current_user['id']

    new_purchase = Purchase(user_id=user_id, artwork_id=artwork_id, purchase_date=datetime.utcnow())
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({"msg": "Artwork purchased successfully."}), 201
