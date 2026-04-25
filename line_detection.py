import numpy as np
import cv2
def detect_lines(minlength,edges):

    # cv2.imwrite('./Tests/edges'+ trans_id,edges)
    value, ref_val = 20, 5  # to remove random waste

   # pixel thresh
    lines = cv2.HoughLinesP(
        edges,
        # Input edge image
        1,
        # Distance resolution in pixels
        np.pi / 180,
        # Angle resolution in radians
        threshold=15,
        # Min number of votes for valid line
        minLineLength=minlength,
        # Min allowed length of line
        maxLineGap=6
        # Max allowed gap between line for joining them
    )

    return lines

image = cv2.imread("test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg",0)

blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, threshold1=30, threshold2=100)
x,y,w,h = 23, 102, 597, 534
im = edges[y:y+h,x:x+w]
min_w =int(534* 0.9)
result = detect_lines(min_w,im)
# print(result)
im2 = image[y:y+h,x:x+w]
# for i in result:
#     for j in i:
#         cv2.rectangle(im2,(j[0],j[2]),(j[1],j[3]),(0,255,0),2)

line_image = np.copy(im2) * 0

for line in result:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

        cv2.imshow("image",line_image)
        cv2.waitKey(0)

