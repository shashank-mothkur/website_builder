import cv2

# Load your image
image = cv2.imread('test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg', cv2.IMREAD_GRAYSCALE)

# Step 1: Apply edge detection
edges = cv2.Canny(image, 50, 150)

# Step 2: Connected Components Labeling
_, labels, stats, _ = cv2.connectedComponentsWithStats(edges)

# Step 3: Filter Horizontal Lines
for i, stat in enumerate(stats):
    x, y, w, h, area = stat
    aspect_ratio = float(w) / h

    # Define a threshold for aspect ratio to consider it a horizontal line
    if aspect_ratio > 5:
        cv2.rectangle(image, (x, y), (x + w, y + h), 255, 2)

# Visualize the result
cv2.imshow('Horizontal Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
