from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Import the blueprints
from app.routes.auth import auth_bp
from app.routes.compliance import compliance_bp
from app.routes.audit import audit_bp
from app.routes.views import views_bp

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

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(compliance_bp, url_prefix="/compliance")
    app.register_blueprint(audit_bp, url_prefix="/audit")
    app.register_blueprint(views_bp)  # No URL prefix for the root blueprint

    return app
