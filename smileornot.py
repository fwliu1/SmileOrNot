import numpy as np
import cv2

smile = cv2.imread("smile.png")
smile = cv2.cvtColor(smile, cv2.COLOR_BGR2BGRA)
sad = cv2.imread("sad.png")
sad = cv2.cvtColor(sad, cv2.COLOR_BGR2BGRA)

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier('haarcascade_smile.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

smilebool = False;

while True:
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img_h, img_w, img_c = img.shape

    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.1,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    
    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        smiles = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.16,
            minNeighbors=35,     
            minSize=(40, 40),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        smilebool = False;
        for (x2,y2,w2,h2) in smiles:
            smilebool = True;
            #print(x2,y2)
            #cv2.rectangle(roi_color, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
        #print(smilebool)
        
        overlay = np.zeros((img_h, img_w, 4), dtype='uint8')
    
    smile_h, smile_w, smile_c = smile.shape
    sad_h, sad_w, sad_c = sad.shape
    
    if smilebool == False:
        for i in range(0, sad_h):
            for j in range(0, sad_w):
                if sad[i,j][3] != 0:
                    overlay[i,j] = sad[i,j];
    if smilebool == True:
        for i in range(0, smile_h):
                for j in range(0, smile_w):
                    if smile[i,j][3] != 0:
                        img_h 
                        overlay[i,j] = smile[i,j];
    
    cv2.addWeighted(overlay,0.25, img, 1.0, 0, img)
        
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
        
        
cap.release()
cv2.destroyAllWindows()