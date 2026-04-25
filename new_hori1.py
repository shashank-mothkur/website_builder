import cv2
import numpy as np


def find_largest_horizontal_lines(binary_image):
    lines = cv2.HoughLinesP(binary_image, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is not None:
        horizontal_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y2 - y1) < 5:  # Assuming a threshold for horizontal lines
                horizontal_lines.append([(x1, y1), (x2, y2)])

        if horizontal_lines:
            largest_line = max(horizontal_lines, key=lambda line: abs(line[0][1] - line[1][1]))
            return largest_line

    return None


# Load the binary image
binary_image = cv2.imread('test/images/1.png', cv2.IMREAD_GRAYSCALE)
_, binary_image = cv2.threshold(binary_image, 128, 255, cv2.THRESH_BINARY)

# Find the largest horizontal line
largest_horizontal_line = find_largest_horizontal_lines(binary_image)

# Draw the line on the original image
output_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
if largest_horizontal_line is not None:
    cv2.line(output_image, largest_horizontal_line[0], largest_horizontal_line[1], (0, 255, 0), 2)

# Display the result
#cv2.imshow('Result Image', output_image)
cv2.imwrite("./saved_images/save_eroded.jpg",output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



