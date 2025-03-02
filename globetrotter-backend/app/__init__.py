from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    from app.routes import routes
    app.register_blueprint(routes)

    # with app.app_context():
    #     db.create_all()  # Ensure tables exist
    #     from app.utils import populate_database
    #     populate_database()  # Auto-seed database

    return app
