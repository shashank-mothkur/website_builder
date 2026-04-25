import cv2
import numpy as np
from collections import deque
import copy
def bfs_horizontal(image, start_point, visited, threshold):
    height, width = image.shape[:2]
    queue = deque([start_point])
    visited.add(start_point)
    line_points = []

    while queue:
        x, y = queue.popleft()

        # Check if the pixel intensity is greater than a threshold (indicating an edge)
        if image[y, x] > threshold:
            print(image[y, x])
            line_points.append((x, y))

            # Explore right
            new_x, new_y = x + 1, y
            if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited:
                queue.append((new_x, new_y))
                visited.add((new_x, new_y))

            # Explore left
            new_x, new_y = x - 1, y
            if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited:
                queue.append((new_x, new_y))
                visited.add((new_x, new_y))

    return line_points

def detect_horizontal_lines(image, threshold=100):
    # Convert the image to grayscale and apply Canny edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,bin = _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(bin, 50, 150)


    height, width = edges.shape[:2]
    visited = set()
    lines = []

    for y in range(height):
        for x in range(width):
            if (x, y) not in visited and edges[y, x] > 0:
                line_points = bfs_horizontal(edges, (x, y), visited, threshold)
                print(line_points)
                if len(line_points) > 5:  # Filter out short segments (adjust threshold as needed)
                    lines.append(line_points)
    print(lines)
    return lines

# Load the image
image = cv2.imread('test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg')

# Detect horizontal lines using BFS
horizontal_lines = detect_horizontal_lines(image, threshold=100)
length= 0
hori = copy.deepcopy(horizontal_lines)
li=[]

for i in range(0,len(horizontal_lines)):
    li.append(0)
    for j in range(0,len(horizontal_lines)):
        if(abs(i[1]-j[1])<10):
            if(i[0]<=j[0]):
                li[-1]= i
            else:
                li[-1] = j
    length = max(len(i),length)

# Draw the detected lines (optional)
#max_length = max(horizontal_lines)
for line in horizontal_lines:
    print(line)
    #if(len(line) >= 0.8*length):

    for point in line:
            cv2.circle(image, point, 2, (0, 255, 0), -1)
        #cv2.circle(image, line[0], 2, (0, 255, 0), -1)
        #cv2.circle(image, line[-1], 2, (0, 255, 0), -1)
# Display the image with detected lines (optional)
# cv2.imshow('Image with Detected Horizontal Lines', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite("./saved_images/save_eroded.jpg",image)