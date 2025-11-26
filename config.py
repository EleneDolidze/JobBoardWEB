#ამის მიზანია Flask აპლიაკციის უსაფრთხოების key და
#მონაცემთა ბაზის მისამართის გაწერა

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "mysecretkey"

    #ეს ქმნის SQLITE მონაცემთა ბაზას - jobboard.db დირექტორიაში
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'jobboard.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
