from app.models import User
from app import db, bcrypt

def seed_admin():
    if not User.query.filter_by(username="admin").first():
        hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin = User(username="admin", email="admin@orderflow.com", password=hashed_password, role="admin")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin already exists")
