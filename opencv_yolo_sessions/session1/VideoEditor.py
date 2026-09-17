
import cv2
import numpy as np


############# Concept 5 ######################


# cap = cv2.VideoCapture(0)   # 0 = default webcam

# while True:                 # loop forever
#     ret, frame = cap.read() # grab a frame
#     if not ret:
#         print("Camera error!"); break

#     # ── YOUR CODE GOES HERE ──
#     frame = cv2.resize(frame, (640, 480))

#     cv2.imshow("Webcam", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):  # q to quit
#         break

# cap.release()
# cv2.destroyAllWindows()

############# Concept 6 ######################

img = cv2.imread("resources/lena.png")

# Step 1: Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Step 2: Define color range and create mask
lower = np.array([0, 100, 100])   # green low
upper = np.array([10, 255, 255]) # green high
mask = cv2.inRange(hsv, lower, upper)
# mask: white where color matches, black elsewhere

# Step 3: Find contours (outlines of white blobs)
contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

# Step 4: Draw bounding box for each contour
for cnt in contours:
    if cv2.contourArea(cnt) > 500:  # ignore noise
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

cv2.imshow('Mask', mask)
cv2.imshow('Detected', img)
cv2.waitKey(0)