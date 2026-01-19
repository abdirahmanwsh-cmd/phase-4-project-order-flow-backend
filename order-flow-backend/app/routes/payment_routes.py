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
    ---
    tags:
      - Payments
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - order_id
            - phone_number
          properties:
            order_id:
              type: integer
              example: 1
            phone_number:
              type: string
              example: 0712345678
              description: Kenyan phone number (0712345678 or 254712345678)
    responses:
      200:
        description: STK push sent successfully
        schema:
          properties:
            message:
              type: string
            CheckoutRequestID:
              type: string
            ResponseCode:
              type: string
            CustomerMessage:
              type: string
      400:
        description: Invalid request or validation error
      404:
        description: Order not found
      500:
        description: M-Pesa error
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('order_id') or not data.get('phone_number'):
            return jsonify({'error': 'order_id and phone_number required'}), 400
        
        # Get order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Get payment amount (ensures min 1 KES)
        amount = order.get_payment_amount()
        
        # Clean and validate phone number
        phone = str(data['phone_number']).strip().replace(' ', '').replace('-', '')
        
        # Provide helpful feedback for common phone formats
        if len(phone) < 9:
            return jsonify({'error': 'Phone number too short. Use format: 0712345678 or 254712345678'}), 400
        if len(phone) > 13:
            return jsonify({'error': 'Phone number too long. Use format: 0712345678 or 254712345678'}), 400
        
        print(f"Processing payment: Order={order.id}, Amount={amount} KES, Phone={phone}")
        
        # Initiate STK push
        response = mpesa.stk_push(
            phone_number=phone,
            amount=amount,
            account_reference=f"ORD{order.id}",
            transaction_desc=f"Order{order.id}"
        )
        
        print(f"M-Pesa Response: {response}")  # Debug logging
        
        # Return the full response with CheckoutRequestID
        return jsonify({
            'message': 'STK push sent. Check your phone to complete payment.',
            'CheckoutRequestID': response.get('CheckoutRequestID'),
            'MerchantRequestID': response.get('MerchantRequestID'),
            'ResponseCode': response.get('ResponseCode'),
            'ResponseDescription': response.get('ResponseDescription'),
            'CustomerMessage': response.get('CustomerMessage'),
            'amount': amount,
            'phone': phone,
            'mpesa_response': response
        }), 200
        
    except ValueError as e:
        # Validation errors (phone number, amount)
        print(f"Validation Error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"M-Pesa Error: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payments/status/<checkout_request_id>', methods=['GET'])
def check_payment_status(checkout_request_id):
    """
    Check M-Pesa payment status
    ---
    tags:
      - Payments
    parameters:
      - in: path
        name: checkout_request_id
        required: true
        schema:
          type: string
        description: CheckoutRequestID from STK push response
    responses:
      200:
        description: Payment status
        schema:
          properties:
            checkout_request_id:
              type: string
            status:
              type: string
              enum: [pending, completed, cancelled, failed, timeout]
            result_code:
              type: string
            message:
              type: string
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
