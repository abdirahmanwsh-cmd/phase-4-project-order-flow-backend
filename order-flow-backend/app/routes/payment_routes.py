from flask import Blueprint, request, jsonify
from app.services.mpesa_service import MPesaService
from app.models.order import Order
from app import db

payment_bp = Blueprint('payment', __name__)
mpesa = MPesaService()

@payment_bp.route('/payments/mpesa/initiate', methods=['POST'])
def initiate_mpesa_payment():
    """
    Initiate M-Pesa STK Push payment
    
    Request body:
    {
        "order_id": 1,
        "phone_number": "0712345678"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('order_id') or not data.get('phone_number'):
            return jsonify({'error': 'order_id and phone_number required'}), 400
        
        # Get order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Initiate STK push
        response = mpesa.stk_push(
            phone_number=data['phone_number'],
            amount=order.total,
            account_reference=f"Order{order.id}",
            transaction_desc=f"Payment for Order {order.id}"
        )
        
        print(f"M-Pesa Response: {response}")  # Debug logging
        
        # Return the full response with CheckoutRequestID
        return jsonify({
            'message': 'STK push sent',
            'CheckoutRequestID': response.get('CheckoutRequestID'),
            'MerchantRequestID': response.get('MerchantRequestID'),
            'ResponseCode': response.get('ResponseCode'),
            'ResponseDescription': response.get('ResponseDescription'),
            'CustomerMessage': response.get('CustomerMessage'),
            'mpesa_response': response
        }), 200
        
    except Exception as e:
        print(f"M-Pesa Error: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payments/status/<checkout_request_id>', methods=['GET'])
def check_payment_status(checkout_request_id):
    """
    Check M-Pesa payment status
    
    For sandbox: Returns mock status
    For production: Query Daraja API
    """
    try:
        # In sandbox mode, we can't query transaction status reliably
        # Return a mock response for testing
        return jsonify({
            'checkout_request_id': checkout_request_id,
            'status': 'pending',
            'message': 'Payment status check - use callback for real status'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """
    M-Pesa callback endpoint
    Safaricom sends payment result here
    """
    try:
        data = request.get_json()
        
        # Log callback data (for debugging)
        print("M-Pesa Callback:", data)
        
        # Process callback result
        # Extract result code and update order status
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        
        if result_code == 0:
            # Payment successful
            return jsonify({'message': 'Payment received'}), 200
        else:
            # Payment failed
            return jsonify({'message': 'Payment failed'}), 200
            
    except Exception as e:
        print("Callback error:", str(e))
        return jsonify({'error': str(e)}), 500
