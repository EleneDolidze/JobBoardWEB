from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    print("A: Starting create_app")
    app = Flask(__name__)
    print("B: App created")

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    print("C: Extensions initialized")

    from .routes import bp as main_bp
    print("D: Routes imported")

    app.register_blueprint(main_bp)
    print("E: Blueprint registered")

    return app







