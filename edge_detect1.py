import cv2
import numpy as np
from PIL import Image
# Load an image from file
image = cv2.imread('./test/images/img_18.png', cv2.IMREAD_GRAYSCALE)

# Get the dimensions of the image

def edge_detection(image):

    # Apply Gaussian blur to the image to reduce noise
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, threshold1=30, threshold2=100)


    # Add batch dimension if needed

    # Apply binary thresholding to the edges
    _, binary_edges = cv2.threshold(edges, 30, 255, cv2.THRESH_BINARY_INV)
    three_channel_binary = cv2.merge([binary_edges, binary_edges, binary_edges])

    # cv2.imshow('Original Image', image)
    cv2.imshow('Canny Edges', edges)
    cv2.imshow('image', three_channel_binary)
    #cv2.imshow('Binary Edges', binary_edges)
    #cv2.imshow('canny_input', canny_input)

    # Wait for a key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("./saved_images/save_edge.jpg", three_channel_binary)
    #return binary_edges
    #return three_channel_binary

#img = edge_detection(image)

#cv2.imwrite("./saved_images/save_edge.jpg",img)