from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Assuming you have a config.py file

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register your blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
