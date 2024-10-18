import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///art_gallery.db'  # Switch to PostgreSQL in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')
