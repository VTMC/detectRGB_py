import cv2

path = "D:/github_project/detectRGB_py/TestImage/Boditolk_20260916_082915.jpg"

#read image 
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"이미지를 불러오지 못했습니다: {path}")

#change Gray
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def changeThreshold(thresholdValue):
    ret, binaryImg = cv2.threshold(
        grayImg,
        thresholdValue,
        255,
        cv2.THRESH_BINARY
    )
    
    cv2.imshow(windowName, binaryImg)

#make Window
windowName = "RESULT"

# 창을 먼저 생성
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

changeThreshold(127)

#Threshold 조절 바 생성
cv2.createTrackbar(
    "Threshold",    #트랙 바 이름
    windowName,     #트랙 바 윈도우 창 이름
    127,            #초기값
    255,            #최댓값
    changeThreshold #콜백 함수  
)

cv2.waitKey(0)
cv2.destroyAllWindows()