from asyncore import read
from crypt import methods
from itertools import count
import RPi.GPIO as GPIO
from flask import Flask, render_template,request,Response,jsonify
# import count
import cv2
import numpy as np
import sqlite3 as sql
import time




import datetime
import imutils
import numpy as np
from centroidtracker import CentroidTracker

protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
# detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
# detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)


app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)






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

f=open("count.txt","r")
cnt=f.read()
f.close()

a=open("MaskData.txt","r")
mask=a.read()
a.close()


main_screen_dict = {
    1 : ':cam_height, :cam_width, :3',
    2 : 'cam_height:cam_height*2, :cam_width, :3',
    3 : ':cam_height, cam_width:cam_width*2, :3',
    4 : 'cam_height:cam_height*2, cam_width:cam_width*2, :3'
}



gpio_pins={1:3,
           2:5,
           3:7,
           4:11,
           5:12,
           6:13,
           7:15,
           8:16,
           9:18,
           10:19,
           11:21,
           12:22,
           13:23,
           14:24,
           15:26,
           16:29,
           17:31,
           18:32,
           19:33,
           20:35,
           21:36,
           22:37,
           23:38,
           24:40 
}

#voltage_pins 



relay_pin={1:11,
           2:13,
           3:15,
           4:19,
           5:21,
           6:23,
           7:33,
           8:35,
           9:37,
           10:12,
           11:16,
           12:18,
           13:22,
           14:32,
           15:36,
           16:38,
           17:40
}




