import cv2
import numpy as np

# Load an image from disk
img = cv2.imread("resources/lena.png")

# What IS this image?
print(type(img))     # <class 'numpy.ndarray'>
print(img.shape)     # (height, width, channels)
print(img.dtype)     # uint8  (0-255)

# Read one pixel at row=100, col=200
pixel = img[100, 200]
print(pixel)  # [255  48 162]  ← [B, G, R]!

# Show the image
cv2.imshow('My Image', img)
cv2.waitKey(0)     # 0 = wait forever
cv2.destroyAllWindows()
