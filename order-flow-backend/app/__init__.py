from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800 

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        db.create_all()

    return app