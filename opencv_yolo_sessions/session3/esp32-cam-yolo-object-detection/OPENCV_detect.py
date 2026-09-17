import cv2
import numpy as np

# ============================================================
# ESP32-CAM STREAM
# ============================================================

STREAM_URL = "http://192.168.186.122/stream"

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("ERROR: Could not open ESP32-CAM stream")
    exit()

print("ESP32-CAM connected")


# ============================================================
# RED HSV RANGES
# ============================================================

# Red exists at both ends of the HSV scale

LOWER_RED_1 = np.array([
    0,
    100,
    100
])

UPPER_RED_1 = np.array([
    10,
    255,
    255
])


LOWER_RED_2 = np.array([
    170,
    100,
    100
])

UPPER_RED_2 = np.array([
    179,
    255,
    255
])


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # Read frame from ESP32-CAM
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not receive frame")
        break


    # ========================================================
    # CONVERT BGR TO HSV
    # ========================================================

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )


    # ========================================================
    # DETECT RED
    # ========================================================

    mask1 = cv2.inRange(
        hsv,
        LOWER_RED_1,
        UPPER_RED_1
    )

    mask2 = cv2.inRange(
        hsv,
        LOWER_RED_2,
        UPPER_RED_2
    )


    # Combine masks
    mask = cv2.bitwise_or(
        mask1,
        mask2
    )


    # ========================================================
    # REDUCE NOISE
    # ========================================================

    mask = cv2.GaussianBlur(
        mask,
        (5, 5),
        0
    )


    # ========================================================
    # FIND CONTOURS
    # ========================================================

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # ========================================================
    # ANALYZE RED OBJECTS
    # ========================================================

    for cnt in contours:

        # Ignore small objects
        if cv2.contourArea(cnt) < 1000:
            continue


        # Calculate perimeter
        perimeter = cv2.arcLength(
            cnt,
            True
        )


        # Approximate contour
        approx = cv2.approxPolyDP(
            cnt,
            0.04 * perimeter,
            True
        )


        # Number of corners
        corners = len(approx)


        # ====================================================
        # IDENTIFY SHAPE
        # ====================================================

        if corners == 3:

            shape = "Triangle"


        elif corners == 4:

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.9 <= ratio <= 1.1:
                shape = "Square"
            else:
                shape = "Rectangle"


        else:

            shape = "Circle"


        # ====================================================
        # DRAW CONTOUR
        # ====================================================

        cv2.drawContours(
            frame,
            [cnt],
            -1,
            (0, 0, 255),
            3
        )


        # Bounding box
        x, y, w, h = cv2.boundingRect(cnt)


        # ====================================================
        # DISPLAY SHAPE
        # ====================================================

        cv2.putText(
            frame,
            shape,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "ESP32-CAM Red Shape Detection",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()
