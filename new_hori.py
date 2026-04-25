import cv2
import numpy as np
from queue import Queue

def bfs_connected_components(image):
    height, width = image.shape[:2]
    visited = np.zeros((height, width), dtype=bool)
    components = []
    cv2.imshow("image",image)
    cv2.waitKey(0)
    for y in range(height):
        for x in range(width):
            if not visited[y, x] and image[y, x] == 255:
                component = []
                queue = Queue()
                queue.put((x, y))
                visited[y, x] = True

                while not queue.empty():
                    cx, cy = queue.get()
                    component.append((cx, cy))

                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx] and image[ny, nx] == 255:
                            queue.put((nx, ny))
                            visited[ny, nx] = True

                components.append(component)

    return components

def filter_horizontal_components(components, aspect_ratio_threshold):
    filtered_components = []
    for component in components:
        x, y, w, h = cv2.boundingRect(np.array(component))
        aspect_ratio = w / h
        if aspect_ratio < aspect_ratio_threshold:
            filtered_components.append(component)

    return filtered_components

# Load the image and preprocess it
image = cv2.imread('test/images/er.png',0)
print(image.shape)
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# Find connected components
components = bfs_connected_components(binary_image)

# Filter horizontal components (adjust aspect_ratio_threshold as needed)
aspect_ratio_threshold = 0.1
horizontal_components = filter_horizontal_components(components, aspect_ratio_threshold)
print(horizontal_components)
# Draw the lines on the original image
#output_image = cv2.imread('test/images/1.png')
for component in horizontal_components:
    for x, y in component:
        cv2.circle(binary_image, (x, y), 1, (0, 255, 0), -1)

# Display the image with detected lines
cv2.imshow('Image with Detected Horizontal Lines', binary_image)
cv2.imwrite("saved_images/save_erode.jpg",binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

