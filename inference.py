from ultralytics import YOLO
import cv2
import json
import numpy as np
import torch

model = YOLO(r"C:\Users\NHi560\Desktop\Projects\site_builder\site_builder_29_09\best_3.pt")
def detect_triangle(image_obj):

    #image_obj = cv2.imread('image.jpg')

    gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((4, 4), np.uint8)
    dilation = cv2.dilate(gray, kernel, iterations=1)

    #blur = cv2.GaussianBlur(dilation, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 30)
    #edges = cv2.Canny(thresh, 25, 175, apertureSize=3)
    cv2.imwrite("result_edges.png", edges)
    # Now finding Contours         ###################
    contours,_ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coordinates = []
    for cnt in contours:
        # [point_x, point_y, width, height] = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(
            cnt, 0.07 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            coordinates.append([cnt])
            cv2.drawContours(image_obj, [cnt], 0, (0, 0, 255), 3)

    cv2.imwrite("result.png", image_obj)
    cv2.waitKey(0)
    return coordinates

def boundingbox_images(image):
    #image_link = "test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg"
    #image = cv2.imread(image_link)
    #image = cv2.resize(image,(400,400))
    results = model.predict(source=image, save=True)
    names = model.names
    print(names)
    results_json = {"boxes": results[0].boxes.xyxy.tolist(), "Classes": results[0].boxes.cls.tolist(),
                    "scores": results[0].boxes.conf.tolist()}\

    result_json_last =  {}

    for i in range(0, len(results_json["boxes"])):
        bbox = results_json["boxes"][i]
        name = names[results_json["Classes"][i]]
        if(name not in result_json_last):

            result_json_last[name] = [[int(bbox[0]),int(bbox[1]),int(bbox[2]-bbox[0]),int(bbox[3]-bbox[1])]]
        else:
            result_json_last[name].append([int(bbox[0]),int(bbox[1]),int(bbox[2]-bbox[0]),int(bbox[3]-bbox[1])])

    #print(detect_triangle(image))
    '''with open("./bb_output/"+image_link[12:]+".json", "w") as outfile:
        json.dump(result_json_last, outfile)'''


    '''for result in results_json:
        boxes = result.boxes
        result_json[result.cls]
        for box in boxes:
            # Extract box coordinates and class
            b = box.xyxy[0].cpu().numpy()
            c = int(box.cls[0].cpu().numpy())
            class_label = result.names[c]

            b = b.astype(int)

            cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
            cv2.putText(image, class_label, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("image",image)
    cv2.waitKey(0)'''
    return result_json_last

#print(boundingbox_images("test/images/image123.png"))
