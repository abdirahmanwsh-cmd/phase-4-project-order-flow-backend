from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from app import db, bcrypt
from app.models.user import User
from app.models.role import Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test", methods=["GET"])
def auth_test():
    """
    Test endpoint for auth routes
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Auth routes are working
        schema:
          properties:
            message:
              type: string
              example: Auth routes working
    """
    return jsonify({"message": "Auth routes working"})

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: SecurePass123!
    responses:
      201:
        description: User registered successfully
        schema:
          properties:
            msg:
              type: string
              example: User registered successfully
      400:
        description: Missing required fields
      409:
        description: Email or username already exists
      500:
        description: Registration failed
    """
    data = request.get_json()
    
    required_fields = ["username", "email", "password"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields (username, email, password)"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email already registered"}), 409
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username already taken"}), 409
    
    new_user = User(
        username=data["username"],
        email=data["email"]
    )
    new_user.set_password(data["password"])
    
    customer_role = Role.query.filter_by(name="customer").first()
    if not customer_role:
        customer_role = Role(name="customer")
        db.session.add(customer_role)
        db.session.commit()
    
    new_user.roles.append(customer_role)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login with email and password
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: SecurePass123!
    responses:
      200:
        description: Login successful
        schema:
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
                roles:
                  type: array
                  items:
                    type: string
      400:
        description: Missing email or password
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    
    if not data or "email" not in data or "password" not in data:
        return jsonify({"msg": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    
    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Invalid email or password"}), 401
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"roles": [role.name for role in user.roles]}
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "roles": [role.name for role in user.roles]
        }
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        schema:
          type: string
          example: Bearer <refresh_token>
        description: Refresh token in Bearer format
    responses:
      200:
        description: New access token generated
        schema:
          properties:
            access_token:
              type: string
      404:
        description: User not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    new_access_token = create_access_token(
        identity=user.id,
        additional_claims={"roles": [role.name for role in user.roles]}
    )
    
    return jsonify({"access_token": new_access_token}), 200