from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from app.models import User

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Use app context for database initialization and user creation
    with app.app_context():
        # Ensure the database tables are created
        db.create_all()

        # Create the default admin user if it doesn't exist
        try:
            if not User.query.filter_by(email="admin@local.domain").first():
                default_admin = User(
                    username="admin",
                    email="admin@local.domain",
                    password_hash=generate_password_hash("changeme"),
                    role="admin"
                )
                db.session.add(default_admin)
                db.session.commit()
                print("Default admin user created: admin@local.domain / changeme")
        except Exception as e:
            print(f"Error during default admin user creation: {e}")

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.compliance import compliance_bp
    from app.routes.audit import audit_bp
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(compliance_bp, url_prefix="/compliance")
    app.register_blueprint(audit_bp, url_prefix="/audit")
    app.register_blueprint(views_bp)

    return app
