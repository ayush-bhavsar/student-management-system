from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes.auth import auth_bp
from routes.students import students_bp
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "students.db")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///" + DATABASE_PATH
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    os.makedirs(DATABASE_DIR, exist_ok=True)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
