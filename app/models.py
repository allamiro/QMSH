from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class ComplianceStandard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_compliant = db.Column(db.Boolean, default=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    findings = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    corrective_action = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
