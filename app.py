from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models import User, Artwork, Review, Purchase

# Initialize Flask app
app = Flask(__name__)

# Configuration for database and JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_gallery.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Routes

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'email', 'password', 'is_artist')):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], password=hashed_password, is_artist=data['is_artist'])
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


# Artwork CRUD operations
@app.route('/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    return jsonify([{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist': artwork.artist.name
    } for artwork in artworks]), 200

@app.route('/artworks', methods=['POST'])
@jwt_required()
def create_artwork():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_artist:
        return jsonify({'error': 'Only artists can create artwork'}), 403
    
    data = request.get_json()
    if not data or not all(key in data for key in ('title', 'description', 'price')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    artwork = Artwork(
        title=data['title'],
        description=data.get('description'),
        price=data['price'],
        artist_id=user.id
    )
    
    try:
        db.session.add(artwork)
        db.session.commit()
        return jsonify({'message': 'Artwork created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific artwork by ID
@app.route('/artworks/<int:id>', methods=['GET'])
def get_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    return jsonify({
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist': artwork.artist.name
    }), 200

# Update an artwork (restricted to the artist who owns it)
@app.route('/artworks/<int:id>', methods=['PUT'])
@jwt_required()
def update_artwork(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    artwork = Artwork.query.get_or_404(id)
    
    if artwork.artist_id != user.id:
        return jsonify({'error': 'You do not have permission to edit this artwork'}), 403

    data = request.get_json()
    artwork.title = data.get('title', artwork.title)
    artwork.description = data.get('description', artwork.description)
    artwork.price = data.get('price', artwork.price)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Artwork updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete an artwork (restricted to the artist who owns it)
@app.route('/artworks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_artwork(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    artwork = Artwork.query.get_or_404(id)
    
    if artwork.artist_id != user.id:
        return jsonify({'error': 'You do not have permission to delete this artwork'}), 403

    try:
        db.session.delete(artwork)
        db.session.commit()
        return jsonify({'message': 'Artwork deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Purchase an artwork
@app.route('/purchase', methods=['POST'])
@jwt_required()
def purchase_artwork():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    data = request.get_json()
    artwork = Artwork.query.get_or_404(data['artwork_id'])
    
    if artwork.price > data.get('amount'):
        return jsonify({'error': 'Insufficient payment'}), 400
    
    purchase = Purchase(user_id=user.id, artwork_id=artwork.id)
    
    try:
        db.session.add(purchase)
        db.session.commit()
        return jsonify({'message': 'Artwork purchased successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
