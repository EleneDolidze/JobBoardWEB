#მიზანია მომხმარებლისა და მის მიერ შექმნილი ყველა ვაკანსიის ამოღება ბაზიდან

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created!")



