import sqlite3 as sql

import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BOARD)



gpio_pin={1:3,
           2:5,
           3:7,
           4:11,5:12,
           6:13,
           7:15,8:16,
                9:18,
           10:19,
           11:21,12:22,
           13:23,14:24,
                 15:26,
           16:29,
           17:31,18:32,
           19:33,
           20:35,21:36,
           22:37,23:38,
                 24:40 
}

#voltage_pins 


voltage_pins={1:1,
              2:2,
              3:4,
              4:17
}



# while (True):
con=sql.connect("sensorsinfo.db")
# con.row_factory=sql.Row
cur=con.cursor()
cur.execute("select * from sensors_info")
posts=cur.fetchall()
print(posts)


for i in posts:
    outpin=i[0]
    print(outpin)
    gpio_pins=gpio_pin
    a=gpio_pins.get(i[0])
    print(a)

    GPIO.setup(a, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        #GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP )

    output= GPIO.input(a)
    print(output)
    if(i[4]=='ON'):
        dbvalue=0
        if(dbvalue!=output):
            print(dbvalue,output)
        #    print("changed ")
            
            
        #    con=sql.connect('sensorsinfo.db')
        #    cur.execute("UPDATE sensors_info SET state='OFF' WHERE state='ON'")
        #    con.commit()
            with sql.connect('sensorsinfo.db') as con:
                cur=con.cursor()
                cur.execute("UPDATE sensors_info SET state='OFF' WHERE pinno=?",(i[0],))
                cur.execute("INSERT INTO HISTORY (PINNO, NAME,STATE,TIME) VALUES(?,?,?,datetime('now','localtime'))",(i[0],i[1],i[4],))
            #   cur.execute("UPDATE sensors_info SET state='ON' WHERE state='OFF'")
                con.commit()
                msg="Sensor added successfully"
    else:
        dbvalue=1
        if(dbvalue!=output):
            print(dbvalue,output)


        #    print("changed ")
            
            
        #    con=sql.connect('sensorsinfo.db')
        #    cur.execute("UPDATE sensors_info SET state='OFF' WHERE state='ON'")
        #    con.commit()
            with sql.connect('sensorsinfo.db') as con:
                cur=con.cursor()
            #   cur.execute("UPDATE sensors_info SET state='OFF' WHERE state='ON'")
                cur.execute("UPDATE sensors_info SET state='ON' WHERE PINNO=?",(i[0],))
                cur.execute("INSERT INTO HISTORY (PINNO, NAME,STATE,TIME) VALUES(?,?,?,datetime('now','localtime'))",(i[0],i[1],i[4],))

                con.commit()
                msg="Sensor added successfully"
        
        
        
    



con.close()



