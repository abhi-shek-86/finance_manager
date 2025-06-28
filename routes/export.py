import pandas as pd
from io import BytesIO
from flask import Blueprint, send_file, render_template
from flask_login import login_required, current_user
from models.transaction import Transaction
from utils.pdf import to_pdf   # helper (in utils/pdf.py)
import flask

export_bp = Blueprint("export", __name__)

@export_bp.route("/csv")
@login_required
def export_csv():
    txns = Transaction.query.filter_by(user_id=current_user.id).all()
    df = pd.DataFrame([{
        "Date":        t.date,
        "Category":    t.category,
        "Amount":      t.amount,
        "Type":        t.type,
        "Description": t.description or ""
    } for t in txns])

    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(buf,
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="transactions.csv")

@export_bp.route("/pdf")
@login_required
def export_pdf():
    txns = Transaction.query.filter_by(user_id=current_user.id).all()
    html = render_template("export.html", transactions=txns)
    pdf_bytes = to_pdf(html)
    return send_file(BytesIO(pdf_bytes),
                     mimetype="application/pdf",
                     as_attachment=True,
                     download_name="transactions.pdf")

@export_bp.route("/download")
@login_required
def export_download():
    fmt = (flask.request.args.get("format") or "csv").lower()
    if fmt == "pdf":
        return export_pdf()
    else:
        return export_csv()
