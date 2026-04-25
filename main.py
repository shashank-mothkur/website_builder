from inference import boundingbox_images
from redundancy_check import redundancy
from extracttext import extract_ocr,calculate_iou
from edge_detect1 import edge_detection
from fill_bbox1 import fill_white_box
import copy
import os,json
import cv2
#from dropdown import dropdown


def compare_labels(data_dup, redundancy_result, label, box_val_tmp, final_label):
    val = False
    red_index_list=[]
    for j in range(0, len(data_dup[label])):
        if (redundancy_result["rectangle"][box_val_tmp][0] <= data_dup[label][j][0] and
                redundancy_result["rectangle"][box_val_tmp][1] <= data_dup[label][j][1] and
                redundancy_result["rectangle"][box_val_tmp][2] + redundancy_result["rectangle"][box_val_tmp][0] >=
                data_dup[label][j][2] + data_dup[label][j][0] and redundancy_result["rectangle"][box_val_tmp][3] +
                redundancy_result["rectangle"][box_val_tmp][1] >= data_dup[label][j][3] + data_dup[label][j][1]):
            # del(data_dup["search"][i])
            if (final_label not in data_dup):
                data_dup[final_label] = [redundancy_result["rectangle"][box_val_tmp]]
            else:
                data_dup[final_label].append(redundancy_result["rectangle"][box_val_tmp])
            # print(redundancy_result["rectangle"])
            # print(data_dup
            val = True

            red_index=redundancy_result["rectangle"][box_val_tmp]
            if red_index in red_index_list:
                continue
            else:
                red_index_list.append(red_index)
                index = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val_tmp])
                del (data_dup["rectangle"][index])
                #if(label == "search"):
                #    del(data_dup["search"][index])



    return  val

