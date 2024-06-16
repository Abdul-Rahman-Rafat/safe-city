import cv2

# Replace with your DroidCam IP address
droidcam_url = 'http://192.168.1.5:4747/video'

# Open the DroidCam stream with FFmpeg backend in OpenCV
cap = cv2.VideoCapture(droidcam_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Could not open video stream.")
else:
    print("Video stream opened successfully.")

# Loop to capture frames from the DroidCam stream
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break
    
    # Display the resulting frame
    cv2.imshow('DroidCam Stream', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