# camera=cv2.VideoCapture(0)
def generate_frames():
    con=sql.connect("sensorsinfo.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur1=con.cursor()
    cur.execute("select * from camera_info")
    rtsps=cur.fetchall()
    cur1.execute("SELECT COUNT(*) FROM camera_info")
    pins=cur1.fetchall()
    a=pins[0][0]
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
    
    
    
    # def read_camera ():

    #     for i in range(1,a+1):
                    
                    
    #                     if i == 1:
    #                         print(rtsps[i-1][1])
    #                         cam1 = create_camera(rtsps[i-1][1])

    #                         success, current_screen = cam1.read()
    #                         Main_screen[:cam_height, :cam_width, :3] = current_screen

    #                     if i == 2:
    #                         # print(rtsps[i-1][1])
    #                         cam2 = create_camera(rtsps[i-1][1])

    #                         success, current_screen = cam2.read()
    #                         Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen

    #                     if i == 3:
    #                         cam3 = create_camera(rtsps[i-1][1])

    #                         success, current_screen = cam3.read()
    #                         Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen

    #                     if i == 4:
    #                         cam4 = create_camera(rtsps[i-1][1])

    #                         success, current_screen = cam4.read()
    #                         Main_screen[cam_height:cam_height*2, cam_width:cam_width*2, :3] = current_screen

    
    
    # for i in range(1,a+1):
                    
                    
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
       
        # return (Main_screen)

#Open all four camera Framers
    # cam1 = create_camera("10.0.0.190")
    # cam2 = create_camera("10.0.0.179")
    # cam3 = create_camera("10.0.0.178")
    # cam4 = create_camera("10.0.0.180")
    # cam5 = create_camera("10.0.0.180")
# print ("Reading camera successfull")
    Main_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen on which all four camera will be stiched
    display_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen to be display on 5 inch TFT display
    kernal = np.ones((5,5),np.uint8) #form a 5x5 matrix with all ones range is 8-bit

    # print("Main screen",Main_screen)
 



    while True:
            
        ## read the camera frame
        #  success,frame=camera.read()
        
        frame2 = read_camera() #Read the 2nd frame
     
        # if not success:
        #     break
        # else:
        ret,buffer=cv2.imencode('.jpg',frame2)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




 
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():

    con=sql.connect("sensorsinfo.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    # cur.execute("select * from sensors_info")
    # posts=cur.fetchall()
     

   
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        
        
        
        with sql.connect('sensorsinfo.db') as con:
               cur=con.cursor()
               cur.execute('DELETE FROM sensors_info WHERE pinno = (?)',(getid,))
               con.commit()
               msg="Sensor added successfully"
             
    return jsonify(msg) 


@app.route('/on')
def on():
        GPIO.setmode(GPIO.BOARD)
        con=sql.connect("sensorsinfo.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from sensors_info")
        posts=cur.fetchall()

        
        
        for post in posts:
            
            for i in posts:
                if(i['relaypinno']!='None'):
                        # print(i['relaypinno'])

                        # gpio_pins=gpio_pin
                        a=relay_pin.get(i['relaypinno'])   
                        # print(a)         
                        GPIO.setup(a, GPIO.OUT)
                        try:
                                #while True:
                    # GPIO.output(11,False)
                        #print('Relay 1 OFF')
                        #time.sleep(5)

                                GPIO.output(a,True)
                                print('Relay 1 ON')
                                time.sleep(20)
                                #break
                        finally:
                                print("clean up called")
                                GPIO.cleanup()

    
        return render_template('index.html')







gpio_pin={1:3,
           2:5,
           3:7,
           4:11,
           5:12,
           6:13,
           7:15,
           8:16,
           9:18,
           10:19,
           11:21,
           12:22,
           13:23,
           14:24,
           15:26,
           16:29,
           17:31,
           18:32,
           19:33,
           20:35,
           21:36,
           22:37,
           23:38,
           24:40 
}

#voltage_pins 


voltage_pins={1:1,
              2:2,
              3:4,
              4:17
}
relay_pins={1:11,
           2:13,
           3:15,
           4:19,
           5:21,
           6:23,
           7:33,
           8:35,
           9:37,
           10:12,
           11:16,
           12:18,
           13:22,
           14:32,
           15:36,
           16:38,
           17:40
}






@app.route("/update_sensor_status",methods=['POST'])
def update_sensor_status():
    GPIO.setmode(GPIO.BOARD)
    while(1):
        con=sql.connect("sensorsinfo.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from sensors_info")
        posts=cur.fetchall()
        
        sensor = {}
        for i in posts:
            # print('pinnno',i['pinno'])
            # print(i['Name'])
            pin_name = 'Pinno' + str(i['pinno'])
            sensor[pin_name] = {}
            # print(i['pinno'])
            # gpio_pins=gpio_pin
            a=gpio_pins.get(i['pinno'])
            # print("hello")
            
            # print(a)
            # print("jay ho")
            

            ##Check pin status
            GPIO.setup(a, GPIO.IN, pull_up_down=GPIO.PUD_UP )
            

            status= GPIO.input(a)
            # print(status)


            if 'State' not in sensor[pin_name]:
                sensor[pin_name]['State'] = status
            else:
                sensor[pin_name]['State'] += status 

            if 'Onmsg' not in sensor[pin_name]:
                sensor[pin_name]['Onmsg'] = i['Onmsg']
            else:
                sensor[pin_name]['Onmsg'] += i['Onmsg'] 

            if 'Offmsg' not in sensor[pin_name]:
                sensor[pin_name]['Offmsg'] = i['Offmsg']
            else:
                sensor[pin_name]['Offmsg'] += i['Offmsg']  

            if 'Name' not in sensor[pin_name]:
                sensor[pin_name]['Name'] = i['Name']
            else:
                sensor[pin_name]['Name'] += i['Name'] 
                
            if 'Type' not in sensor[pin_name]:
                sensor[pin_name]['Type'] = i['Type']
            else:
                sensor[pin_name]['Type'] += i['type'] 
                               

        # print(sensor)
        return jsonify(sensor)


@app.route("/")
def home():
    GPIO.setmode(GPIO.BOARD)
   
    while(1):
        con=sql.connect("sensorsinfo.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from sensors_info")
        posts=cur.fetchall()

        
        sensor = {}
        
        sensor={
            
            'Pinno1': {
                'State': 'On',
                'Onmsg': 'On',
                'OfMsg': 'Off',
                'Name': 'A'
                
            },
            'Pinno2': {
                'State': 'On',
                'Onmsg': 'On',
                'OfMsg': 'Off',
                'Name': 'B'
                
            },
            'Pinno3': {
                'State': 'On',
                'Onmsg': 'On',
                'OfMsg': 'Off',
                'Name': 'C'
                
            }
            
        }
        
        # print(sensor)
        sensor2 = {}
        for i in posts:
            print('pinnno',i['pinno'])
            # print(i['Name'])
            pin_name = 'Pinno' + str(i['pinno'])
            sensor2[pin_name] = {}

            ##Check pin status
            # GPIO.setup(i['pinno'], GPIO.IN, pull_up_down=GPIO.PUD_UP )
	        #GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP )

            # status= GPIO.input(i['pinno'])
            
            
            if 'State' not in sensor2[pin_name]:
                sensor2[pin_name]['State'] = i['State']
            else:
                sensor2[pin_name]['State'] += i['State']
                
            if 'Onmsg' not in sensor2[pin_name]:
                sensor2[pin_name]['Onmsg'] = i['Onmsg']
            else:
                sensor2[pin_name]['Onmsg'] += i['Onmsg'] 
                
            if 'Offmsg' not in sensor2[pin_name]:
                sensor2[pin_name]['Offmsg'] = i['Offmsg']
            else:
                sensor2[pin_name]['Offmsg'] += i['Offmsg']  
                
            if 'Name' not in sensor2[pin_name]:
                sensor2[pin_name]['Name'] = i['Name']
            else:
                sensor2[pin_name]['Name'] += i['Name'] 
                
            if 'Type' not in sensor2[pin_name]:
                sensor2[pin_name]['Type'] = i['Type']
            else:
                sensor2[pin_name]['Type'] += i['type'] 
        print("Sensor2",sensor2)
        # for i in  posts:
        #     k=i[0]
        #     status=0
        #     GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP )

        #     status= GPIO.input(k)
        #     temp={
        #     'status':status
        #     }
            
        return render_template('index.html', sensor=sensor2 )


# @app.route('/addrec', methods=['POST', 'GET'])
# def addrec():
#     print(request.form)
#     if (request.method == 'POST'):
#         # try:
#         #    print(request.form)
#         #    print("request",request)
#            pinno1 = request.form['inputText']
#            des = request.form['desc']
#            stat = request.form['inputPassword']
#            onmsg = request.form['on']
#            offmsg = request.form['off']
#            voltagepinno = request.form['inputText2']
#            relaypinnno = request.form['inputText3']

#            sensortype = request.form['X']
#            print(sensortype)
#            with sql.connect('sensorsinfo.db') as con:
#                cur=con.cursor()
#                cur.execute("INSERT INTO sensors_info (pinno,Name,ONmsg,OFFmsg,state,voltagepinno,relaypinno,type) VALUES (?,?,?,?,?,?,?,?)", (pinno1,des,onmsg,offmsg,stat,voltagepinno,relaypinnno,sensortype))
#                con.commit()
#                msg="Sensor added successfully"
#         # except Exception as exp:
#         #     con.rollback()
#         #     msg="error"
#         # finally:
#         #     return render_template("AddSensor.html")
#         #     con.close()
#     # return render_template("AddSensor.html")
#     return redirect('/AddSensor')




@app.route("/AddSensor", methods=['POST', 'GET'])
def Sensor():
    if (request.method == 'POST'):
        # try:
        #    print(request.form)
        #    print("request",request)
           pinno1 = request.form['inputText']
        #    print(pinno1)
           des = request.form['desc']
           stat = request.form['inputPassword']
           onmsg = request.form['on']
           offmsg = request.form['off']
           voltagepinno = request.form['inputText2']
        #    print(voltagepinno)
           relaypinnno = request.form['inputText3']

           sensortype = request.form['X']
           print(sensortype)
           with sql.connect('sensorsinfo.db') as con:
               cur=con.cursor()
               cur.execute("INSERT INTO sensors_info (pinno,Name,ONmsg,OFFmsg,state,voltagepinno,relaypinno,type) VALUES (?,?,?,?,?,?,?,?)", (pinno1,des,onmsg,offmsg,stat,voltagepinno,relaypinnno,sensortype))
               con.commit()
               msg="Sensor added successfully"
        
    con=sql.connect("sensorsinfo.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from sensors_info")
    pinno=cur.fetchall()
    print("before gpiopin",gpio_pin)
    # for pin in pinno:
    #     if pin['pinno'] in gpio_pin:
    #         del gpio_pin[pin['pinno']]
    #     if pin['voltagepinno'] in  voltage_pins:
    #         del voltage_pins[pin['voltagepinno']]
    # relaypinno
    for pin in pinno:
        for k in list(gpio_pin):
            # print(gpio_pin[k],pin['pinno'])
            if k == pin['pinno']:
                print(k,gpio_pin[k],pin['pinno'])
                # k1=gpio_pin.get(k)
                # k2=gpio_pin.pop(k)
                # k3=gpio_pin.pop(k1)
                del gpio_pin[pin['pinno']]
                # print(k2)

            # if gpio_pin[k] == pin['relaypinno']:
            #     del gpio_pin[k]

        for k in list(voltage_pins):
            if k == pin['voltagepinno']:
                del voltage_pins[k]

        for k in list(relay_pins):
            if k == pin['relaypinno']:
                del relay_pins[k]

            if k== pin['pinno']:
                del relay_pins[k]

    print("after gpiopin",gpio_pin)

        
    return render_template('AddSensor.html', gpio_pin=gpio_pin, voltage_pins=voltage_pins, relay_pins=relay_pins)





@app.route('/delrec', methods=['POST', 'GET'])
def deleteSensor():
    if (request.method == 'POST'):
        data = request.data
        json2 = request.get_json() 
        # data1 = json.loads(request.data)
        print(data)
        print(json2)
        
    return render_template("View.html")






# @app.route("/update",methods=['POST'])
# def update1():
#     while(1):
#         con=sql.connect("sensorsinfo.db")
#         con.row_factory=sql.Row
#         cur=con.cursor()
#         cur.execute("select * from sensors_info")
#         posts=cur.fetchall()

#         sensor = {}
        
#         sensor={
            
#             'Pinno1': {
#                 'State': 'On',
#                 'Onmsg': 'On',
#                 'OfMsg': 'Off',
#                 'Name': 'A'

#             },
#             'Pinno2': {
#                 'State': 'On',
#                 'Onmsg': 'On',
#                 'OfMsg': 'Off',
#                 'Name': 'B'
                
#             },
#             'Pinno3': {
#                 'State': 'On',
#                 'Onmsg': 'On',
#                 'OfMsg': 'Off',
#                 'Name': 'C'
                
#             }
            
#         }
        
#         # print(sensor)
#         sensor2 = {}
#         for i in posts:
#             print('pinnno',i['pinno'])
#             # print(i['Name'])
#             pin_name = 'Pinno' + str(i['pinno'])
#             sensor2[pin_name] = {}
#             gpio_pins=gpio_pin
#             a=gpio_pins.get(i['pinno'])

#             ##Check pin status
#             GPIO.setup(a, GPIO.IN, pull_up_down=GPIO.PUD_UP )
#             #GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP )

#             status= GPIO.input(a)


#             if 'State' not in sensor2[pin_name]:
#                 sensor2[pin_name]['State'] = status
#             else:
#                 sensor2[pin_name]['State'] +=status

#             if 'Onmsg' not in sensor2[pin_name]:
#                 sensor2[pin_name]['Onmsg'] = i['Onmsg']
#             else:
#                 sensor2[pin_name]['Onmsg'] += i['Onmsg'] 

#             if 'Offmsg' not in sensor2[pin_name]:
#                 sensor2[pin_name]['Offmsg'] = i['Offmsg']
#             else:
#                 sensor2[pin_name]['Offmsg'] += i['Offmsg']  

#             if 'Name' not in sensor2[pin_name]:
#                 sensor2[pin_name]['Name'] = i['Name']
#             else:
#                 sensor2[pin_name]['Name'] += i['Name'] 
#         print("Sensor2",sensor2)
#         # for i in  posts:
#         #     k=i[0]
#         #     status=0
#         #     GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP )

#         #     status= GPIO.input(k)
#         #     temp={
#         #     'status':status
#         #     }

# 	#return render_template('index.html', sensor=sensor2 )
#         return jsonify(sensor2)











@app.route("/View")
def View():    
    con=sql.connect("sensorsinfo.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from sensors_info")
    rows=cur.fetchall()
    
    return render_template('View.html',rows=rows)


@app.route("/AddCamera")
def AddCamera():
    return render_template('AddCamera.html')





@app.route('/addcamera', methods=['POST', 'GET'])
def addcamera():
    if (request.method == 'POST'):
        try:
           name= request.form['name']
           url= request.form['url']
           with sql.connect('sensorsinfo.db') as con:
               cur=con.cursor()
               cur.execute("INSERT INTO camera_info (name,url) VALUES (?,?)", (name , url))
               con.commit()
               msg="Sensor added successfully"
        except:
            con.rollback()
            msg="error"
        finally:
            return render_template("AddCamera.html")
            con.close()



# @app.route("/FaceMask")
# def FaceMask():
#     return render_template('FaceMask.html')

@app.route("/update",methods=['POST'])
def update():
    f=open("count.txt","r")
    cnt=f.read()
    f.close()
    return jsonify('',render_template('update.html',x=cnt))

@app.route("/update2",methods=['POST'])
def update2():
    f=open("count.txt","r")
    cnt=f.read()
    f.close()
    return jsonify('',render_template('update2.html',x=cnt))   

@app.route("/update3",methods=['POST'])
def update():
    f=open("mask.txt","r")
    mask=f.read()
    f.close()
    return jsonify('',render_template('update3.html',y=mask)) 




# @app.route("/PersonCount")
# def PersonCount():
   
#     return render_template('PersonCount.html',x=cnt)


@app.route("/ShowScreen")
def ShowScreen():
    return render_template('ShowScreen.html')

@app.route("/Video")
def Video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frm(count):
    while True:
        frame=count.abc()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')		


if __name__ == "__main__":

    app.run(host='0.0.0.0',debug=True)
