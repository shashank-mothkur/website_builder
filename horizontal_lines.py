import cv2
import numpy as np

# Read the image
image = cv2.imread('test/images/er.png')


# Apply Gaussian blur to reduce noise (optional but recommended)
#blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Apply edge detection using Canny
#edges = cv2.Canny(blurred, 30, 150, apertureSize=3)


# Find lines using Hough Line Transform

# edges = cv2.Canny(blurred, threshold1=30, threshold2=100,apertureSize=3)
# cv2.imshow("edges",edges)
# cv2.waitKey(0)
# # Apply binary thresholding to the edges
# binary_edges = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)[1]
#
# cv2.imshow('binary_edges', binary_edges)
# cv2.waitKey(0)
# kernel = np.ones((4, 4), np.uint8)
# #print(binary_edges)
# inverted_edges = cv2.bitwise_not(binary_edges)
# image = cv2.erode(inverted_edges, kernel, iterations=1)
# cv2.imshow("image",image)
# cv2.waitKey(0)

lines = cv2.HoughLinesP(image ,1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# Extract horizontal lines
horizontal_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    if abs(y2 - y1) < 10:  # Adjust the threshold for what you consider "horizontal"
        horizontal_lines.append((x1, y1, x2, y2))

# Draw the lines on the original image (optional)
line_image = np.copy(image)
for line in horizontal_lines:
    x1, y1, x2, y2 = line
    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the original image with lines (optional)
cv2.imwrite("./saved_images/save_eroded.jpg",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print coordinates of horizontal lines
for line in horizontal_lines:
    print(f"Start Point: ({line[0]}, {line[1]}), End Point: ({line[2]}, {line[3]})")



