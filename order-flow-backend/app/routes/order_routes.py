from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order
from app.models.order_item import OrderItem

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - phone
            - email
            - address
            - total
            - items
          properties:
            customer_name:
              type: string
              example: John Doe
            phone:
              type: string
              example: 0712345678
            email:
              type: string
              example: john@example.com
            address:
              type: string
              example: 123 Main St
            city:
              type: string
              example: Nairobi
            total:
              type: number
              example: 150.50
            items:
              type: array
              items:
                type: object
                properties:
                  menu_item_id:
                    type: integer
                  quantity:
                    type: integer
                  price:
                    type: number
    responses:
      201:
        description: Order created successfully
      400:
        description: Missing required fields
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        print(f"Received order data: {data}")  # Debug logging
        
        # Support both frontend field names and backend field names
        address = data.get('address') or data.get('delivery_address', '')
        city = data.get('city', 'N/A')  # Default city if not provided
        total = data.get('total') or data.get('total_amount')
        
        if not data or not all([data.get('customer_name'), data.get('phone'), data.get('email'), address, total, data.get('items')]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_order = Order(
            customer_name=data['customer_name'],
            phone=data['phone'],
            email=data['email'],
            address=address,
            city=city,
            total=total,
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
    """
    Get order by ID
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: Order ID
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
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
    """
    Get all orders
    ---
    tags:
      - Orders
    responses:
      200:
        description: List of all orders
        schema:
          properties:
            orders:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  customer_name:
                    type: string
                  total:
                    type: number
                  status:
                    type: string
                  created_at:
                    type: string
    """
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        orders_list = [{'id': o.id, 'customer_name': o.customer_name, 'total': o.total, 'status': o.status, 'created_at': o.created_at.isoformat() if o.created_at else None} for o in orders]
        return jsonify({'orders': orders_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@order_bp.route('/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """
    Update order status
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: Order ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum: [pending, processing, completed, cancelled]
              example: completed
    responses:
      200:
        description: Status updated successfully
      400:
        description: Status is required
      404:
        description: Order not found
    """
    try:
        data = request.get_json()
        new_status = data.get("status")

        if not new_status:
            return jsonify({"error": "Status is required"}), 400

        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        order.status = new_status
        db.session.commit()

        return jsonify({"message": "Status updated", "order": order.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
