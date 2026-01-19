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
            account_reference=f"ORD{order.id}",
            transaction_desc=f"Order{order.id}"
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
    Query M-Pesa payment status
    
    Returns the status of a payment transaction
    """
    try:
        # Query M-Pesa for transaction status
        result = mpesa.query_stk_status(checkout_request_id)
        
        print(f"M-Pesa Status Query Result: {result}")  # Debug logging
        
        # Parse the response
        result_code = result.get('ResultCode')
        result_desc = result.get('ResultDesc', '')
        
        # Determine status
        if result_code == '0':
            status = 'completed'
            message = 'Payment successful'
        elif result_code == '1032':
            status = 'cancelled'
            message = 'Payment cancelled by user'
        elif result_code == '1':
            status = 'failed'
            message = 'Payment failed'
        elif result_code == '1037':
            status = 'timeout'
            message = 'Payment timeout'
        else:
            status = 'pending'
            message = result_desc or 'Payment processing'
        
        return jsonify({
            'checkout_request_id': checkout_request_id,
            'status': status,
            'result_code': result_code,
            'message': message,
            'mpesa_response': result
        }), 200
        
    except Exception as e:
        print(f"Status Query Error: {str(e)}")  # Debug logging
        # If query fails, assume still pending
        return jsonify({
            'checkout_request_id': checkout_request_id,
            'status': 'pending',
            'message': 'Unable to verify status, payment may still be processing',
            'error': str(e)
        }), 200


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
