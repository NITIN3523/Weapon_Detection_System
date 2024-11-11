import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image,ImageTk
import numpy as np
import pymongo
from UI.detection import Detection                
from datetime import datetime
import time
import subprocess
import threading
import os
from UI.send_alert import send_detection_link


def run_server_side_app():
    subprocess.Popen(['python', 'Server_Side/app.py'], cwd=os.getcwd())

# Create and start the thread
thread = threading.Thread(target=run_server_side_app)
thread.start()

store_email = None
store_camera_name = None

def set_email(email):
    global store_email
    store_email = email
    
def set_camera_name(camera_name):
    global store_camera_name
    store_camera_name = camera_name

class MonitoringWindow():
    
    def __init__(self,root):     
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client.Weapon_Detection_Alert_Info
        self.db_dash = db.dashboard
        self.db_email = db.users
        
        # root = tk.Tk()
        self.root = root
        self.root = tk.Toplevel(root)  
        
        self.center_window()
        self.root.title('Weapon Detection Monitoring')
        # self.root.resizable(0,0)
        self.root.iconbitmap(False,'Client_Side/transparent.ico')

        self.camera_frame = tk.Label(self.root)
        # self.camera_frame = tk.Label(self.root,width=123,height=32)

        s = ttk.Style()
        s.configure('stop_monitor.TButton', font=("Helvetica",11))
        self.monitor_button = ttk.Button(self.root, text='Stop Monitoring',width=28,style='stop_monitor.TButton',command=self.root_close)

        self.camera_frame.grid(row=0,column=0,padx=3,pady=3,sticky='nsew')
        self.monitor_button.grid(row=1,column=0,pady=3,sticky='ew')
        
        # Make sure rows and columns expand when window resizes
        self.root.grid_rowconfigure(0, weight=1)  # Camera frame row expands
        self.root.grid_columnconfigure(0, weight=1)  # Both camera frame and button expand horizontally
        
        self.cap = cv2.VideoCapture('Client_Side/gun.mp4')
        # self.cap = cv2.VideoCapture('gun.mp4')
        self.imgtk = None
        self.lasttime = time.time()
        self.set_frame()
        # self.root.mainloop()
        
    def root_close(self):
        self.cap.release()
        self.root.destroy()
    
    def center_window(self):
        window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 874) // 2
        y = (screen_height - 530) // 2
        window.geometry(f"874x530+{x}+{y}")
    
    def set_frame(self): 
        global store_email
        global store_camera_name
        
        ret, frame = self.cap.read()
        if ret:
            
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)            
            img = Image.fromarray(frame)    
            img = img.resize((865, 480), Image.Resampling.LANCZOS)
            np_image = np.array(img)
            img,flag = Detection.detectgun(image=np_image)
            
            current_time = time.time()  
            img = Image.fromarray(img)        
            
            if flag == 1 and current_time - self.lasttime >= 10:
                now = datetime.now()                
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                image = img
                image = image.resize((600,600),Image.Resampling.LANCZOS)               
                send_detection_link(store_email)                
                self.store_detection(image, store_camera_name, dt_string, store_email)                

            self.imgtk = ImageTk.PhotoImage(image=img)
            self.camera_frame.imgtk = self.imgtk
            self.camera_frame.configure(image=self.imgtk)
            
        self.root.after(1, self.set_frame)
        
    
    def store_detection(self, img, camera_name, datetime_str, email):
        
        now = datetime.now()
        # Split datetime into individual components
        day = now.day
        month = now.month
        year = now.year
        hour = now.hour
        minute = now.minute
        second = now.second
        
        filepath = 'Server_Side/static/Images/' + email   
        print(filepath)     
        img_path = filepath + '/' + str(camera_name) + '_' + str(day) + '_' + str(month) + '_' + str(year) + '_' + str(year) + '_' + str(hour) + '_' + str(minute) + '_' + str(second) + '.jpeg'
        print(img_path)
        
        if os.path.exists(filepath):
            img.save(img_path)
        else:
            os.mkdir(filepath)
            img.save(img_path)
        
        if email:
            detection_data = {
                "camera_name": camera_name,
                "datetime": datetime_str,
            }
            self.db_email.update_one(
                {"email": email},
                {"$push": {"detections": detection_data}},
                upsert=True
            )
        
                
# app = MonitoringWindow()