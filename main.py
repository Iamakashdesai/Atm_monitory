# import RPi.GPIO as GPIO

from flask import Flask, render_template,request,Response

import cv2
import numpy as np
import sqlite3 as sql



app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)


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

# camera=cv2.VideoCapture(0)
def generate_frames():
    def create_camera (cam_ip):
        rtsp = "rtsp://" + rtsp_username + ":" + rtsp_password + "@" + cam_ip + ":554/cam/realmonitor?channel=1&subtype=1" #change the IP to suit yours
    #rtsp = "0"
    # print("rtsp url",rtsp)
        cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
        cap.set(3, cam_width)  # ID number for width is 3
        cap.set(4, cam_height)  # ID number for height is 480
        cap.set(10, 100)  # ID number for brightness is 10
        return cap
    def read_camera ():
        success, current_screen = cam1.read()
        Main_screen [:cam_height, :cam_width, :3] = current_screen
        success, current_screen = cam2.read()
        Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen
        success, current_screen = cam3.read()
        Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen
        success, current_screen = cam4.read()
        Main_screen[cam_height:cam_height*2, cam_width:cam_width*2, :3] = current_screen
        return (Main_screen)

#Open all four camera Framers
    cam1 = create_camera("10.0.0.190")
    cam2 = create_camera("10.0.0.179")
    cam3 = create_camera("10.0.0.178")
    cam4 = create_camera("10.0.0.180")
# print ("Reading camera successfull")
    Main_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen on which all four camera will be stiched
    display_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen to be display on 5 inch TFT display
    kernal = np.ones((5,5),np.uint8) #form a 5x5 matrix with all ones range is 8-bit



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

@app.route("/")
def home():
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
            # print(i['pinno'])
            # print(i['Name'])
            pin_name = 'Pinno' + str(i['pinno'])
            sensor2[pin_name] = {}
            
            ##Check pin status
            # GPIO.setup(i['pinno'], GPIO.IN, pull_up_down=GPIO.PUD_UP )

            # status= GPIO.input(i['pinno'])
            
            if 'State' not in sensor2[pin_name]:
                sensor2[pin_name]['State'] = i['state']
            else:
                sensor2[pin_name]['State'] += i['state']
                
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
        print("Sensor2",sensor2)
        # for i in  posts:
        #     k=i[0]
        #     status=0
        #     GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP )

        #     status= GPIO.input(k)
        #     temp={
        #     'status':status
        #     }
            
        return render_template('index.html', sensor=sensor )
@app.route("/AddSensor")
def Sensor():
    return render_template('AddSensor.html')



@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if (request.method == 'POST'):
        try:
           pinno1 = request.form['inputText']
           des = request.form['desc']
           stat = request.form['inputPassword']
           onmsg = request.form['on']
           offmsg = request.form['off']
           with sql.connect('sensorsinfo.db') as con:
               cur=con.cursor()
               cur.execute("INSERT INTO sensors_info (pinno,Name,ONmsg,OFFmsg,state) VALUES (?,?,?,?,?)", (pinno1,des,onmsg,offmsg,stat))
               con.commit()
               msg="Sensor added successfully"
        except:
            con.rollback()
            msg="error"
        finally:
            return render_template("AddSensor.html")
            con.close()







@app.route("/View")
def View():    
    con=sql.connect("sensorsinfo.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from sensors_info")
    rows=cur.fetchall()
    
    return render_template('View.html',rows=rows)

@app.route("/Reset")
def Reset():
    return render_template('Reset.html')

@app.route("/AddCamera")
def AddCamera():
    return render_template('AddCamera.html')

@app.route("/FaceMask")
def FaceMask():
    return render_template('FaceMask.html')

@app.route("/PersonCount")
def PersonCount():
    return render_template('PersonCount.html')

@app.route("/ShowScreen")
def ShowScreen():
    return render_template('ShowScreen.html')

@app.route("/Video")
def Video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)