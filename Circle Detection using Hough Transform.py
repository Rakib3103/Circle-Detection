import cv2
import numpy as np

img = cv2.imread('/home/rakib/Documents/4th Kibo RPC/circle.png', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian Blur to reduce noise
img_blur = cv2.GaussianBlur(img, (5,5), 1)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

# Draw detected circles on the original image
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)

cv2.imshow('Circle Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
