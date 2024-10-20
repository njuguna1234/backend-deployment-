from app import app
from models import db, User, Artwork, Review, Purchase
from werkzeug.security import generate_password_hash
import random

# Sample data
def seed_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create some users
        users = [
            User(username='artist1', email='artist1@example.com', password=generate_password_hash('password1')),
            User(username='artist2', email='artist2@example.com', password=generate_password_hash('password2')),
            User(username='buyer1', email='buyer1@example.com', password=generate_password_hash('password3')),
            User(username='buyer2', email='buyer2@example.com', password=generate_password_hash('password4'))
        ]

        # Add users to session
        db.session.add_all(users)
        db.session.commit()

        # Create some artworks (assuming the artist is just a user in this case)
        artworks = [
            Artwork(title='Sunset Landscape', description='A beautiful sunset', price=200.00, artist_id=1),
            Artwork(title='Abstract Colors', description='A modern abstract painting', price=350.00, artist_id=1),
            Artwork(title='Portrait of a Woman', description='An oil portrait', price=500.00, artist_id=2),
            Artwork(title='Cityscape', description='A vibrant city skyline', price=275.00, artist_id=2)
        ]

        # Add artworks to session
        db.session.add_all(artworks)
        db.session.commit()

        # Create some reviews
        reviews = [
            Review(content='Amazing artwork! Looks even better in person.', rating=5, user_id=3, artwork_id=1),
            Review(content='Great colors, but I expected a larger canvas.', rating=4, user_id=3, artwork_id=2),
            Review(content='Love it! Perfect addition to my living room.', rating=5, user_id=4, artwork_id=3),
            Review(content='The detail in this piece is incredible.', rating=5, user_id=4, artwork_id=4)
        ]

        # Add reviews to session
        db.session.add_all(reviews)
        db.session.commit()

        # Create some purchases
        purchases = [
            Purchase(user_id=3, artwork_id=1),
            Purchase(user_id=3, artwork_id=2),
            Purchase(user_id=4, artwork_id=3),
            Purchase(user_id=4, artwork_id=4)
        ]

        # Add purchases to session
        db.session.add_all(purchases)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
