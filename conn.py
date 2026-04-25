import cv2
import numpy as np

# Load the image
image = cv2.imread('test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find connected components
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)

# Loop through the components and draw points on the image
horr=[]
for i in range(1, num_labels):
    component_mask = (labels == i).astype(np.uint8)
    points = np.column_stack(np.where(component_mask == 1))
    print(points)
    hor=[]
    rev_hor=[]
    flag=0
    for point in points:
        print("point",point)
        '''if(len(hor)==0):
            hor.append(list(point))
            flag=1
        else:
            if(point[0]>hor[-1][0] and abs(hor[-1][1]-point[1])<20):
                hor.append(list(point))
        if(flag==0):
            if(point[0]<hor[-1][0] and abs(hor[-1][1]-point[1])<20):
                rev_hor.append(list(point))
                flag=1
        else:
            if(point[0] < rev_hor[-1][0] and abs(rev_hor[-1][1] - point[1]) < 20):
                rev_hor.append(list(point))'''


        cv2.circle(image, tuple(reversed(point)), 2, (0, 255, 0), -1)  # Draw a green circle at each point
    cv2.imshow("image",image)
    cv2.waitKey(0)
    '''horr.append(hor)
    horr.append(rev_hor[::-1])
# Save the image with points
print(horr)

for i in horr:
    for j in i:
        cv2.circle(image, tuple(reversed(j)), 2, (0, 255, 0), -1)  # Draw a green circle at each point'''
cv2.imwrite('./saved_images/save_eroded.jpg', image)
