from flask import Blueprint, render_template
from app.models import ComplianceStandard

compliance_bp = Blueprint("compliance", __name__)

@compliance_bp.route("/dashboard")
def dashboard():
    standards = ComplianceStandard.query.all()
    return render_template("compliance/dashboard.html", standards=standards)

@compliance_bp.route("/track/<int:id>")
def track_compliance(id):
    standard = ComplianceStandard.query.get_or_404(id)
    return render_template("compliance/track.html", standard=standard)
