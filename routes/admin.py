from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    users = User.query.all()
    return render_template("admin.html", users=users)
