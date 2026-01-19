import requests
import base64
from datetime import datetime
import os

class MPesaService:
    def __init__(self):
        # Get credentials from environment variables or use defaults
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY', 'your_consumer_key_here')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET', 'your_consumer_secret_here')
        self.business_shortcode = os.getenv('MPESA_SHORTCODE', '174379')
        self.passkey = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
        
        # Sandbox URLs
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        self.query_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        
    def get_access_token(self):
        """Get OAuth access token from Daraja API"""
        try:
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded}"
            }
            
            response = requests.get(self.auth_url, headers=headers)
            response.raise_for_status()
            
            return response.json()['access_token']
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    def generate_password(self, timestamp):
        """Generate password for STK push"""
        data = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(data.encode()).decode()
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiate STK Push payment
        
        Args:
            phone_number: Customer phone (format: 254XXXXXXXXX)
            amount: Amount to charge
            account_reference: Order ID or reference
            transaction_desc: Description of transaction
        """
        try:
            # Get access token
            access_token = self.get_access_token()
            
            # Generate timestamp and password
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = self.generate_password(timestamp)
            
            # Format phone number (remove leading 0 or +, ensure 254 prefix)
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]
            elif not phone_number.startswith('254'):
                phone_number = '254' + phone_number
            
            # Prepare request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://phase-4-project-order-flow-backend.onrender.com/api/payments/mpesa/callback",
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"STK Push failed: {str(e)}")

    def query_stk_status(self, checkout_request_id):
        """
        Query the status of an STK Push transaction
        
        Args:
            checkout_request_id: CheckoutRequestID from STK push response
        """
        try:
            # Get access token
            access_token = self.get_access_token()
            
            # Generate timestamp and password
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = self.generate_password(timestamp)
            
            # Prepare request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            response = requests.post(self.query_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"Query failed: {str(e)}")