def layer2(imagepath):
    #imagepath = "test/images/7-Sketch_jpg.rf.6cb2756540e69bdd91414a88022adff5.jpg"
    image = cv2.imread(imagepath)
    #image = cv2.resize(image,(400,400))
    #cv2.imwrite("./rezise_image/resize_image.png",image)
    #imagepath = "./rezise_image/resize_image.png"
    #image1 = edge_detection(image)
    #cv2.imshow("image1",image)
    #cv2.waitKey(0)
    bb_results = boundingbox_images(image)
    redundancy_result = redundancy(bb_results,image)
    print("redundancy_result", redundancy_result)
    ocr_output = extract_ocr(imagepath)
    data_dup = copy.deepcopy(redundancy_result)
    redundancy_result_copy = copy.deepcopy(redundancy_result)
    data={}
    try:
        if("icon" in redundancy_result_copy ):

            for box_val in range(0, len(redundancy_result_copy["icon"])):
                for index in ocr_output:
                    iou = calculate_iou(redundancy_result["icon"][box_val][0:4],index["bbox"])
                    print(iou)
                    if(iou > 0.1):
                        #index = data_dup["icon"].index(redundancy_result["icon"][box_val])
                        del (data_dup["icon"][box_val])
                        del (redundancy_result["icon"][box_val])


    except Exception as e:
        print("error while deleting icons in ocr detection",e)

    try:
        if("square" in redundancy_result_copy):
            for box_val in range(0, len(redundancy_result_copy["square"])):
                if(abs(redundancy_result["square"][box_val][2]-redundancy_result["square"][box_val][3])>20):
                    if("rectangle" not in redundancy_result):
                        redundancy_result["rectangle"] = [redundancy_result["rectangle"][box_val]]
                        data_dup["rectangle"] = [data_dup["rectangle"][box_val]]

                    else:
                        redundancy_result["rectangle"].append(redundancy_result["rectangle"][box_val])
                        data_dup["rectangle"].append(data_dup["rectangle"][box_val])
                    del(redundancy_result["square"][box_val])
                    del(data_dup["square"][box_val])
    except Exception as e:
        print("error while wrong square", e)

    print("after square deletion",redundancy_result)
    print("after square deletion",data_dup)
    if("rectangle" in redundancy_result):

        button_index_list = []
        for box_val in range(0,len(redundancy_result["rectangle"])):
            print("start_rec",redundancy_result["rectangle"][box_val])
            if("arrow" in data_dup):
                val = compare_labels(data_dup,redundancy_result,"arrow", box_val, "card")
                if val == True:
                    continue

                '''for i in range(0,len(data_dup["arrow"])):
                    if(box_val[0]<= i[0] and box_val[1]<=i[1] and box_val[2]>=i[2] and box_val[3]>=i[3]):
                        #del(data_dup["arrow"][i])
                        if("card" not in data_dup):
                            data_dup["card"] = redundancy_result["rectangle"][box_val]
                        else:
                            data_dup["card"].append(redundancy_result["rectangle"][box_val])

                        del(data_dup["rectangle"][box_val])
                        break'''
            if("icon" in data_dup):
                try:
                    val = compare_labels(data_dup,redundancy_result,"icon", box_val,  "card")
                    if val == True:
                        continue
                except Exception as e:
                    print("error in icon",e)

            if ("search" in data_dup):
                try:
                    val = compare_labels(data_dup,redundancy_result,"search",box_val,"search_bar")
                    if val == True:
                        continue
                except Exception as e:
                    print("error in search",e)
            if ("dropdown" in data_dup):
                try:
                    val = compare_labels(data_dup,redundancy_result,"dropdown",box_val,"drop_down")
                    if val == True:
                        continue
                except Exception as e:
                    print("error in drop_down",e)


            if("search_bar" not in data_dup):
                try:
                    for index in ocr_output:
                        if (index["word"].lower() == "search"):
                            if (redundancy_result["rectangle"][box_val][0] <= index["bbox"][0] and redundancy_result["rectangle"][box_val][1] <= index["bbox"][1] and redundancy_result["rectangle"][box_val][2]+redundancy_result["rectangle"][box_val][0]  >= index["bbox"][2]+index["bbox"][0]  and redundancy_result["rectangle"][box_val][3] + redundancy_result["rectangle"][box_val][1] >= index["bbox"][3]+ index["bbox"][1]):

                                if ("search_bar" not in data_dup):
                                    data_dup["search_bar"] = [redundancy_result["rectangle"][box_val]]
                                else:
                                    data_dup["search_bar"].append(redundancy_result["rectangle"][box_val])
                                # print(redundancy_result["rectangle"])
                                # print(data_dup["rectangle"])
                                index = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                                del (data_dup["rectangle"][index])
                                break
                except Exception as e:
                    print("error in search bar ",e)

            try:
                flag = 1

                for index in ocr_output:
                    if (index["word"] == "<" or index["word"][0] == "<"):
                        print("index")
                        if (redundancy_result["rectangle"][box_val][0] <= index["bbox"][0] and redundancy_result["rectangle"][box_val][1] <= index["bbox"][1] and redundancy_result["rectangle"][box_val][2] + redundancy_result["rectangle"][box_val][0] >= index["bbox"][2] + index["bbox"][0] and redundancy_result["rectangle"][box_val][3] + redundancy_result["rectangle"][box_val][1] >= index["bbox"][3] + index["bbox"][1]):
                            print("yes")
                            for index1 in ocr_output:
                                if (index1["word"] == ">" or index["word"][-1]== ">"):
                                    if (redundancy_result["rectangle"][box_val][0] <= index1["bbox"][0] and redundancy_result["rectangle"][box_val][1] <= index1["bbox"][1] and redundancy_result["rectangle"][box_val][2] + redundancy_result["rectangle"][box_val][0] >= index1["bbox"][2] + index1["bbox"][0] and redundancy_result["rectangle"][box_val][3] + redundancy_result["rectangle"][box_val][1] >= index1["bbox"][3] + index1["bbox"][1]):
                                        print("no")
                                        print("rectangle",redundancy_result["rectangle"][box_val])
                                        print("<",index["bbox"])
                                        print(">",index1["bbox"])
                                        flag=0
                                        if ("text_box" not in data_dup):
                                            data_dup["text_box"] = [redundancy_result["rectangle"][box_val]]
                                        else:
                                            data_dup["text_box"].append(redundancy_result["rectangle"][box_val])
                                        # print(redundancy_result["rectangle"])
                                        # print(data_dup["rectangle"])
                                        ind = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                                        del (data_dup["rectangle"][ind])
                                        break
                        elif( "<" in index["word"] and ">" in index["word"]):
                            if (redundancy_result["rectangle"][box_val][0] <= index["bbox"][0] and redundancy_result["rectangle"][box_val][1] <= index["bbox"][1] and redundancy_result["rectangle"][box_val][2] + redundancy_result["rectangle"][box_val][0] >= index["bbox"][2] + index["bbox"][0] and redundancy_result["rectangle"][box_val][3] + redundancy_result["rectangle"][box_val][1] >= index["bbox"][3] + index["bbox"][1]):
                                flag = 0
                                print("rectangle", redundancy_result["rectangle"][box_val])
                                print("ocr output", index["word"])
                                print("ocr output box",index["bbox"])
                                if ("text_box" not in data_dup):
                                    data_dup["text_box"] = [redundancy_result["rectangle"][box_val]]
                                else:
                                    data_dup["text_box"].append(redundancy_result["rectangle"][box_val])
                                # print(redundancy_result["rectangle"])
                                # print(data_dup["rectangle"])
                                ind = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                                del (data_dup["rectangle"][ind])
                                break


                print(flag)
                if flag==1:
                    try:
                        image1 = cv2.imread(imagepath)

                        for index in ocr_output:
                            if (redundancy_result["rectangle"][box_val][0] <= index["bbox"][0] and
                                    redundancy_result["rectangle"][box_val][1] <= index["bbox"][1] and
                                    redundancy_result["rectangle"][box_val][2] +
                                    redundancy_result["rectangle"][box_val][0] >= index["bbox"][2] + index["bbox"][
                                        0] and redundancy_result["rectangle"][box_val][3] +
                                    redundancy_result["rectangle"][box_val][1] >= index["bbox"][3] + index["bbox"][1]):
                                image1[index['bbox'][1]:index['bbox'][1]+index['bbox'][3],index['bbox'][0]:index['bbox'][0]+index['bbox'][2]] = (255, 255, 255)
                                cv2.imwrite("./saved_images/crop.jpg",image1)
                                #cv2.imshow()
                                #cv2.waitKey(0)
                        #image2 = image1[redundancy_result["rectangle"][box_val][1]:redundancy_result["rectangle"][box_val][1]+redundancy_result["rectangle"][box_val][3],redundancy_result["rectangle"][box_val][0]:redundancy_result["rectangle"][box_val][0]+redundancy_result["rectangle"][box_val][2]]
                        #value = dropdown(imagepath,redundancy_result["rectangle"][box_val])
                        '''value = dropdown(image1,redundancy_result["rectangle"][box_val])
                        if value == True:
                            if ("dropdown" not in data_dup):
                                data_dup["dropdown"] = [redundancy_result["rectangle"][box_val]]
                            else:
                                data_dup["dropdown"].append(redundancy_result["rectangle"][box_val])
                            ind = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                            del (data_dup["rectangle"][ind])
                            continue'''
                    except Exception as e:
                        print("error in dropdown",e)

                    for index in ocr_output:
                        if(index["word"].lower() != "search"):
                            if (redundancy_result["rectangle"][box_val][0] <= index["bbox"][0] and redundancy_result["rectangle"][box_val][1] <= index["bbox"][1] and redundancy_result["rectangle"][box_val][2] + redundancy_result["rectangle"][box_val][0] >= index["bbox"][2] + index["bbox"][0] and redundancy_result["rectangle"][box_val][3] + redundancy_result["rectangle"][box_val][1] >= index["bbox"][3] + index["bbox"][1]):

                                if ("button" not in data_dup):
                                    data_dup["button"] = [redundancy_result["rectangle"][box_val]]
                                else:
                                    data_dup["button"].append(redundancy_result["rectangle"][box_val])

                                red_index = redundancy_result["rectangle"][box_val]
                                if red_index in button_index_list:
                                    continue
                                else:
                                    button_index_list.append(red_index)
                                    index = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                                    del (data_dup["rectangle"][index])
                                    break
                    # print(redundancy_result["rectangle"])
                    # print(data_dup["rectangle"])
                    #ind = data_dup["rectangle"].index(redundancy_result["rectangle"][box_val])
                    #del (data_dup["rectangle"][ind])
                    #break
            except Exception as e:
                print("error in button and textbox",e)
                #for box_val in range(0, len(redundancy_result["rectangle"])):
            try:
                #### remaining rectangles into cards
                print(redundancy_result['rectangle'][box_val])
                ind = data_dup['rectangle'].index(redundancy_result['rectangle'][box_val])
                if "card" in data_dup:
                    data_dup['card'].append(data_dup['rectangle'][ind])
                else:
                    data_dup['card']=[data_dup['rectangle'][ind]]
            except Exception as e:
                print("error in empty rectangles",e)
    print(data_dup)
    try:
        if("square" in redundancy_result):

            for box_val in range(0, len(redundancy_result["square"])):

                flag = 0
                for index in ocr_output:
                    if (redundancy_result["square"][box_val][0] <= index["bbox"][0] and redundancy_result["square"][box_val][1] <= index["bbox"][1] and redundancy_result["square"][box_val][2] + redundancy_result["square"][box_val][0] >= index["bbox"][2] + index["bbox"][0] and redundancy_result["square"][box_val][3] + redundancy_result["square"][box_val][1] >= index["bbox"][3] + index["bbox"][1]):
                        if ("button" not in data_dup):
                            data_dup["button"] = [redundancy_result["square"][box_val]]
                        else:
                            data_dup["button"].append(redundancy_result["square"][box_val])

                        index = data_dup["square"].index(redundancy_result["square"][box_val])
                        del (data_dup["square"][index])
                        flag = 1
                        break
                    elif(len(index["word"])>1):
                        #print(index["word"])
                        #print(redundancy_result["square"][box_val])
                        #print(index["bbox"])
                        print(data_dup)
                        if(abs(redundancy_result["square"][box_val][1]-index["bbox"][1])<=80 and abs((redundancy_result["square"][box_val][1]+redundancy_result["square"][box_val][3])-(index["bbox"][1]+index["bbox"][3]))<=80):

                            if("check_box" not in data_dup):
                                data_dup["check_box"] = [redundancy_result["square"][box_val]]
                            else:
                                data_dup["check_box"].append(redundancy_result["square"][box_val])
                            print(redundancy_result["square"])
                            print(data_dup["square"])
                            #if(redundancy_result["square"][box_val] in data_dup):
                            indexx = data_dup["square"].index(redundancy_result["square"][box_val])
                            del(data_dup["square"][indexx])
                            flag = 1
                            break
                if(flag == 0):
                    try:
                        #### remaining rectangles into cards
                        print(redundancy_result['square'][box_val])
                        ind = data_dup['square'].index(redundancy_result['square'][box_val])
                        if "card" in data_dup:
                            data_dup['card'].append(data_dup['square'][ind])
                        else:
                            data_dup['card']=[data_dup['square'][ind]]
                    except Exception as e:
                        print("error in empty square",e)
        print(data_dup)
    except Exception as e:
        print("error in square",e)



    if("rectangle" in data_dup):
        #if (len(data_dup["rectangle"]) == 0):
        del (data_dup["rectangle"])

    if("square" in data_dup):
        #if (len(data_dup["square"]) == 0):
        del (data_dup["square"])

    final_result={}
    final_result['uicontrol']=data_dup
    final_result['text']=ocr_output
    #print("final_result",final_result)
    return final_result


