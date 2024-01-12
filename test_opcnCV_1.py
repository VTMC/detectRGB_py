import cv2
# import rawpy as rp


# path = "E:/VTMC_GitHub/StoredProject_LibRaw_0.21.2/StoredProject_LibRaw_0.21.2/LibRaw-0.21.2/testFile/test_A80_whiteBalanced.tiff"
path = "C:/Users/owner/Downloads/Send Anywhere (2024-01-08 14-48-11)/RAW_2024-01-08-14-46-20-093.dng.tiff"

# read image
img = cv2.imread(path)

# # change img to gray
# grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # threshold
# ret, thresholdImg = cv2.threshold(grayImg, 150, 255, cv2.THRESH_BINARY)
# thresholdImg = cv2.bitwise_not(thresholdImg)

# # findContours
# contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# # drawContours
# for i in range(len(contours)):
#     cv2.drawContours(img, [contours[i]], 0, (0, 0, 255), 2)
#     print(i, hierarchy[0][i])

# revise value
x_plus = 100
# x_plus = 0

# draw Rectangle
x = 909
y = 1149
w = 1165
h = 1686

# x = x + (x_plus/2 - 1)
x = x + x_plus
w = w - x_plus*2

cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

# resize img
# dst = cv2.resize(thresholdImg, dsize=(480, 640), interpolation=cv2.INTER_AREA)
dst = cv2.resize(img, dsize=(480, 640), interpolation=cv2.INTER_AREA)

# show image
cv2.imshow("RESULT", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()