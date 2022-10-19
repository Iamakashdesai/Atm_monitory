import cv2
import imutils
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
import datetime
import imutils
import time

cam_width = 640
cam_height = 480

#models
prototxtPath = r"deploy.prototxt"
weightsPath = r"res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("mask_detector.model")

#frame0 = cv2.VideoCapture(0)
#frame1 = cv2.VideoCapture(1)

def read_camera():
   while True:
      success, current_screen = frame0.read()
      Main_screen[:cam_height, :cam_width, :3] = current_screen
      success, current_screen = frame1.read()
      Main_screen[:cam_height, cam_width:cam_width *2, :3] = current_screen
      return (Main_screen)

def find_screen():
   if (x < cam_width):
      if (y < cam_height):
         screen = window[0:cam_height, 0:cam_width]
         print("Activity in cam screen 1")
      else:
         screen = window[:cam_height, cam_width:cam_width *2]
         print("Activity in cam screen 2")
      return (screen)

frame0 = cv2.VideoCapture(0)
frame1 = cv2.VideoCapture(1)

print("Reading cam successfully")
Main_screen = np.zeros(((cam_height *1), (cam_width *2), 3), np.uint8)
display_screen = np.zeros(((cam_height *1), (cam_width *2), 3), np.uint8)
kernal = np.ones((5,5), np.uint8)

#while 1:

   #ret0, img0 = frame0.read()
   #ret1, img00 = frame1.read()
   #img1 = cv2.resize(img0,(360,240))
   #img2 = cv2.resize(img00,(360,240))
   #if (frame0):
       #cv2.imshow('img1',img1)
   #if (frame1):
       #cv2.imshow('img2',img2)

   #k = cv2.waitKey(30) & 0xff
   #if k == 27:
      #break

#frame0.release()
#frame1.release()
#cv2.destroyAllWindows()

#Function to detect mask
def detect_and_predict_mask(window0, faceNet, maskNet):
   # grab the dimensions of the frame and then construct a blob
   # from it
   (h, w) = window0.shape[:2]
   blob = cv2.dnn.blobFromImage(window0, 1.0, (224, 224),
                                (104.0, 177.0, 123.0))

   # pass the blob through the network and obtain the face detections
   faceNet.setInput(blob)
   detections = faceNet.forward()
   print(detections.shape)

   # initialize our list of faces, their corresponding locations,
   # and the list of predictions from our face mask network
   faces = []
   locs = []
   preds = []

   # loop over the detections
   for i in range(0, detections.shape[2]):
      # extract the confidence (i.e., probability) associated with
      # the detection
      confidence = detections[0, 0, i, 2]

      # filter out weak detections by ensuring the confidence is
      # greater than the minimum confidence
      if confidence > 0.5:
         # compute the (x, y)-coordinates of the bounding box for
         # the object
         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
         (startX, startY, endX, endY) = box.astype("int")

         # ensure the bounding boxes fall within the dimensions of
         # the frame
         (startX, startY) = (max(0, startX), max(0, startY))
         (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

         # extract the face ROI, convert it from BGR to RGB channel
         # ordering, resize it to 224x224, and preprocess it
         face = window0[startY:endY, startX:endX]
         face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
         face = cv2.resize(face, (224, 224))
         face = img_to_array(face)
         face = preprocess_input(face)

         # add the face and bounding boxes to their respective
         # lists
         faces.append(face)
         locs.append((startX, startY, endX, endY))

         # only make a predictions if at least one face was detected
   if len(faces) > 0:
      # for faster inference we'll make batch predictions on *all*
      # faces at the same time rather than one-by-one predictions
      # in the above `for` loop
      faces = np.array(faces, dtype="float32")
      preds = maskNet.predict(faces, batch_size=32)

      # return a 2-tuple of the face locations and their corresponding
      # locations
   return (locs, preds)

def main():

   fpsLimit = 1
   startTime = time.time()
   fps_start_time = datetime.datetime.now()
   fps = 0
   total_frames = 0

   while True:
      window0 = read_camera()
      nowTime = time.time()
      if(int(nowTime - startTime)) > fpsLimit:
         window0 = imutils.resize(window0, width=600)
         total_frames = total_frames + 1

         (h, w) = window0.shape[:2]

         blob = cv2.dnn.blobFromImage(window0, 1.0, (224, 224),
            (104.0, 177.0, 123.0))

         faceNet.setInput(blob)
         detections = faceNet.forward()
         print(detections.shape)

         (locs, preds) = detect_and_predict_mask(window0, faceNet, maskNet)

         for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            # print(label)
            cv2.putText(window0, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(window0, (startX, startY), (endX, endY), color, 2)
            datet = str(datetime.datetime.now())

            f = open("mask.txt", "w")
            f.write(str(label))
            f.close()

         fps_end_time = datetime.datetime.now()
         time_diff = fps_end_time - fps_start_time
         if time_diff.seconds == 0:
            fps = 0.0
         else:
            fps = (total_frames / time_diff.seconds)

         datet = "FPS: {:.2f}".format(fps)

         cv2.putText(window0, datet, (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         #f = open("E:/Admission to Academic Year 2020-21_files/count.txt","w")
         #f.write(str(label))
         #f.close()

         cv2.imshow("App", window0)
         startTime = time.time()
         print(fps)
         key = cv2.waitKey(1)
         if key == ord('q'):
            break

main()