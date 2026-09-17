import cv2

cap = cv2.VideoCapture(0)

while True:

    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image into black and white
    _, threshold = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY
    )

    # Find the contours
    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Analyze each contour
    for cnt in contours:

        # Ignore small objects/noise
        if cv2.contourArea(cnt) < 1000:
            continue

        # Calculate the perimeter of the contour
        perimeter = cv2.arcLength(cnt, True)

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
            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.9 <= ratio <= 1.1:
                shape = "Square"
            else:
                shape = "Rectangle"

        else:
            shape = "Circle"

        # Draw the contour
        cv2.drawContours(
            frame,
            [cnt],
            -1,
            (0, 255, 0),
            3
        )

        # Get the position of the object
        x, y, w, h = cv2.boundingRect(cnt)

        # Write the shape name
        cv2.putText(
            frame,
            shape,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # Display the original color image
    cv2.imshow("Shape Detector", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()