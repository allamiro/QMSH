from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from app.models import User, db

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import models after app and db are initialized
    with app.app_context():
        from app import models

        # Create the default admin user if it doesn't exist
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
