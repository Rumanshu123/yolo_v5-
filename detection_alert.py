import cv2
import torch
import time
import os
import smtplib
import requests
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Verify numpy version
if not hasattr(np, '_no_nep50_warning'):
    print("Warning: NumPy version may cause issues with YOLOv5")
    print("Current NumPy version:", np.__version__)
    print("Recommended: pip install numpy==1.23.5")

# Email configuration
EMAIL_ADDRESS = "rumanshuchandekar89@gmail.com"
EMAIL_PASSWORD = "czytmpcof145zwedxgg"
RECIPIENT_EMAIL = "rumanshuchandekar89@gmail.com"

# Detection area
ROI = (300, 200, 1000, 800)
CONF_THRESH = 0.5

# Load YOLOv5 model with error handling
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)
    print("YOLOv5 model loaded successfully")
except Exception as e:
    print(f"Error loading YOLOv5 model: {e}")
    print("Try these solutions:")
    print("1. pip install numpy==1.23.5")
    print("2. pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt")
    exit(1)

# [Rest of your original script remains the same...]

def send_email(image_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Security Alert: Object Detected!"
    
    body = "An object was detected in the restricted area. See attached image."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(image_path))
    msg.attach(image)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def is_in_roi(bbox, roi):
    x1, y1, x2, y2 = bbox
    roi_x1, roi_y1, roi_x2, roi_y2 = roi
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return (roi_x1 <= center_x <= roi_x2) and (roi_y1 <= center_y <= roi_y2)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    last_alert_time = 0
    alert_cooldown = 30
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            cv2.rectangle(frame, (ROI[0], ROI[1]), (ROI[2], ROI[3]), (0, 255, 0), 2)
            results = model(frame)
            detections = results.pandas().xyxy[0]
            object_detected = False
            
            for _, det in detections.iterrows():
                if det['confidence'] > CONF_THRESH:
                    x1, y1, x2, y2 = int(det['xmin']), int(det['ymin']), int(det['xmax']), int(det['ymax'])
                    color = (0, 0, 255)
                    
                    if is_in_roi((x1, y1, x2, y2), ROI):
                        color = (255, 0, 0)
                        object_detected = True
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{det['name']} {det['confidence']:.2f}", 
                               (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            current_time = time.time()
            if object_detected and (current_time - last_alert_time) > alert_cooldown:
                last_alert_time = current_time
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                image_path = f"detection_{timestamp}.jpg"
                cv2.imwrite(image_path, frame)
                print("\aALERT! Object detected in restricted area!")
                print(f"Saved: {image_path}")
                send_email(image_path)
            
            cv2.imshow("YOLOv5 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()