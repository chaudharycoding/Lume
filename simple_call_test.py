from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

print("\n=== Making Test Call ===")
print("Calling from: +14134660906")
print("Calling to: +15082398066")

# Initialize Twilio client
client = Client(account_sid, auth_token)

try:
    call = client.calls.create(
        to='+15082398066',
        from_='+14134660906',
        twiml='<Response><Say>This is a simple test call. Please confirm if you receive this.</Say></Response>'
    )
    print("\nCall initiated:")
    print(f"Call SID: {call.sid}")
    print(f"Status: {call.status}")

except Exception as e:
    print("\nError:")
    print(str(e)) 