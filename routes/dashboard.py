from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from extensions import db
from models.transaction import Transaction
from models.budget import Budget

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def overview():
    # Monthly totals
    month_label = func.date_format(Transaction.date, "%Y-%m")
    monthly_rows = (
        db.session.query(month_label.label("month"),
                         func.sum(Transaction.amount).label("total"))
        .filter(Transaction.user_id == current_user.id)
        .group_by(month_label)
        .all()
    )
    # Convert to list of dicts
    monthly = [{"month": row.month, "total": float(row.total)} for row in monthly_rows]

    # Top expense categories
    top_cats_rows = (
        db.session.query(Transaction.category,
                         func.sum(Transaction.amount).label("total"))
        .filter(Transaction.user_id == current_user.id,
                Transaction.type == "expense")
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(5)
        .all()
    )
    top_categories = [{"category": row.category, "total": float(row.total)} for row in top_cats_rows]

    # Budgets for current user
    budgets = Budget.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard.html",
        monthly=monthly,
        top_categories=top_categories,
        budgets=budgets,
    )
