import cv2
import numpy as np

def find_horizontal_lines(image_path):
    # Step 1: Read and preprocess the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Step 2: Find connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    print(stats)
    # Step 3: Filter horizontal components
    horizontal_lines = []
    for i in range(1, num_labels):  # Skip the background label (0)
        left, top, width, height, _ = stats[i]
        aspect_ratio = width / height
        if aspect_ratio > 10:  # Adjust this threshold based on your image
            horizontal_lines.append((left, top, left+width, top+height))

    return horizontal_lines

def draw_horizontal_lines(image_path, horizontal_lines):
    image = cv2.imread(image_path)
    print(horizontal_lines)
    for line in horizontal_lines:
        cv2.line(image, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)

    #cv2.imshow('Detected Horizontal Lines', image)
    cv2.imwrite("./saved_images/save_eroded.jpg", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage:
image_path = 'test/images/1.png'
horizontal_lines = find_horizontal_lines(image_path)
draw_horizontal_lines(image_path, horizontal_lines)
