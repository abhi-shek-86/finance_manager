from flask import Flask, redirect, url_for, flash, request, jsonify
from config import Config
from extensions import db, login_manager
from models.user import User
from werkzeug.security import generate_password_hash

login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.transaction import transactions_bp
    from routes.dashboard import dashboard_bp
    from routes.budget import budget_bp
    from routes.export import export_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(dashboard_bp,   url_prefix="/dashboard")
    app.register_blueprint(budget_bp,      url_prefix="/budget")
    app.register_blueprint(export_bp,      url_prefix="/export")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create DB tables
    with app.app_context():
        from models import User, Transaction, Budget
        db.create_all()

        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),  # Default password
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    return app

app = create_app()

@login_manager.unauthorized_handler
def unauthorized_callback():
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({"error": "Login required"}), 401
    flash("Please login first!", "login_required")
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
