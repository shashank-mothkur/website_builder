import cv2
image = cv2.imread('saved_images/save_r.jpg')
#image = cv2.imread("test/images/2-Sketch.jpg")
#image = cv2.imread('test/images/img_1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
cv2.imshow("binary",binary_image)
cv2.waitKey(0)
#h,w = binary_image.shape[:2]
x1,y1,w,h= 216, 222, 1620, 2120
binary_image = binary_image[y1:y1+h,x1:x1+w]
#x1,y1=0,0
#h,w = binary_image.shape[:2]
'''res = []
for i in range(0,h):
    c=0
    k=0
    temp= 0
    flag = 0
    for j in range(0,30):
        if(crop_img[i][j]== 0):
            c = c + 1
            #temp.append(i)
            if (flag == 0):
                temp=i
                flag=1

        else:
            for t in range(i-5,i+5):
                if (i >=0  and i<=h-5):
                    if(crop_img[t][j]== 0):
                        c=c+1
                        #temp.append(t)
                        break

    for b in range(w-30,w):
        for t in range(i - 5, i + 5):
            if(i>=5 and i<=h-5):
                if(crop_img[t][b]== 0):
                    k=k+1
                    break
    print("temp",temp)
    if(c>=14 and  k>= 14):
        res.append(temp)
        print("result",res)

print("res",res)
final_res = [res[0]]
for i in range(0,len(res)-1):
    if(abs(res[i]-res[i+1])>=5):
        final_res.append(res[i+1])

print(final_res)
del(final_res[0])
#del(final_res[len(final_res)-1])
for i in range(0,len(final_res)):
    final_res[i]= final_res[i]+5

print("final_res",final_res)
for i in final_res:
    cv2.rectangle(image,(0,i),(w,i),(0,255,0),1)

cv2.imshow("image",image)
cv2.waitKey(0)'''

#####################################################################
final_temp=[]
for i in range(0,h):
    flag = 0
    c=0
    k=0
    white=0
    temp=0

    for p in range(0,50):
        if(binary_image[i][p]==255):
            white= white+1
    if(white>40):
        continue
    for j in range(0,50):
        if (binary_image[i][j] == 0):
            c = c + 1
            temp=i
        else:
            if(i<=10):
                for t in range(0,i+10):
                    if (binary_image[t][j] == 0):
                        c = c + 1
                        break
            elif(i>=h-10):
                for t in range(i,h):
                    if (binary_image[t][j] == 0):
                        c = c + 1
                        break
            else:
                for t in range(i-10,i+10):
                    if (binary_image[t][j] == 0):
                        c = c + 1
                        break

    for b in range(w - 50, w):
        if (binary_image[i][j] == 0):
            k = k + 1
            # temp.append(i)
        else:
            if (i <= 10):
                for t in range(0, i + 10):
                    if (binary_image[t][j] == 0):
                        k = k + 1
                        break
            elif (i >= h - 10):
                for t in range(i, h):
                    if (binary_image[t][j] == 0):
                        k = k + 1
                        break
            else:
                for t in range(i - 10, i + 10):
                    if (binary_image[t][j] == 0):
                        k = k + 1
                        break
    print("i",i)
    print("temp",temp)
    print("c",c)
    print("k",k)
    if(c>=30 and k>=30):
        final_temp.append(temp)
print("final_temp",final_temp)
if(len(final_temp) !=0):
    final = [final_temp[0]]
    for i in range(0,len(final_temp)-1):
        if (abs(final_temp[i] - final_temp[i + 1]) >= 10):
            final.append(final_temp[i + 1])
    print(final)
    for i in final:
        cv2.rectangle(image,(x1,i+y1),(w+x1,i+y1),(0,255,0),1)

    #cv2.imshow("image",image)
    cv2.imwrite("./saved_images/save_final_hori.jpg",image)
    #cv2.waitKey(0)
else:
    print("no horiozontal lines")


