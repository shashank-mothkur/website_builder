import cv2
import numpy as np

# Load your image
image = cv2.imread('test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection (optional, but can help improve results)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
cv2.imshow("edges",edges)
cv2.waitKey(0)

# Use Hough Line Transform to detect lines
#lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None , 50, 10)

# Draw the detected lines on the original image
'''if lines is not None:
    for rho, theta in lines[:, 0]:
        if np.pi/2 - 0.1 < theta < np.pi/2 + 0.1:  # Filter for horizontal lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)'''
if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

# Display the image with detected lines
cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()