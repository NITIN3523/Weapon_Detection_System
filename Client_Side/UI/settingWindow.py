from tkinter import ttk
import tkinter.font as tkFont
from UI.monitoringWindow import MonitoringWindow,set_camera_name
from UI.monitoringWindow import set_email

class SettingWindow():
    def __init__(self,root):
        
        self.root = root                
        self.center_window()
        self.root.title('Weapon Detection Setting')
        self.root.resizable(0,0)
        self.root.iconbitmap(False,'Client_Side/transparent.ico')
        custom_font = tkFont.Font(family="Helvetica", size=12)

        self.sys_name = ttk.Label(self.root,text='Enter camera location and email address',font=tkFont.Font(size=12,family="Helvetica"),wraplength=280)
        
        self.cameralocation = ttk.Label(self.root, text='Camera Location:',font=tkFont.Font(size=12,family="Helvetica"))        
        self.cameralocation_entry = ttk.Entry(self.root, width=26, font=custom_font)
        
        self.Mblnum_mailadd = ttk.Label(self.root, text='Email Address:',font=tkFont.Font(size=12,family="Helvetica"))
        self.Mblnum_mailadd_entry = ttk.Entry(self.root, width=26, font=custom_font)

        s = ttk.Style()
        s.configure('monitoring_btn.TButton', font=("Helvetica",11))
        self.monitor_button = ttk.Button(self.root, text='Start Monitoring',width=28, style='monitoring_btn.TButton',command = self.open_settingWindow)

        self.sys_name.place(x=20, y=20)
        self.cameralocation.place(x=30, y=80)
        self.cameralocation_entry.place(x=30, y=110)
        self.Mblnum_mailadd.place(x=30,y=140)
        self.Mblnum_mailadd_entry.place(x=30, y=170)
        self.monitor_button.place(x=37, y=230)
    
    def hide_widgets(self):        
        self.sys_name.place_forget()
        self.cameralocation.place_forget()
        self.cameralocation_entry.place_forget()
        self.Mblnum_mailadd.place_forget()
        self.Mblnum_mailadd_entry.place_forget()
        self.monitor_button.place_forget()

    def open_settingWindow(self):
        cameraname = self.cameralocation_entry.get()
        email = self.Mblnum_mailadd_entry.get()
        set_camera_name(cameraname)
        set_email(email)
        monitorwin = MonitoringWindow(self.root)
        
    def center_window(self):
        window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 300) // 2
        window.geometry(f"300x300+{x}+{y}")