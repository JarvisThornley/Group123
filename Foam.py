import cv2
import numpy as np

#img = cv2.imread("image.png")

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    img = frame

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")

def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #_, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
    _, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
    #img_blur = cv2.GaussianBlur(thresh, (5, 5), 2)
    #img_canny = cv2.Canny(img_blur, 0, 0)
    #return img_canny
    return thresh

def get_contours(img):
    contours, _ = cv2.findContours(process(img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    r1, r2 = sorted(contours, key=cv2.contourArea)[-3:-1]
    x, y, w, h = cv2.boundingRect(np.r_[r1, r2])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

#get_contours(img)

pro_img = process(img)

cv2.imshow("img_processed", pro_img)
dims = pro_img.shape
print(dims)
cv2.waitKey(0)
