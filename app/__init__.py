from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#DB და LoginManager ჯერ ინიციალიზებულია, მაგრამ არა app-სთან დაკავშირებული
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    #DB და LoginManager დაკავშირება app–თან
    db.init_app(app)
    login_manager.init_app(app)

    #Routes აქ უნდა გამოიძახო, Blueprint–ს გამოყენებით
    from app.routes import main
    app.register_blueprint(main)

    return app



