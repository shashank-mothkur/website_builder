'''import cv2
import numpy as np

# Let's load a simple image with 3 black squares
image = cv2.imread('test/images/er5.png')
cv2.waitKey(0)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
#edged = cv2.Canny(gray, 30, 200)
#cv2.imshow("edges",edged)

cv2.waitKey(0)
kernel = np.zeros((5, 5), np.uint8)
dilated_image = cv2.dilate(gray, kernel, iterations=1)
cv2.imshow('Canny Edges After dilate', dilated_image)
cv2.waitKey(0)
# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
contours, hierarchy = cv2.findContours(dilated_image,
                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#cv2.imshow('Canny Edges After Contouring', edged)
#cv2.waitKey(0)

print("Number of Contours found = " + str(len(contours)))
print(contours)
# Draw all contours
# -1 signifies drawing all contours
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
for contour in contours:
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    cv2.imshow('Contours', image)
    cv2.waitKey(0)
cv2.destroyAllWindows()'''

import cv2
import numpy as np

# Load the image
image = cv2.imread('test/images/er4.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out horizontal contours
horizontal_lines = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if h > 5 and w > 100:
        horizontal_lines.append(contour)

# Draw the horizontal lines on the original image
line_image = np.copy(image)
#cv2.drawContours(line_image, horizontal_lines, -1, (0, 255, 0), 2)

for contour in horizontal_lines:
    cv2.drawContours(line_image, [contour], -1, (0, 255, 0), 2)

    cv2.imshow('Contours', line_image)
    cv2.waitKey(0)

# Display the result
cv2.imshow('Horizontal Lines', line_image)
cv2.waitKey(0)
cv2.destroyAllWindows()