import cv2
import math

videoFile = "citmore.mp4"
imagesFolder = "/Users/arin/Desktop/final_yr_project/frame_extract/frames/citmoreframes"
cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
print cap.isOpened()
print frameRate
i = 0
# frameRate = 25.0
while(cap.isOpened()):
	# print "extracting..."
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (int(frameId) % math.floor(frameRate) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
        cv2.imwrite(filename, frame)
    print "extracting..." + str(frameId)
    i = i + 1
cap.release()
print "Done!"
