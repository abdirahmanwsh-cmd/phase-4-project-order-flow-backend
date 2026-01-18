from app import create_app, db
from seed_menu import seed_menu

app = create_app()
with app.app_context():
    db.create_all()
    seed_menu()
    print("Menu seeded successfully!")