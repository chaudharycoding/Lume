from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = '+14134660906'  # Hardcoded verified number
to_number = '+14134660906'    # Hardcoded destination number

print("\n=== Making Emergency Call ===")
print(f"From: {from_number}")
print(f"To: {to_number}")

try:
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Make the call with more interactive TwiML
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        twiml='''
            <Response>
                <Say voice="alice" language="en-US">
                    Alert! This is an urgent test call from your fire detection system.
                    A potential fire has been detected in the monitored area.
                    Please press any key to acknowledge this message.
                </Say>
                <Gather numDigits="1" timeout="10"/>
                <Say>No input received. Repeating message.</Say>
                <Pause length="1"/>
                <Say voice="alice" language="en-US">
                    This is a repeat of the emergency alert.
                    A potential fire has been detected. Please respond immediately.
                </Say>
            </Response>
        '''
    )
    
    print("\n=== Call Status ===")
    print(f"Call SID: {call.sid}")
    print(f"Status: {call.status}")
    
    # Fetch and print call details
    call_details = client.calls(call.sid).fetch()
    print("\n=== Call Details ===")
    print(f"From: {call_details.from_}")
    print(f"To: {call_details.to}")
    print(f"Status: {call_details.status}")
    print(f"Direction: {call_details.direction}")
    
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