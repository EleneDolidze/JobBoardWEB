#მიზანია მომხმარებლისა და მის მიერ შექმნილი ყველა ვაკანსიის ამოღება ბაზიდან
from app import app, db
from app.models import User, Job

with app.app_context():
    user = User.query.first()
    print(user.id, user.name)

    jobs = Job.query.filter_by(user_id=user.id).all()
    print(jobs)



