import cv2
import math

src = cv2.imread('canvasInput')
dst = cv2.math.zeros(src.rows, src.cols, cv.CV_8UC3)
lines = cv2.math()
color = cv2.Scalar(255, 0, 0)
cv2.cvtColor(src, src, cv2.COLOR_RGBA2GRAY, 0)
cv2.Canny(src, src, 50, 200, 3)

cv2.HoughLinesP(src, lines, 1, math.PI / 180, 2, 0, 10)

for i in range(0,len(lines.rows)):
    startPoint = cv2.circle(lines.data32S[i * 4], lines.data32S[i * 4 + 1])
    endPoint = cv2.circle(lines.data32S[i * 4 + 2], lines.data32S[i * 4 + 3])
    cv2.line(dst, startPoint, endPoint, color)

cv2.imshow('canvasOutput', dst)
#src.delete(); dst.delete()
#lines.delete()