dir = "./test/images"
#dir = "./checkbox_folder"
'''images = os.listdir(dir)
c=0
for i in images:
    print(i)
    result = layer2(dir+"/"+i)
    print("final_result", result)
    #with open("./final_output/"+i+".json", "w") as outfile:
    #    json.dump(result, outfile)
    image = cv2.imread(dir+"/"+i)
    #image = cv2.resize(image,(400,400))
    #cv2.imshow("Image",image)
    for k in result["uicontrol"]:
        for j in result["uicontrol"][k]:
            cv2.rectangle(image,(j[0],j[1]),(j[2]+j[0],j[3]+j[1]),(0, 255, 0), 2)
            img = cv2.putText(image, k , (int(j[0]), int(j[1]) - 3),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imwrite("./saved_images/save"+str(c)+".jpg",image)
    c=c+1
    #cv2.imshow("image", image)
    #cv2.waitKey(0)'''
i = "img_13.png"
result = layer2(dir+"/"+i)
img = cv2.imread(dir+"/"+i)
edge_detection(img)
#with open("./final_output/"+i+".json", "w") as outfile:
#    json.dump(result, outfile)
#image = cv2.imread(dir+"/"+i)
image= cv2.imread("./saved_images/save_edge.jpg")
#image = cv2.resize(image,(400,400))
#cv2.imshow("Image",image)
print("results",result)
image2 = fill_white_box(image,result)
cv2.imwrite("./saved_images/save_white.jpg",image2)
for i in result['text']:
    j = i["bbox"]
    cv2.rectangle(image, (j[0], j[1]), (j[2] + j[0], j[3] + j[1]), (0, 255, 0), 2)
    cv2.putText(image, i["word"], (int(j[0]), int(j[1]) - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
for k in result["uicontrol"]:
    for j in result["uicontrol"][k]:
        cv2.rectangle(image,(j[0],j[1]),(j[2]+j[0],j[3]+j[1]),(0, 255, 0), 2)
        img = cv2.putText(image, k , (int(j[0]), int(j[1]) - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

cv2.imwrite("./saved_images/save.jpg",image)
#cv2.imshow("image", image)
#cv2.waitKey(0)'''




















