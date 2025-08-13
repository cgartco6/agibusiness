from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key_agi_business',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
            'mysql://user:password@localhost/agi_business',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='/var/www/uploads',
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {"origins": ["https://yourdomain.co.za"]}
    })

    # Register blueprints
    from .views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # CLI commands
    @app.cli.command('init-db')
    def init_db():
        """Initialize the database"""
        db.create_all()
        print('Database initialized')

    return app
