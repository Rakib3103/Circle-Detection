import cv2
import numpy as np

# Read input image
img = cv2.imread('C:\\Users\\mazha\\OneDrive\\Desktop\\Kibo\\circle.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to remove noise
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(gray_blur, 50, 200)

# Apply Hough transform
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                           param1=50, param2=30, minRadius=0, maxRadius=0)

# Convert the (x, y) coordinates and radius of the circles to integers
circles = np.uint16(np.around(circles))

# Draw the detected circles on the original image
for i in circles[0, :]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

# Display the image with detected circles
cv2.imshow('Detected Circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
