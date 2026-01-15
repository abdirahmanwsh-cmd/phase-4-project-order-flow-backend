from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order
from app.models.order_item import OrderItem

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['customer_name', 'phone', 'email', 'address', 'city', 'total', 'items']):
            return jsonify({'error': 'Missing fields'}), 400
        
        new_order = Order(
            customer_name=data['customer_name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address'],
            city=data['city'],
            total=data['total'],
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()
        
        for item in data['items']:
            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item['menu_item_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        return jsonify({'order_id': new_order.id, 'status': new_order.status, 'total': new_order.total, 'order': new_order.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_data = {'id': order.id, 'customer_name': order.customer_name, 'items': []}
        for item in order.order_items:
            order_data['items'].append({'name': item.menu_item.name if item.menu_item else 'Unknown', 'quantity': item.quantity, 'price': item.price})
        return jsonify(order_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        orders_list = [{'id': o.id, 'customer_name': o.customer_name, 'total': o.total, 'status': o.status, 'created_at': o.created_at.isoformat() if o.created_at else None} for o in orders]
        return jsonify({'orders': orders_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500