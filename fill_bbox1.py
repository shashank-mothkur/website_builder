import cv2

# Reading the input image
#image = cv2.imread('./images1/IMG-0123.jpg')

def fill_white_box(image,result):

    # Bounding box coordinates (xmin, ymin, xmax, ymax)
    #xmin, ymin, xmax, ymax = 100, 150, 500, 600
    for key1 in result['uicontrol']:
        if(key1 != "mainframe"):
            for box in result['uicontrol'][key1]:
                # Adding a filled white rectangle to the image
                cv2.rectangle(image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 255, 255), -1)
    for i in result['text']:
        box = i["bbox"]
        cv2.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 255, 255), -1)



    # Display the modified image
    #cv2.imshow('Modified Image', image)
    cv2.imwrite("./saved_images/save_r.jpg", image)

    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image
