from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.menu_item import MenuItem
from app import db

menu_bp = Blueprint('menu', __name__)

#Admin-only: Create a new menu item
@menu_bp.route('/admin/menu', methods=['POST'])
@jwt_required()
def create_menu_item():

    data = request.get_json()

    required_fields = ['name', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_item = MenuItem(
        name=data['name'],
        description=data.get('description', ''),
        price=float(data['price']),
        is_available=data.get('is_available', True),
        image_url=data.get('image_url', None)
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201


#Public: Get all available menu items
@menu_bp.route('/menu', methods=['GET'])
def get_public_menu():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([item.to_dict() for item in items]), 200


#Admin-only: Get all menu items (including unavailable)
@menu_bp.route('/admin/menu', methods=['GET'])
@jwt_required()
def get_all_menu_items():
    items = MenuItem.query.all()
    return jsonify([item.to_dict() for item in items]), 200


#Admin-only: Update a menu item
@menu_bp.route('/admin/menu/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    data = request.get_json()

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.price = float(data['price']) if 'price' in data else item.price
    item.is_available = data.get('is_available', item.is_available)
    item.image_url = data.get('image_url', item.image_url)

    db.session.commit()
    return jsonify(item.to_dict()), 200


#Admin-only: Delete a menu item
@menu_bp.route('/admin/menu/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Menu item deleted"}), 200