from flask import Blueprint, request, redirect, flash, render_template
from flask_login import login_required, current_user
from extensions import db
from models.budget import Budget

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/set", methods=["POST"])
@login_required
def set_budget():
    month = request.form["month"]          # YYYY-MM
    amount = float(request.form["amount"])

    record = Budget.query.filter_by(user_id=current_user.id, month=month).first()
    if record:          # Update
        record.amount = amount
    else:               # Insert
        record = Budget(user_id=current_user.id, month=month, amount=amount)
        db.session.add(record)

    db.session.commit()
    flash("Budget saved", "success")
    return redirect("/dashboard")

@budget_bp.route("/", methods=["GET"])
@login_required
def budget_page():
    return render_template("budget.html")
