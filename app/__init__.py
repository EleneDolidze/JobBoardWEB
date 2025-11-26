from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import routes, models
#პლიკაციის შექმნა
app = Flask(__name__)
app.config.from_object('config.Config')  # შენს config ფაილიდან პარამეტრები

#DB ინიციალიზაცია
db = SQLAlchemy(app)

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


