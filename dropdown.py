import cv2
import numpy as np
import matplotlib.pyplot as plt
from testing_dropdown import test_drop


#def dropdown(image_path,bboxx):
def dropdown(image,bboxx):
    cv2.imshow("image",image)
    cv2.waitKey(0)

    #image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("image",image)
    #cv2.waitKey(0)

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    #image = cv2.rectangle(image, start_point, end_point, color, thickness)
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ############dropdown
    #x,y,w,h = bboxx[0],53,315,105,43 #158,358
    x,y,w,h =  bboxx[0], bboxx[1], bboxx[2], bboxx[3]
    #x,y,w,h = 0,0,image.shape[1],image.shape[0]
    new_w = int(w * 0.8)
    new_1x = x + new_w
    new_1y = y

    ######without dropdown
    # x1,y1,w1,h1 = 51,146,362,35  #413,181 #404,267
    # new_w1 = int(w1 * 0.8)
    # new_2x = x1 + new_w1
    # new_2y = y1
    # new_2x = new_1x + w - new_w
    # new_2y = x + w
    # new_3x = new_1x
    # new_3y = new_1y + h
    # new_4x = new_1x + w - new_w
    # new_4y = new_2y + h
    #image = cv2.rectangle(image, (new_1x,new_1y),(x+w,y+h), color, thickness)
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    ############dropdown
    # Extract the region of interest (ROI) using the bounding box
    roi = image[new_1y:y+h-10, new_1x:x+w-10]
    print("roi size", roi.shape)
    cv2.imshow("roi",roi)
    cv2.waitKey(0)
    ################### shashank #####################
    largest_island = test_drop(roi)
    print("largest_island",largest_island)
    size = roi.shape[0]*roi.shape[1]
    val = (largest_island//size)*100
    print("val",val)
    if(val<=10):
        return True
    else:
        return False


    ##################################################
'''shashank
    # roi = image[new_1y:new_1y+h, new_1x:new_1x+w]
    # Apply histogram equalization to the ROI
    equalized_roi = cv2.equalizeHist(roi)
    #equalized_roi = cv2.equalizeHist(image)
    # Normalize the pixel values within the ROI (optional)
    normalized_roi = equalized_roi.astype(float) / 255.0

    ############without dropdown
    # normal_roi = image[new_2y:y1+h,new_2x:x1+w1]
    # equalized_normal_roi = cv2.equalizeHist(normal_roi)
    # normalized_normal_roi = equalized_normal_roi.astype(float) / 255.0

    # equalized_roi = cv2.equalizeHist(normalized_roi)
    # Plot the original ROI, equalized ROI, and normalized ROI
    # plt.figure(figsize=(15, 4))
    # plt.subplot(1, 3, 1)
    # plt.title('Original ROI')
    # plt.imshow(roi, cmap='gray')

    # plt.subplot(1, 3, 2)
    # plt.title('Equalized ROI')
    # plt.imshow(equalized_roi, cmap='gray')
    # plt.figure(figsize=(5, 4))
    # plt.subplot(1, 3, 1)
    # plt.title('Normalized ROI')
    # plt.imshow(normalized_roi, cmap='gray')
    #
    # # plt.subplot(1,3,2)
    # # plt.title('Normalized_normal ROI')
    # # plt.imshow(normalized_normal_roi, cmap='gray')
    #
    # plt.tight_layout()
    # plt.show()


    # normalized_roi
    # ar = np.array(normalized_roi)
    # # get unique values and counts
    # ar_unique, i = np.unique(ar, return_counts=True)
    # # display the returned array
    # print("Unique values:", ar_unique)
    # # display the counts
    # print("Counts:", i)
    #
    # np.count_nonzero( ar== 0)
    #
    #
    # ar = np.array(normalized_normal_roi)
    # # get unique values and counts
    # ar_unique, i = np.unique(ar, return_counts=True)
    # # display the returned array
    # print("Unique values:", ar_unique)
    # # display the counts
    # print("Counts:", i)
    #
    # np.count_nonzero( ar== 0)

    threshold = 0.3

    #########normal
    # Count black and white pixels for each image
    # img1_black_pixels = (normalized_normal_roi < threshold).sum()
    # img1_white_pixels = (normalized_normal_roi >= threshold).sum()

    ######dropdown
    img2_black_pixels = (normalized_roi < threshold).sum()
    img2_white_pixels = (normalized_roi >= threshold).sum()

    # Compare pixel counts
    #print(img1_black_pixels)
    #print(img1_white_pixels)
    print(img2_black_pixels)
    print(img2_white_pixels)
    # if img1_black_pixels > img2_black_pixels:
    #     print("Image 1 has more black pixels")
    # else:
    #     print("Image 2 has more black pixels")
    val = (img2_black_pixels/img2_white_pixels) * 100
    print("val",val)
    if(val >= 30):
        return True
    else:
        return False 
    shashank '''

#print(dropdown("./test/images/img.png"))