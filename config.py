#ამის მიზანია Flask აპლიაკციის უსაფრთხოების key და
#მონაცემთა ბაზის მისამართის გაწერა

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'jobboard.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


