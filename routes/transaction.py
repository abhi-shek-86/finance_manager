from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from extensions import db
from models.transaction import Transaction

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template("transactions.html", transactions=transactions)

@transactions_bp.route("/add", methods=["POST"])
@login_required
def add_transaction():
    amount = request.form["amount"]
    category = request.form["category"]
    type_ = request.form["type"]
    date = request.form["date"]
    description = request.form["description"]

    txn = Transaction(
        amount=amount,
        category=category,
        type=type_,
        date=date,
        description=description,
        user_id=current_user.id,
    )
    db.session.add(txn)
    db.session.commit()
    flash("Transaction added", "success")
    return redirect("/transactions")

@transactions_bp.route("/delete/<int:id>")
@login_required
def delete_transaction(id):
    txn = Transaction.query.get_or_404(id)
    if txn.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect("/transactions")
    db.session.delete(txn)
    db.session.commit()
    flash("Deleted", "success")
    return redirect("/transactions")
