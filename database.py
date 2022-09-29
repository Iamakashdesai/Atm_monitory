import sqlite3

conn = sqlite3.connect('sensorsinfo.db')
    


conn.execute('''
            CREATE TABLE sensors_info (
                pinno INTEGER PRIMARY KEY NOT NULL,
                Name TEXT NOT NULL,
                ONmsg TEXT ,
                OFFmsg TEXT,
                state TEXT 
            );
        ''')

conn.commit()
print("User table created successfully")
    
conn.close()