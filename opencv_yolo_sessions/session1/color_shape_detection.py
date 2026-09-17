import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)


# Red HSV ranges
# Red exists at both ends of the HSV scale
LOWER_RED_1 = np.array([0, 100, 100])
UPPER_RED_1 = np.array([10, 255, 255])

LOWER_RED_2 = np.array([170, 100, 100])
UPPER_RED_2 = np.array([179, 255, 255])


while True:

    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break


    # Convert BGR image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Detect the first red range
    mask1 = cv2.inRange(
        hsv,
        LOWER_RED_1,
        UPPER_RED_1
    )

    # Detect the second red range
    mask2 = cv2.inRange(
        hsv,
        LOWER_RED_2,
        UPPER_RED_2
    )

    # Combine both red masks
    mask = cv2.bitwise_or(mask1, mask2)


    # Smooth the mask to remove small noise
    mask = cv2.GaussianBlur(
        mask,
        (5, 5),
        0
    )


    # Find contours of the red objects
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # Analyze every red contour
    for cnt in contours:

        # Ignore very small regions
        if cv2.contourArea(cnt) < 1000:
            continue


        # Calculate the perimeter
        perimeter = cv2.arcLength(
            cnt,
            True
        )


        # Simplify the contour
        approx = cv2.approxPolyDP(
            cnt,
            0.04 * perimeter,
            True
        )


        # Count the corners
        corners = len(approx)


        # Identify the shape
        if corners == 3:

            shape = "Triangle"

        elif corners == 4:

            # Get the bounding rectangle
            x, y, w, h = cv2.boundingRect(cnt)

            # Compare width and height
            ratio = w / float(h)

            if 0.9 <= ratio <= 1.1:
                shape = "Square"
            else:
                shape = "Rectangle"

        else:

            # For this simple version,
            # shapes with many points are considered circles
            shape = "Circle"


        # Draw the contour in red
        cv2.drawContours(
            frame,
            [cnt],
            -1,
            (0, 0, 255),
            3
        )


        # Get the position of the object
        x, y, w, h = cv2.boundingRect(cnt)


        # Write the detected shape
        cv2.putText(
            frame,
            shape,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )


    # Show the original color webcam
    # with the detected shape
    cv2.imshow(
        "Red Shape Detector",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release the webcam
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()