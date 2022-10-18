import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    _, thresh = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY)#235 thresh at HAL
    #img_blur = cv2.GaussianBlur(thresh, (5, 5), 2)
    #img_canny = cv2.Canny(img_blur, 0, 0)
    #return img_canny
    return thresh

def get_contours(img, thresh):
    contours, _ = cv2.findContours(process(img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    r1, r2 = sorted(contours, key=cv2.contourArea)[-3:-1]
    x, y, w, h = cv2.boundingRect(np.r_[r1, r2])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
def get_moments(thresh):    
    
    # calculate moments of binary image
   # M = cv2.moments(thresh)
    
    # Calculate area
    # foam_area = M['m00']
    foam_area = cv2.countNonZero(process(img))
    
    # Calculate centroid
    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])

    print("The foam area is",foam_area)
    print("(pixels^2)")
    return foam_area
    
#get_contours(img)
d1 = 4.8 #diameter of circle 1 in cm
d2 = 9.0   #diameter of circle 2 in cm
r1 = d1/2.0
r2 = d2/2.0
circ_1 = 2.0 * np.pi * r1 #circumference 1
circ_2 = 2.0 * np.pi * r2 #circumference 2
final_circ = (circ_1 + circ_2)/2.0 #taking the average circumference

pro_img = process(img)

# cv2.imshow("img_processed", pro_img)
dims = pro_img.shape
print(dims)
image_area = pro_img.shape[0] * pro_img.shape[1]

A = get_moments(process(img)) #getting the area of foam
foam_per = (A/(image_area))*100*6
print("The percentage of foam is ",foam_per)

foam_vol = A * final_circ
# print("the foam volume is", foam_vol)

#height, width, _ = dims
#area = height * width
#print("Area of the image is : ", area)
cv2.waitKey(0)