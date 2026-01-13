from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Order Flow API is running"})
