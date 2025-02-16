import cv2
from fire_detector import FireDetection
import numpy as np

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(output_video_frames, output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()

def draw_detections(frame, detections):
    boxes = []
    scores = []
    
    for box_array in detections:
        if isinstance(box_array, np.ndarray):
            for box in box_array:
                if len(box) == 4:
                    x1, y1, x2, y2 = map(int, box)
                    boxes.append([x1, y1, x2, y2])
                    scores.append(1.0)

    if len(boxes) > 0:
        boxes = np.array(boxes)
        scores = np.array(scores)
        indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), score_threshold=0.5, nms_threshold=0.4)

        if len(indices) > 0:
            largest_box = None
            largest_area = 0
            for i in indices.flatten():
                x1, y1, x2, y2 = boxes[i]
                area = (x2 - x1) * (y2 - y1)
                if area > largest_area:
                    largest_area = area
                    largest_box = (x1, y1, x2, y2)

            if largest_box is not None:
                x1, y1, x2, y2 = largest_box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return frame

# Twilio credentials (replace with your actual credentials)
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client  # Ensure Twilio is imported

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = "AC7b3dfc7a47154cfd2c6a41f5b7e8f34e"
TWILIO_AUTH_TOKEN = "1f9834e86b001e221f75c0ee7474aa65"
TWILIO_PHONE_NUMBER = "+18886118361"
EMERGENCY_NUMBER = "+1911"  # Replace with an emergency contact if needed

def call_911():
    print("Attempting to place an emergency call...")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    call = client.calls.create(
        to=EMERGENCY_NUMBER,  
        from_=TWILIO_PHONE_NUMBER,
        twiml="<Response><Say>Fire detected! Please send help immediately.</Say></Response>"
    )
    
    print(f"Emergency call placed. Call SID: {call.sid}")

def alert_and_call_911():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askyesno("Emergency Alert", "Fire detected! Call 911?")
    if response:
        call_911()
    else:
        print("Emergency call canceled.")

def main():
    input_video_path = "input_videos/input_video_fire.mp4"
    output_video_path = "output_videos/detected_fire.mp4"

    video_frames = read_video(input_video_path)
    fire_detector = FireDetection("weights/new_fire_detection.pt")

    processed_frames = []

    for frame in video_frames:
        detections = fire_detector.detect_fire(frame)
        frame_with_detections = draw_detections(frame, detections)
        processed_frames.append(frame_with_detections)

        # Check if fire is detected, then trigger the emergency call pop-up
        if len(detections) > 0:
            alert_and_call_911()  # <-- New function integrated here

    save_video(processed_frames, output_video_path)

    print(f"Processed video saved at: {output_video_path}")

if __name__ == "__main__":
    main()