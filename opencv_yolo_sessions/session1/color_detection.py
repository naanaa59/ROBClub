import cv2
import numpy as np


# Open the webcam
# 0 means the computer's default camera
cap = cv2.VideoCapture(0)


# Define the colors that we want to detect
#
# Each color has:
# - "ranges"      → HSV values used to detect the color
# - "draw_color"  → BGR color used to draw the contour
colors = {

    "Red": {
        # Red is special because it is located
        # at both ends of the HSV scale
        "ranges": [
            (np.array([0, 100, 100]), np.array([10, 255, 255])),
            (np.array([170, 100, 100]), np.array([179, 255, 255]))
        ],

        # OpenCV uses BGR, so (0, 0, 255) = red
        "draw_color": (0, 0, 255)
    },

    "Green": {
        # HSV range for green
        "ranges": [
            (np.array([35, 50, 50]), np.array([85, 255, 255]))
        ],

        # (0, 255, 0) = green in BGR
        "draw_color": (0, 255, 0)
    },

    "Blue": {
        # HSV range for blue
        "ranges": [
            (np.array([90, 50, 50]), np.array([130, 255, 255]))
        ],

        # (255, 0, 0) = blue in BGR
        "draw_color": (255, 0, 0)
    }
}


# Keep reading images from the webcam
while True:

    # Read one frame from the webcam
    #
    # ret   → tells us if the frame was successfully captured
    # frame → the actual image
    ret, frame = cap.read()

    # If the camera failed to give us an image,
    # stop the program
    if not ret:
        break


    # Convert the image from BGR to HSV
    #
    # HSV makes it easier to detect specific colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Check each color we defined above
    #
    # Example:
    # color_name = "Red"
    # color_info = information about red
    for color_name, color_info in colors.items():

        # Create an empty black image.
        #
        # This will be our MASK.
        #
        # The mask will contain:
        # White → pixels that match the color
        # Black → everything else
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)


        # A color can have one or more HSV ranges.
        #
        # Red has two ranges, while green and blue
        # currently have one.
        for lower, upper in color_info["ranges"]:

            # Find the pixels that are inside
            # the current HSV range
            current_mask = cv2.inRange(
                hsv,
                lower,
                upper
            )

            # Combine the current mask with the previous one
            #
            # This is especially important for red,
            # because red uses two HSV ranges.
            mask = cv2.bitwise_or(
                mask,
                current_mask
            )


        # Find the contours of the detected color
        #
        # A contour is the boundary/outline
        # of a detected region.
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        # Look at every contour we found
        for cnt in contours:

            # Ignore very small regions.
            #
            # This helps remove noise and tiny
            # accidental color detections.
            if cv2.contourArea(cnt) < 1000:
                continue


            # Draw the contour on the ORIGINAL
            # color image, not on the mask.
            #
            # This allows us to keep seeing
            # the normal webcam image.
            cv2.drawContours(
                frame,
                [cnt],
                -1,
                color_info["draw_color"],
                3
            )


            # Get the position and size of the object
            #
            # x, y → position
            # w, h → width and height
            x, y, w, h = cv2.boundingRect(cnt)


            # Write the name of the detected color
            # above the object
            cv2.putText(
                frame,
                color_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color_info["draw_color"],
                2
            )


    # Display the ORIGINAL webcam image
    #
    # The mask is NOT displayed.
    # We only use it internally to detect colors.
    cv2.imshow("Color Detector", frame)


    # Press Q to quit the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release the webcam
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()