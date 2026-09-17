import cv2, numpy as np

def nothing(x): pass  # callback for trackbars

cap = cv2.VideoCapture(0)
cv2.namedWindow("Tuner")

# Create 6 trackbars: H_min, S_min, V_min, H_max, S_max, V_max
cv2.createTrackbar("H min", "Tuner", 0,   179, nothing)
cv2.createTrackbar("S min", "Tuner", 50,  255, nothing)
cv2.createTrackbar("V min", "Tuner", 50,  255, nothing)
cv2.createTrackbar("H max", "Tuner", 85,  179, nothing)
cv2.createTrackbar("S max", "Tuner", 255, 255, nothing)
cv2.createTrackbar("V max", "Tuner", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Read current trackbar positions
    h1=cv2.getTrackbarPos("H min","Tuner")
    s1=cv2.getTrackbarPos("S min","Tuner")
    v1=cv2.getTrackbarPos("V min","Tuner")
    h2=cv2.getTrackbarPos("H max","Tuner")
    s2=cv2.getTrackbarPos("S max","Tuner")
    v2=cv2.getTrackbarPos("V max","Tuner")

    lower = np.array([h1, s1, v1])
    upper = np.array([h2, s2, v2])
    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow("Tuner", frame)
    cv2.imshow("Mask",  mask)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release(); cv2.destroyAllWindows()
