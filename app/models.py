from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):   #ამოწმებს უზერს მონაცემთა ბაზიდან
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(100), default='default.jpg')
    jobs = db.relationship('Job', backref='author', lazy=True)

    #პაროლების უსაფრთხოება
    def set_password(self, password):  #პაროლის მიღება და ჰეშირება
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  #ამოწმებს ემთხვევა თუ არა შეყვანილი პაროლი ამ უზერის ჰეშს
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(200), nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    category = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

