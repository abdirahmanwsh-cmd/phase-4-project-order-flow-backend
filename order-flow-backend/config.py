import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    BASE_DIR, "instance", "orderflow.db"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev-secret-key"
JWT_SECRET_KEY = "jwt-secret-key"
