import os
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label
import cv2


def boxes(img):
    #img = ImageOps.grayscale(orig)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im = np.array(gray_image)

    # Inner morphological gradient.
    im = morphology.grey_dilation(im, (3, 3)) - im

    # Binarize.
    mean, std = im.mean(), im.std()
    t = mean + std
    im[im < t] = 0
    im[im >= t] = 1

    # Connected components.
    lbl, numcc = label(im)
    # Size threshold.

    min_size = 200
    # #min_size = 1000
    # print(min_size)

    box_list = []
    for i in range(1, numcc + 1):
        py, px = np.nonzero(lbl == i)
        if len(py) < min_size:
            im[lbl == i] = 0
            continue
        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        # Four corners and centroid.
        box_list.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (np.mean(px), np.mean(py))])

    return im.astype(np.uint8) * 255, box_list


def check_mainframe(box_list):
    curr_area_list = 0
    for i in range(len(box_list)):
        xmin = box_list[i][0][0][0]
        xmax = box_list[i][0][1][0]

        ymin = box_list[i][0][0][1]
        ymax = box_list[i][0][2][1]

        print(xmin, xmax, ymin, ymax)

        width = xmax - xmin
        height = ymax - ymin

        area = width * height
        if area >= curr_area_list:
            curr_area_list = area
            coords = [xmin, ymin, xmax, ymax]
    # print("maximum area:", max(area_list))
    return coords, area


