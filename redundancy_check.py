import json, math
import os, copy
from mainframe import check_mainframe
from mainframe import boxes
from PIL import Image, ImageOps, ImageDraw

# Open the JSON file
files = os.listdir('./bb_output')

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return int(distance)

def calculate_iou(box1, box2):
    # box1 and box2 should be in the format (x, y, w, h)

    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Calculate the coordinates of the intersection rectangle
    x_intersection = max(x1, x2)
    y_intersection = max(y1, y2)
    w_intersection = min(x1 + w1, x2 + w2) - x_intersection
    h_intersection = min(y1 + h1, y2 + h2) - y_intersection

    # If there is no intersection, return 0
    if w_intersection <= 0 or h_intersection <= 0:
        return 0.0

    # Calculate the area of intersection
    intersection_area = w_intersection * h_intersection

    # Calculate the area of the union
    area1 = w1 * h1
    area2 = w2 * h2
    union_area = area1 if area1 > area2 else area2
    # Calculate IOU
    iou = intersection_area / union_area

    return iou
def redundancy(bb_results,image):
    all_data_finals = []
    #for file in files:
    #if '.json' in file:
    #file = './bb_output/' + file
    final_main = []
    #with open(file) as json_file:
    # Load the data from the file
    #data = json.load(json_file)
    data = bb_results
    for e in data:
        for f in data[e]:
            m = f[2] - f[0]
            n = f[3] - f[1]
            f.append(f[2]*f[3])  ## area
            f.append(f[0] + int(f[2] / 2))  ##centroid x
            f.append(f[1] + int(f[3] / 2))  ##centriod y
    if('mainframe' in data):
        if len(data['mainframe']) > 1:

            area_prev = 0
            for f in data['mainframe']:
                x1, y1, w1, h1, area, x_g, y_g = f
                ##area=w1*h1
                if area > area_prev:
                    area_prev = area
                    final_main = [f]
        else:
            final_main = data['mainframe']
    data['mainframe'] = final_main

    mainframe = data.pop('mainframe')
    data_dup = copy.deepcopy(data)
    data_final = copy.deepcopy(data)
    for e in data:
        for f in data_dup:
            for j in data[e]:
                for k in data_dup[f]:
                    x1, y1, w1, h1, a1, x_g1, y_g1 = j
                    x2, y2, w2, h2, a2, x_g2, y_g2 = k
                    cg_dist = calculate_distance(x_g1, y_g1, x_g2, y_g2)

                    if cg_dist <= 30 and cg_dist > 0:
                        iou_dist = calculate_iou([x1, y1, w1, h1], [x2, y2, w2, h2])
                        if iou_dist > 0.6:
                            if a1 < a2:
                                data_final[e] = [lst for lst in data_final[e] if lst != j]
                                # del data_final[e][j]
                            else:
                                data_final[f] = [lst for lst in data_final[f] if lst != k]
                                # del data_final[f][k]
    if (mainframe is None or len(mainframe) == 0):
        #input_path = os.path.join(imagepath)  ##change

        im, box_list = boxes(image)
        # print(box_list)
        # print()
        coords, area = check_mainframe(box_list)
        data_final['mainframe'] = [coords]
    else:
        data_final['mainframe'] = mainframe
    #file_path = file.split(".json")[0] + "1.json"
    #with open(file_path, "w") as json_file:
    #    json.dump(data_final, json_file)
    print(data_final)
    all_data_finals.append(data_final)
    print(all_data_finals)
    return data_final

# Access the values
# name = data['name']
# age = data['age']
# city = data['city']

# import cv2
# img = cv2.imread(r"C:\Users\NHI556\Documents\rsltimg2\IMG-0119.jpg")
# coords=[]
# for text in data_final:
#     print(text)
#     for j in range(len(data_final[text])):
#         print(type(data_final[text][j][0]))
#         x1,y1,x2,y2 = data_final[text][j][0],data_final[text][j][1],data_final[text][j][2],data_final[text][j][3]
#         coords.append([x1,y1,x2,y2])
# print(coords)
# for box in coords:
#     x1,y1,w,h   = box
#     x2, y2 = x1+w, y1+h
#     img = cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255),3)
# path = r"C:\Users\NHI556\Documents\rsltimg2\IMG-0119-out.jpg"
# cv2.imwrite(path,img)
