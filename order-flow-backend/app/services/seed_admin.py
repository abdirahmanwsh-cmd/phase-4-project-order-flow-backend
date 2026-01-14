from app import db
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash

def seed_admin():
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session.add(admin_role)
        db.session.commit()

    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            password=generate_password_hash("admin123"),
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()
    print("Admin seeding complete")
