from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID').strip()
auth_token = os.getenv('TWILIO_AUTH_TOKEN').strip()
from_number = os.getenv('TWILIO_PHONE_NUMBER').strip()
to_number = os.getenv('EMERGENCY_NUMBER').strip()

print("\n=== Twilio Configuration ===")
print(f"Account SID: {account_sid}")
print(f"From Number: {from_number}")
print(f"To Number: {to_number}")

try:
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Check account status
    account = client.api.accounts(account_sid).fetch()
    print(f"\n=== Account Status ===")
    print(f"Status: {account.status}")
    print(f"Type: {account.type}")
    
    # List verified numbers
    print("\n=== Verified Numbers ===")
    verified_numbers = client.outgoing_caller_ids.list()
    for number in verified_numbers:
        print(f"Number: {number.phone_number}")
    
    # Make test call
    print("\n=== Making Test Call ===")
    call = client.calls.create(
        to='+15082398066',  # Hardcoded verified number
        from_='+15082398066',  # Hardcoded Twilio number
        twiml='<Response><Say>This is a test call from your fire detection system.</Say></Response>'
    )
    print(f"Call SID: {call.sid}")
    print(f"Call Status: {call.status}")

except Exception as e:
    print("\n=== Error Details ===")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    if hasattr(e, 'code'):
        print(f"Error Code: {e.code}")
    if hasattr(e, 'msg'):
        print(f"Error Message: {e.msg}")
    if hasattr(e, 'status'):
        print(f"HTTP Status: {e.status}") 