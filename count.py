import cv2
import datetime
import imutils

import sqlite3 as sql
import numpy as np
from centroidtracker import CentroidTracker
import time

rtsp_username = "admin"
rtsp_password = "admin"
rtsp_IP = "192.168.29.100"
#cam_width = 1280 #set to resolution of incoming video from DVR
#cam_height = 720 #set to resolution of incoming video from DVR
cam_width = 352
cam_height = 288
#motion_threshold = 1000 #decrease this value to increase sensitivity
motion_threshold = 1500
cam_no = 1

protopath = "/home/admin/test2/ATM/MobileNetSSD_deploy.prototxt"
modelpath = "/home/admin/test2/ATM/MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
# detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
# detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		   "sofa", "train", "tvmonitor"]

tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)




# camera=cv2.VideoCa



def main():
		con=sql.connect("sensorsinfo.db")
		con.row_factory=sql.Row
		cur=con.cursor()
		cur1=con.cursor()
		cur.execute("select * from camera_info")
		rtsps=cur.fetchall()
		cur1.execute("SELECT COUNT(*) FROM camera_info")
		pins=cur1.fetchall()
		a=pins[0][0]
		def non_max_suppression_fast(boxes, overlapThresh):
			try:
				if len(boxes) == 0:
					return []

				if boxes.dtype.kind == "i":
					boxes = boxes.astype("float")

				pick = []

				x1 = boxes[:, 0]
				y1 = boxes[:, 1]
				x2 = boxes[:, 2]
				y2 = boxes[:, 3]

				area = (x2 - x1 + 1) * (y2 - y1 + 1)
				idxs = np.argsort(y2)

				while len(idxs) > 0:
					last = len(idxs) - 1
					i = idxs[last]
					pick.append(i)

					xx1 = np.maximum(x1[i], x1[idxs[:last]])
					yy1 = np.maximum(y1[i], y1[idxs[:last]])
					xx2 = np.minimum(x2[i], x2[idxs[:last]])
					yy2 = np.minimum(y2[i], y2[idxs[:last]])

					w = np.maximum(0, xx2 - xx1 + 1)
					h = np.maximum(0, yy2 - yy1 + 1)

					overlap = (w * h) / area[idxs[:last]]

					idxs = np.delete(idxs, np.concatenate(([last],
														np.where(overlap > overlapThresh)[0])))

				return boxes[pick].astype("int")
			except Exception as e:
				print("Exception occurred in non_max_suppression : {}".format(e))



		# def find_screen():
		# 	if (x < cam_width):
		# 		if(y < cam_height):
		# 			screen = frame1[0:cam_height, 0:cam_width]
		# 			print("Activity in cam screen 1")
		# 		else:
		# 			screen = frame1[cam_height:cam_height*2, :cam_width]
		# 			print("Activity in cam screen 2")
		# 	else:
		# 		if (y < cam_height):
		# 			screen = frame1[:cam_height, cam_width:cam_width * 2]
		# 			print("Activity in cam screen 3")
		# 		else:
		# 			screen = frame1[cam_height:cam_height * 2, cam_width:cam_width * 2]
		# 			print("Activity in cam screen 4")
		# 		return (screen)




		def create_camera (rtsp):
				# rtsp = "rtsp://" + rtsp_username + ":" + rtsp_password + "@" + cam_ip + ":554/cam/realmonitor?channel=1&subtype=1" #change the IP to suit yours
			#rtsp = "0"
			# print("rtsp url",rtsp)
				cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
				cap.set(3, cam_width)  # ID number for width is 3
				cap.set(4, cam_height)  # ID number for height is 480
				cap.set(10, 100)  # ID number for brightness is 10
				return cap



		def read_camera():
				if(a==0):				
					return (Main_screen)
				if(a==1):
					success, current_screen = cam1.read()
					Main_screen [:cam_height, :cam_width, :3] = current_screen
					return (Main_screen)
				if(a==2):
					success, current_screen = cam1.read()
					Main_screen [:cam_height, :cam_width, :3] = current_screen
					success, current_screen = cam2.read()
					Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen			
					return (Main_screen)
				if(a==3):
					success, current_screen = cam1.read()
					Main_screen [:cam_height, :cam_width, :3] = current_screen
					success, current_screen = cam2.read()
					Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen
					success, current_screen = cam3.read()
					Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen			
					return (Main_screen)
				if(a==4):
					success, current_screen = cam1.read()
					Main_screen [:cam_height, :cam_width, :3] = current_screen
					success, current_screen = cam2.read()
					Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen
					success, current_screen = cam3.read()
					Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen
					success, current_screen = cam4.read()
					Main_screen[cam_height:cam_height*2, cam_width:cam_width*2, :3] = current_screen
					return (Main_screen)

		if a == 1:
			cam1 = create_camera(rtsps[0][1])
		if a == 2:
		    # print(rtsps[i-1][1])
			cam1 = create_camera(rtsps[0][1])
			cam2 = create_camera(rtsps[1][1])
		if a == 3:
			cam1 = create_camera(rtsps[0][1])
			cam2 = create_camera(rtsps[1][1])
			cam3 = create_camera(rtsps[2][1])
		if a == 4:
			cam1 = create_camera(rtsps[0][1])
			cam2 = create_camera(rtsps[1][1])
			cam3 = create_camera(rtsps[2][1])
			cam4 = create_camera(rtsps[3][1])


		# for i in range(1,a+1):
                
                
        #             if i == 1:
        #                 cam1 = create_camera(rtsps[i-1][1])
        #             if i == 2:
        #                 # print(rtsps[i-1][1])
        #                 cam2 = create_camera(rtsps[i-1][1])
        #             if i == 3:
        #                 cam3 = create_camera(rtsps[i-1][1])
        #             if i == 4:
        #                 cam4 = create_camera(rtsps[i-1][1])

		# def read_camera():
      
		# 		print("read camera")
    
		# 		success, current_screen = cam1.read()
		# 		Main_screen [:cam_height, :cam_width, :3] = current_screen
		# 		success, current_screen = cam2.read()
		# 		Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen
		# 		success, current_screen = cam3.read()
		# 		Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen
		# 		success, current_screen = cam4.read()
		# 		Main_screen[cam_height:cam_height*2, cam_width:cam_width*2, :3] = current_screen
		# 		return (Main_screen)

	# Open all four camera Framers
		# cam1 = create_camera("10.0.0.176")
		# cam2 = create_camera("10.0.0.179")
		# cam3 = create_camera("10.0.0.178")
		# cam4 = create_camera("10.0.0.180")
		print ("Reading camera successfull")
		Main_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen on which all four camera will be stiched
		display_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen to be display on 5 inch TFT display
		kernal = np.ones((5,5),np.uint8) #form a 5x5 matrix with all ones range is 8-bit



		while True:

			frame2 = read_camera() #Read the 2nd frame


			fpsLimit = 1
			startTime = time.time()
			fps_start_time = datetime.datetime.now()
			fps = 0
			total_frames = 0
			lpc_count = 0
			
			object_id_list = []
			while True:
				# print("while true 2")
				frame = read_camera()
			#        frame=generate_frames()
				# Read the first frame
				# cv2.imshow("akash",frame)
				nowTime = time.time()
				if (int(nowTime - startTime)) > fpsLimit:
					# print("first if")
					#startTime = time.time()
					#frame2 = read_camera()
					#        frame  = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
					frame = imutils.resize(frame, width=600)
					total_frames = total_frames + 1

					(H, W) = frame.shape[:2]

					blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)

					detector.setInput(blob)
					person_detections = detector.forward()
					rects = []
					for i in np.arange(0, person_detections.shape[2]):
						# print("for loop 1")
						confidence = person_detections[0, 0, i, 2]
						if confidence > 0.5:
							idx = int(person_detections[0, 0, i, 1])

							if CLASSES[idx] != "person":
								continue
							person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
							(startX, startY, endX, endY) = person_box.astype("int")
							rects.append(person_box)

					boundingboxes = np.array(rects)
					boundingboxes = boundingboxes.astype(int)
					rects = non_max_suppression_fast(boundingboxes, 0.3)
					objects = tracker.update(rects)

					if objects:
					

						for (objectId, bbox) in objects.items():
							# print("for loop 2")
							x1, y1, x2, y2 = bbox
							x1 = int(x1)
							y1 = int(y1)
							x2 = int(x2)

							cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
							text = "ID: {}".format(objectId)
							cv2.putText(frame, text, (x1, y1 - 5),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

							if objectId not in object_id_list:
								object_id_list.append(objectId)

							fps_end_time = datetime.datetime.now()
							time_diff = fps_end_time - fps_start_time
							if time_diff.seconds == 0:
								fps = 0.0
							else:
								fps = (total_frames / time_diff.seconds)

							fps_text = "FPS: {:.2f}".format(fps)

							cv2.putText(frame, fps_text, (5, 30),
										cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
							
							lpc_count = len(objects)
							# cv2.imshow("akash",frame)
							# print("update count")
							print(lpc_count)
							f=open("/home/admin/test2/ATM/count.txt","w")
							f.write(str(lpc_count))
							f.close()
							startTime=time.time()

					else:
						# print("0")
						f=open("/home/admin/test2/ATM/count.txt","w")
						f.write(str(0))
						f.close()
		
	
				ret,buffer=cv2.imencode('.jpg',frame2)
				frame=buffer.tobytes()
				

		# yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')		

main()