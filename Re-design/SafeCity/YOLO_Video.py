from datetime import datetime
from ultralytics import YOLO
import cv2
import math
from SafeCity.models import Snapshots,User
from SafeCity import db
from SafeCity import app
from pathlib import Path
from query import re_image_name
from mail import send_mail
import tensorrt as trt


output_path = Path.cwd()

img_name = re_image_name()
img_name = int(img_name) + 1

def model(path_x, user, loc, user_mail, CameraID, coroodinate, limit, model_type):
    if model_type == 'Crowd Model':
        global img_name
        cap = cv2.VideoCapture(r'c:\Users\yassi\Downloads\Untitled video - Made with Clipchamp.mp4')
        
        model = YOLO(r"c:\Users\yassi\Desktop\safecity systems\client_side\ui\crowd model\crowd59rp.pt")
        classNames1 = ['person']
        
        last_saved_time = datetime.now()
         
        frame_skip_interval = 1  # Process every 5th frame
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % frame_skip_interval != 0:
                continue

            # Perform object detection on the resized frame
            results = model(frame, imgsz=1024, save=False, conf=0.4, device='cuda')
            
            person_count = 0
            
            for result in results:
                for r in result.boxes.data.tolist():
                    x1, y1, x2, y2 = map(int, r[:4])
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    conf = math.ceil((r[4] * 100)) / 100
                    cls = int(r[5])
                    class_name = classNames1[cls]
                    label = f'{class_name}{conf}'
                    
                    if class_name == 'person' and conf > 0.4:
                        color = (0, 255, 0)
                        person_count += 1
                        
                        # Draw a small red dot at the center of the person
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot
                        
            if person_count >= limit:
                current_time = datetime.now()
                time_diff = (current_time - last_saved_time).total_seconds()
                if time_diff >= 20:
                    file_path = f'{output_path}\\Re-design\\SafeCity\\static\\used_images\\{img_name}.png'
                    print(file_path)
                    cv2.imwrite(file_path, frame)
                    last_saved_time = current_time
                    
                    with app.app_context():
                        send_mail(receiver_mail=user_mail, image_path=file_path, incident_type='person', location=loc, coroodinate=coroodinate)
                        snapshot = Snapshots(Detection_img_ref=img_name, Detection_type='person', Loc=loc, Time=datetime.now(), Alert_sentTo=user, CameraID=CameraID)
                        db.session.add(snapshot)
                        usersnamp = User.query.filter_by(username=user).first()
                        usersnamp.unread_alerts_count+=1
                        db.session.commit()
                    img_name += 1
            
            # Display the person count and overlimit warning if necessary
            if person_count > limit:
                cv2.putText(frame, "Overlimit", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, f"People: {person_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            yield frame

    
    elif model_type == 'Gun Model':
        cap = cv2.VideoCapture(r'c:\Users\yassi\Downloads\Disturbing new footage shows Salvador Ramos in Uvalde school, cops running _ New York Post.mp4')
        
        model = YOLO(r"c:\Users\yassi\Downloads\140e (1).pt")
        classNames1 = ['fire', 'knife', 'gun']
        
        last_saved_time = datetime.now()
        frame_skip_interval = 5  # Process every 5th frame
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % frame_skip_interval != 0:
                continue

            # Resize the frame to 640x360
            frame = cv2.resize(frame, (640, 360))

            # Perform object detection on the resized frame
            results = model(frame, stream=True, device='cuda')
            
            detection_occurred = False
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    class_name = classNames1[cls]
                    label = f'{class_name}{conf}'
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    if class_name == 'fire':
                        color = (222, 82, 175)
                    elif class_name == 'knife':
                        color = (0, 149, 255)
                    elif class_name == 'gun':
                        color = (0, 204, 255)
                    else:
                        color = (85, 45, 255)
                    if conf > 0.65:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                        cv2.rectangle(frame, (x1, y1), c2, color, -1, cv2.LINE_AA)
                        cv2.putText(frame, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
                        detection_occurred = True
            
            if detection_occurred:
                current_time = datetime.now()
                time_diff = (current_time - last_saved_time).total_seconds()
                if time_diff >= 20:
                    file_path = f'{output_path}\\Re-design\\SafeCity\\static\\used_images\\{img_name}.png'
                    print(file_path)
                    cv2.imwrite(file_path, frame)
                    last_saved_time = current_time
                    
                    with app.app_context():
                        send_mail(receiver_mail=user_mail, image_path=file_path, incident_type=class_name, location=loc, coroodinate=coroodinate)
                        snapshot = Snapshots(Detection_img_ref=img_name, Detection_type=class_name, Loc=loc, Time=datetime.now(), Alert_sentTo=user, CameraID=CameraID)
                        db.session.add(snapshot)
                        db.session.commit()
                    img_name += 1
            
            yield frame
