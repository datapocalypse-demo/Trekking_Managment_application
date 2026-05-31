from flask import Flask
from flask_login import LoginManager
from models import db, User
from werkzeug.security import generate_password_hash
import os

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "trek-secret-2024")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Init extensions ───────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)

    # ── Create tables & seed admin ────────────────────────
    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    if not User.query.filter_by(role="admin").first():
        admin = User(
            username="admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            full_name="Site Admin",
            role="admin",
            status="active",
            is_approved=True,
        )
        db.session.add(admin)
        db.session.commit()
        print("[SEED] Admin created → admin@trek.com / admin123")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
