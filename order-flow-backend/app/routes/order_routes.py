from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order
from app.models.user import User
from app.utils.order_status import OrderStatus, can_transition, ORDER_TRANSITIONS

order_bp = Blueprint('order', __name__)

#Customer: Get their own orders
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    current_user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200


#Admin: Get all orders
@order_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200


#Admin: Update order status
@order_bp.route('/admin/orders/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(order_id):
    
    order = Order.query.get_or_404(order_id)
    data = request.get_json()

    if 'status' not in data:
        return jsonify({"error": "Missing 'status' field"}), 400

    new_status_str = data['status']
    try:
        new_status = OrderStatus(new_status_str)
    except ValueError:
        return jsonify({"error": f"Invalid status. Allowed: {[s.value for s in OrderStatus]}"}), 400

    current_status = OrderStatus(order.status)

    if not can_transition(current_status, new_status):
        return jsonify({
            "error": f"Invalid transition from '{current_status.value}' to '{new_status.value}'",
            "allowed_transitions": [s.value for s in ORDER_TRANSITIONS[current_status]]
        }), 400

    order.status = new_status.value
    db.session.commit()

    return jsonify(order.to_dict()), 200
