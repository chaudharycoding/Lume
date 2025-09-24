import cv2
from fire_detector import FireDetection
import numpy as np
from twilio.rest import Client
import os
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
EMERGENCY_NUMBER = os.getenv('EMERGENCY_NUMBER', '+1911')  # Default to 911 if not set

def call_911():
    print("\n=== Making Emergency Call ===")
    print(f"Using Twilio Account SID: {TWILIO_ACCOUNT_SID}")
    print(f"Calling from: {TWILIO_PHONE_NUMBER}")
    print(f"Calling to: {EMERGENCY_NUMBER}")
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        call = client.calls.create(
            to=EMERGENCY_NUMBER,  
            from_=TWILIO_PHONE_NUMBER,
            twiml="<Response><Say>Fire detected! Please send help immediately.</Say></Response>"
        )
        print(f"\nEmergency call placed successfully!")
        print(f"Call SID: {call.sid}")
        print(f"Call Status: {call.status}")
        return True
    except Exception as e:
        print(f"\n=== Twilio Error Details ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        if hasattr(e, 'code'):
            print(f"Error Code: {e.code}")
        if hasattr(e, 'msg'):
            print(f"Error Message: {e.msg}")
        if hasattr(e, 'status'):
            print(f"HTTP Status: {e.status}")
        return False

def main(input_video_path, output_video_path):
    try:
        fire_detector = FireDetection("weights/new_fire_detection.pt")
        
        # Process the video and get detections and fire status
        print(f"🔥 Processing video: {input_video_path}")
        detections, is_fire = fire_detector.detect_fire(input_video_path, save_output=True)
        
        if is_fire:
            print("\n🚨 Fire detected in video! Notifying emergency services...")
            # Skip actual call for demo - just simulate
            # call_911()
        else:
            print("\n✅ No significant fire detected in video.")
        
        print(f"✅ Fire detection completed. Fire detected: {is_fire}")
        return is_fire
        
    except Exception as e:
        print(f"❌ Error in main fire detection: {str(e)}")
        raise e

if __name__ == "__main__":
    # Default paths when running directly
    default_input = "input_videos/input_video_fire.mp4"
    default_output = "output_videos/detected_fire.mp4"
    fire_detected = main(default_input, default_output)