from flask import Blueprint, render_template, request
from app.models import AuditLog, db

audit_bp = Blueprint("audit", __name__)

@audit_bp.route("/")
def audits():
    logs = AuditLog.query.all()
    return render_template("audit/audits.html", logs=logs)

@audit_bp.route("/create", methods=["GET", "POST"])
def create_audit():
    if request.method == "POST":
        section = request.form["section"]
        findings = request.form["findings"]
        status = request.form["status"]

        new_audit = AuditLog(section=section, findings=findings, status=status)
        db.session.add(new_audit)
        db.session.commit()
        return redirect("/audit")
    return render_template("audit/create.html")
