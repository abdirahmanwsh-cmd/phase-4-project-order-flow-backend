from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import Cart
from app.models.menu_item import MenuItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Order Flow API', 'endpoints': {'/api/menu': 'Menu API', '/api/cart': 'Cart API', '/api/orders': 'Orders API', '/api/payments/mpesa/initiate': 'M-Pesa Payment'}}), 200

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    """
    Get all cart items
    ---
    tags:
      - Cart
    responses:
      200:
        description: List of cart items
        schema:
          properties:
            cart_items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  menu_item_id:
                    type: integer
                  menu_item_name:
                    type: string
                  menu_item_price:
                    type: number
                  quantity:
                    type: integer
    """
    try:
        cart_items = Cart.query.all()
        return jsonify({'cart_items': [item.to_dict() for item in cart_items]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    """
    Add item to cart
    ---
    tags:
      - Cart
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - menu_item_id
          properties:
            menu_item_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 2
    responses:
      201:
        description: Item added to cart
      400:
        description: Invalid request
      404:
        description: Menu item not found
    """
    try:
        data = request.get_json()
        if not data or not data.get('menu_item_id'):
            return jsonify({'error': 'menu_item_id required'}), 400
        
        # Validate menu item exists and is available
        menu_item = MenuItem.query.filter_by(
            id=data['menu_item_id'],
            is_available=True
        ).first()
        if not menu_item:
            return jsonify({'error': 'Item not found or unavailable'}), 404

        #REQUIRED: Handle quantity safely (ensure >= 1)
        quantity = data.get('quantity', 1)
        if not isinstance(quantity, int) or quantity < 1:
            return jsonify({'error': 'Quantity must be a positive integer'}), 400

        #Create cart item with snapshot fields (required by updated Cart model)
        cart_item = Cart(
            user_id=1,  #still hardcoded; replace later with auth
            menu_item_id=menu_item.id,
            quantity=quantity,
            menu_item_name=menu_item.name,
            menu_item_price=float(menu_item.price)
        )
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added', 'cart_item': cart_item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):
    """
    Remove item from cart
    ---
    tags:
      - Cart
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: Cart item ID
    responses:
      200:
        description: Item removed from cart
      404:
        description: Cart item not found
    """
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