from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "trek-secret-2024"

# Initialize Database
db.init_app(app)


def seed_admin():
    """Create default admin if not exists"""

    if not User.query.filter_by(role="admin").first():

        admin = User(
            username="admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            full_name="Site Admin",
            role="admin",
            status="active",
            is_approved=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")


with app.app_context():
    db.create_all()
    seed_admin()


@app.route("/")
def home():
    return "TrailSync Database Setup Complete!"


if __name__ == "__main__":
    app.run(debug=True)
