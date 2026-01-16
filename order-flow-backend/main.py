from app import create_app, db
from app.services.seed_admin import seed_admin

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # Create all tables
        seed_admin()      # Seed admin user
    app.run(debug=True, port=5555)
