from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flasgger import Swagger
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
bcrypt = Bcrypt()

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
    
    # Configure Swagger UI
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/api/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/api/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Order Flow API",
            "description": "API documentation for Order Flow Restaurant Management System",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Configure CORS for all environments
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",                    # local dev (Vite default port)
                "http://localhost:3000",                    # if using Create React App
                "https://order-flow-frontend.web.app",      # main Firebase domain
                "https://order-flow-frontend.firebaseapp.com",  # secondary Firebase domain
                "https://*.onrender.com"                    # Render deployments (wildcard)
            ],
            "supports_credentials": True,                   # important for cookies/auth headers
            "allow_headers": ["Content-Type", "Authorization"]  # allow JWT header
        }
    })
    
    # Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.menu_routes import menu_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(payment_bp, url_prefix="/api")
    app.register_blueprint(menu_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
