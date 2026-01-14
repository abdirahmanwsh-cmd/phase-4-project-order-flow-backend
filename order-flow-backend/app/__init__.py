from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    db.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
