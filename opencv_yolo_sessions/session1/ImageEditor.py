import cv2
import time
import numpy as np

#####################################################################
#####################################################################
###################     Live Code Challenge 1   #####################
#####################################################################
#####################################################################




#####################################################################
#####################################################################
###################     Live Code Challenge 2   #####################
#####################################################################
#####################################################################





#####################################################################
###################        Resize               #####################
#####################################################################
# img = cv2.imread("resources/lena.png")
# print(img.shape)

# imgResize = cv2.resize(img, (300, 200))
# print(imgResize.shape)
# cv2.imshow("Output", img)
# cv2.imshow("Resize", imgResize)
# cv2.waitKey(0)

#####################################################################
###################               Crop          #####################
#####################################################################
# img = cv2.imread("resources/lena.png")
# print(img.shape)
# imgCropped = img[0:100, 200:300]
# cv2.imshow("Cropped", imgCropped)
# cv2.imshow("Output", img)
# cv2.waitKey(0)


#####################################################################
###################        Gray / Blur          #####################
#####################################################################
# img = cv2.imread("resources/lena.png")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)

# cv2.imshow("Gray Image", imgGray)
# cv2.imshow("Blur Image", imgBlur)

# cv2.waitKey(0)


#####################################################################
###################        Flip                 #####################
#####################################################################
# img = cv2.imread("resources/lena.png")
# imgFliped = cv2.flip(img, 1)


# cv2.imshow("Flipped Image", imgFliped)
# cv2.imshow("Original Image", img)
# cv2.waitKey(0)


#####################################################################
###################        Draw                 #####################
#####################################################################
# import cv2
# import numpy as np


# # Create a 337 × 337 image with 3 channels
# img = np.zeros((337, 337, 3), np.uint8)

# print(img)

# # Fill the entire image with blue
# # OpenCV uses BGR
# img[:] = 255, 0, 0

# # Draw a green rectangle
# cv2.rectangle(
#     img,
#     (50, 100),
#     (250, 250),
#     (0, 255, 0),
#     2
# )

# # Write text
# cv2.putText(
#     img,
#     "Hi!",
#     (50, 50),
#     cv2.FONT_HERSHEY_SIMPLEX,
#     1,
#     (255, 255, 255),
#     2
# )

# # Display the final image
# cv2.imshow("Original Image", img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

#####################################################################
###################        Copy                 #####################
#####################################################################
# import cv2

# img = cv2.imread("resources/lena.png")
# copy = img.copy()

# cv2.circle(copy, (100, 100), 30, (0, 255, 0), 2)

# cv2.imshow("Original", img)
# cv2.imshow("Modified", copy)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
