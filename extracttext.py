import requests
import re
import os
import json
import cv2

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
    union_area = area1 + area2 - intersection_area

    # Calculate IOU
    iou = intersection_area / union_area

    return iou


def call_cv_text(image_path):
    url = "https://carnivalsb.nslhub.com/cv"

    payload = {'serviceType': 'text',
               'trans_id': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI4TU1aaFRvM1Q1WXFxRkpiQ2phbFozYU91dG5wUEJ3bEVRWHNTZWEyZEZJIn0.eyJleHAiOjE2OTQxMDcwOTAsImlhdCI6MTY5NDEwNTI5MCwianRpIjoiNTEyYTgzOWEtYzFhNS00MDUxLThjNmQtYTY4ZjYwZWI2ZGIzIiwiaXNzIjoiaHR0cHM6Ly9wcmVxYWlhbS5uc2xodWIuY29tL3JlYWxtcy9jdnByZXFhIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImM3YmI0MjcyLWU0YjctNDA3Ni1hYmViLWRlOTNlYzkwMmRkMSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImN2cHJlcWEiLCJzZXNzaW9uX3N0YXRlIjoiN2QzNTc3OWMtZGMxYy00NTAzLTg4ZmEtNDE4YTgwNGM2MDIzIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMtY3ZwcmVxYSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI3ZDM1Nzc5Yy1kYzFjLTQ1MDMtODhmYS00MThhODA0YzYwMjMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJTcmF2YW4gQ2giLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzcmF2YW4iLCJnaXZlbl9uYW1lIjoiU3JhdmFuIiwiZmFtaWx5X25hbWUiOiJDaCIsImVtYWlsIjoic3JhdmFuLmNob2trYXB1QG5zbGh1Yi5jb20ifQ.Lf23TGn0jcp3DBXiywR5Z2aCGPWDz6SQF6ud5CA9jis5wLIawUmwAy-8EwWDRgUbu3x_HMJL8vOfGLSlsLoyDLWeE7HvHXA4XolJrx6zG82w_AYVqeWqRIDKcCw5lqxY87WbSQ3lv-hiEutedNkOqKcuW7AI83yi5YxvDQy8aMvAnwlIXtXLv2ppd-2scWe2buI7TQRY7qHs2MDdxOX6-Te8vscOiuSQ96m0hJgvgzm6h3aTvt9WU1Kl-GTnkyyuL9PX8UuYUPjphxQ2wa0sMOD8BdL74P591kslo2X1O3CLTjO1pkg7X2-AC461w9-HSU_catumnkKc_ts0nuiKhQ'}
    files = [
        ('file', (
        'name_test_afollowup_2.JPG', open(image_path, 'rb'),
        'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.json())
    return response.json()

def width_height(text_and_boxes):
    for item in text_and_boxes:
        item['bbox'][2] = item['bbox'][2] - item['bbox'][0]
        item['bbox'][3] = item['bbox'][3] - item['bbox'][1]

    return text_and_boxes





def extract_ocr(image_path):
    #dir = "./test/images"
    #saving_dir = "./text_detect4"
    #images = os.listdir(dir)
    image = ""
    pattern = r'^0.*'
    pattern2 = r'[^\w\s]'

    #for image in images:
    #image_path = dir + "/" + image
    #saving_img = saving_dir + "/" + image
    result = call_cv_text(image_path)
    #print(result)
    #print("####")
    # Delete the first bounding box
    #if text_and_boxes:
    #    del text_and_boxes[0]
    text_and_boxes = []
    for textb in result["result"]:
        if textb == "text_0" or textb[:4] != "text" or (result["result"][textb]["transcription"].isalpha() and len(result["result"][textb]["transcription"]) <= 2) or re.match(pattern, result["result"][textb]["transcription"]):
            continue
        temp = {}
        temp["word"] = result["result"][textb]["transcription"]
        temp["bbox"] = [result["result"][textb]["xmin"], result["result"][textb]["ymin"], result["result"][textb]["xmax"],result["result"][textb]["ymax"]]
        text_and_boxes.append(temp.copy())
    # Process and save the image in the output folder
    #processed_image_path = os.path.join(output_folder, filename)
    img = cv2.imread(image_path)


    iou_results = []

    boxes_texts= width_height(text_and_boxes)
    # print(boxes_texts)

    i = 0
    while i < len(boxes_texts):
        j = i + 1
        while j < len(boxes_texts):
            box1 = boxes_texts[i]['bbox']
            box2 = boxes_texts[j]['bbox']
            iou = calculate_iou(box1, box2)
            iou_results.append({'pair': (boxes_texts[i]['word'], boxes_texts[j]['word']), 'iou': iou})

            # If IoU is equal to 1, remove one of the boxes
            if iou >= 0.5:
                del boxes_texts[j]
            else:
                j += 1

        i += 1

    #print(iou_results)

    for item in boxes_texts:

        top_left = (item['bbox'][0],item['bbox'][1])
        bottom_right = (item['bbox'][2]+item['bbox'][0],item['bbox'][3]+item['bbox'][1])
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
        cv2.putText(img, item["word"], ((int(item['bbox'][0]), int(item['bbox'][3]+item['bbox'][1]) + 10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),3,cv2.LINE_AA)
        #print("text", item['text'])
    #print("Bounding Box:", item['bounding_box'])
    #print()
    #cv2.imwrite(saving_img, img)

    print("TEXT and Bounding Box",boxes_texts)

    for i in boxes_texts:
        j = i["bbox"]
        cv2.rectangle(img,(j[0],j[1]),(j[2]+j[0],j[3]+j[1]),(0, 255, 0), 2)
        cv2.putText(img, i["word"] , (int(j[0]), int(j[1]) - 3),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite("./saved_images/save_ocr.jpg",img)
    #cv2.imshow("image",img)
    #cv2.waitKey(0)
    return boxes_texts


# for result in iou_results:
#     pair = result['pair']
#     iou = result['iou']
#     intersection = result['intersection']
#     print(f"IoU between {pair} is {iou:.4f}")

    
# [19, 90, 71, 110] --- [19,90,w = [2]-[0], h = [3]-[1]]
#print(extract_ocr("test/images/img_1.png"))