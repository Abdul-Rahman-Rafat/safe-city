from datetime import datetime
from ultralytics import YOLO
import cv2
import math

def video_detection(path_x):
    # Create a Webcam Object
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    model = YOLO(r"D:\pro\crowd59rp.pt")
    
    classNames1 = ['person']
    
    last_saved_time = datetime.now()

    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        
        detection_occurred = False  # Flag to indicate if detection occurred
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                conf = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])
                class_name = classNames1[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                if class_name == 'person':
                    color = (222, 82, 175)
                elif class_name == 'knife':
                    color = (0, 149, 255)
                elif class_name == 'gun':
                    color = (0, 204, 255)
                else:
                    color = (85, 45, 255)
                if conf > 0.65:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1, y1-2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
                    detection_occurred = True
        
        # Check if a detection occurred and if it's time to save an image
        if detection_occurred:
            current_time = datetime.now()
            time_diff = (current_time - last_saved_time).total_seconds()
            if time_diff >= 10:
                cv2.imwrite(f'detected_image_{current_time.strftime("%Y%m%d_%H%M%S")}.jpg', img)
                last_saved_time = current_time
        
        yield img

    cv2.destroyAllWindows()
