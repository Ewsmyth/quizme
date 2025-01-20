import time
from flask import Flask
from . import config
from .models import db, User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .utils import create_roles, create_admin_user

csrf = CSRFProtect()  # Initialize CSRF protection
limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])  # Initialize rate limiter

def create_app():
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object(config)

    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize rate limiter
    limiter.init_app(app)

    # Initialize database
    db.init_app(app)

    # Setup Flask-Login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.auth_login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Import and register blueprints
    from .auth import auth
    from .user import user
    from .admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    # Wait for the database to be ready
    with app.app_context():
        for _ in range(10):  # Retry 10 times
            try:
                print("Attempting to initialize the database...")
                db.create_all()  # Initialize database tables
                create_roles()
                create_admin_user()
                print("Database initialization complete.")
                break
            except Exception as e:
                print(f"Database not ready. Retrying in 5 seconds... ({e})")
                time.sleep(5)
        else:
            print("Failed to initialize the database after 10 attempts.")

    return app
