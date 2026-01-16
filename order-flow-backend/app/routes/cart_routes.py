from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import Cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Order Flow API - ', 'endpoints': {'/api/cart': 'Cart API', '/api/orders': 'Orders API'}}), 200

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    try:
        cart_items = Cart.query.all()
        return jsonify({'cart_items': [item.to_dict() for item in cart_items]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        if not data or not data.get('menu_item_id'):
            return jsonify({'error': 'menu_item_id required'}), 400
        
        cart_item = Cart(
            user_id=1,
            menu_item_id=data['menu_item_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added', 'cart_item': cart_item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):
    try:
        cart_item = Cart.query.get(id)
        if not cart_item:
            return jsonify({'error': 'Not found'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Removed'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500