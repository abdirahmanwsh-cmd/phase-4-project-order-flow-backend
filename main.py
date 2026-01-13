from app import create_app, db
from app.services import seed_admin

app = create_app()

with app.app_context():
    db.create_all()       # create database tables
    seed_admin()          # seed admin user

if __name__ == "__main__":
    app.run(debug=True)
