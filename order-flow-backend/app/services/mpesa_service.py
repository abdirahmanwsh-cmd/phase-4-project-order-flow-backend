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
            print(f"Consumer Key: {self.consumer_key[:10]}...")
            print(f"Consumer Secret: {self.consumer_secret[:10]}...")
            
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded}"
            }
            
            response = requests.get(self.auth_url, headers=headers)
            print(f"Access Token Response Status: {response.status_code}")
            print(f"Access Token Response: {response.text}")
            
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
            # Validate and format amount (minimum 1 KES)
            amount = int(float(amount))
            if amount < 1:
                raise ValueError("Amount must be at least 1 KES")
            
            # Get access token
            access_token = self.get_access_token()
            
            # Generate timestamp and password
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = self.generate_password(timestamp)
            
            # Format phone number (remove leading 0 or +, ensure 254 prefix)
            phone_number = str(phone_number).strip()
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]
            elif not phone_number.startswith('254'):
                phone_number = '254' + phone_number
            
            # Validate phone number (must be 12 digits: 254XXXXXXXXX)
            if not phone_number.isdigit() or len(phone_number) != 12:
                raise ValueError(f"Invalid phone number: {phone_number}. Must be 254XXXXXXXXX (12 digits)")
            
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
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://phase-4-project-order-flow-backend.onrender.com/api/mpesa/callback",
                "AccountReference": str(account_reference)[:13],  # Max 13 chars
                "TransactionDesc": str(transaction_desc)[:13]  # Max 13 chars
            }
            
            print(f"STK Push Request: {payload}")  # Debug
            
            response = requests.post(self.stk_push_url, json=payload, headers=headers, timeout=30)
            
            print(f"STK Push Response Status: {response.status_code}")  # Debug
            print(f"STK Push Response Body: {response.text}")  # Debug
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('errorMessage', error_data.get('errorCode', ''))
                    request_id = error_data.get('requestId', '')
                    
                    # Build detailed error message
                    details = []
                    if error_msg:
                        details.append(f"Error: {error_msg}")
                    if request_id:
                        details.append(f"RequestID: {request_id}")
                    if error_data.get('fault'):
                        fault = error_data['fault']
                        details.append(f"Fault: {fault.get('faultstring', fault)}")
                    
                    full_error = " | ".join(details) if details else response.text
                except:
                    full_error = response.text or "Unknown error"
                
                raise Exception(f"M-Pesa API returned {response.status_code}: {full_error}")
            
            result = response.json()
            
            # Check if M-Pesa accepted the request
            if result.get('ResponseCode') != '0':
                raise Exception(f"M-Pesa rejected request: {result.get('ResponseDescription', 'Unknown error')} (Code: {result.get('ResponseCode')})")
            
            return result
            
        except ValueError as e:
            # Re-raise validation errors as-is
            raise
        except requests.exceptions.Timeout:
            raise Exception("M-Pesa request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to M-Pesa. Check internet connection.")
        except Exception as e:
            if "M-Pesa" in str(e) or "rejected" in str(e) or "timed out" in str(e):
                raise
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
