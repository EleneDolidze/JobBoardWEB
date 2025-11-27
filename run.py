#Flask აპლიკაციის გამშვები ფაილიfrom app import create_app
from app import create_app

app = create_app()

print("Created app:", app)

if __name__ == "__main__":
    print("RUN BLOCK ENTERED")
    app.run(debug=True, port=5000)








