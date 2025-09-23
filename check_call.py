from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_PHONE_NUMBER')
to_number = os.getenv('EMERGENCY_NUMBER')

print("\n=== Twilio Account Details ===")
print(f"Account SID: {account_sid}")
print(f"From Number: {from_number}")
print(f"To Number: {to_number}")

try:
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Check account status first
    account = client.api.accounts(account_sid).fetch()
    print(f"\n=== Account Status ===")
    print(f"Status: {account.status}")
    print(f"Type: {account.type}")
    
    # Check account balance
    balance = client.api.balance.fetch()
    print(f"Account Balance: ${balance.balance}")
    print(f"Currency: {balance.currency}")
    
    # List verified numbers
    print("\n=== Verified Numbers ===")
    verified_numbers = client.outgoing_caller_ids.list()
    for number in verified_numbers:
        print(f"Number: {number.phone_number}")
    
    # Check recent calls
    print("\n=== Recent Calls ===")
    calls = client.calls.list(limit=5)
    for call in calls:
        print(f"\nCall SID: {call.sid}")
        print(f"Status: {call.status}")
        # Fetch specific call for more details
        call_details = client.calls(call.sid).fetch()
        print(f"From: {call_details.from_}")
        print(f"To: {call_details.to}")
        print(f"Duration: {call_details.duration}s")
        print(f"Start Time: {call_details.start_time}")
        print(f"End Time: {call_details.end_time}")
        if call_details.status == 'failed':
            print(f"Error Code: {call_details.error_code}")
            print(f"Error Message: {call_details.error_message}")
    
    # Make a new test call with more verbose TwiML
    print("\n=== Making New Test Call ===")
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        twiml='''
            <Response>
                <Say voice="alice" language="en-US">
                    This is an urgent test call from your fire detection system.
                    If you can hear this message, please press any key.
                    I repeat, this is a test call.
                </Say>
                <Pause length="2"/>
                <Gather numDigits="1" timeout="10" action="/gather"/>
            </Response>
        '''
    )
    print(f"New Call SID: {call.sid}")
    print(f"Initial Status: {call.status}")
    
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