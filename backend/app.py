from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "trekking-management-app-secret-key-for-jwt-2026"

db.init_app(app)
JWTManager(app)

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from routes.user_routes import user_bp
from routes.booking_routes import booking_bp
from routes.job_routes import job_bp
from routes.public_routes import public_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(job_bp)
app.register_blueprint(public_bp)
# (more blueprints are registered here in the next milestones)


def create_database():
    """Create all tables and the single Admin user (done in code, no manual DB creation)."""
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin = User(
                name="Admin",
                email="admin@trek.com",
                password_hash=generate_password_hash("admin123"),
                role="admin",
                phone="9999999999",
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created -> admin@trek.com / admin123")


create_database()


@app.route("/")
def home():
    return "Trekking Management App backend is running"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
