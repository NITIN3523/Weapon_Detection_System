from tkinter import ttk, messagebox
import tkinter.font as tkFont
from UI.settingWindow import SettingWindow
import pymongo
import webbrowser
import bcrypt


class LoginWindow():
    def __init__(self,root):
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client.Weapon_Detection_Alert_Info
        self.db_email = db.users
        
        self.root = root
        self.center_window()
        self.root.title('Weapon Detection Login')
        self.root.resizable(0,0)
        self.root.iconbitmap(False,'Client_Side/transparent.ico')
        custom_font = tkFont.Font(family="Helvetica", size=12)

        self.sys_name = ttk.Label(root,text='Weapon Detection System',font=tkFont.Font(size=12,family="Helvetica"))
        
        self.username = ttk.Label(root, text='Email:',font=tkFont.Font(size=12,family="Helvetica"))        
        self.username_entry = ttk.Entry(root, width=26, font=custom_font)
        
        self.password = ttk.Label(root, text='Password:',font=tkFont.Font(size=12,family="Helvetica"))
        self.password_entry = ttk.Entry(root, width=26, font=custom_font, show='*')

        s = ttk.Style()
        s.configure('login_btn.TButton', font=("Helvetica",11))
        self.login_button = ttk.Button(root, text='Login',width=28, style='login_btn.TButton',command = self.open_monitor_page)
        
        s.configure('register_btn.TButton', font=("Helvetica",11))
        self.register_button = ttk.Button(root, text='Register',width=28,style='register_btn.TButton',command = self.get_register_page)

        self.sys_name.place(x=60, y=20)
        self.username.place(x=30, y=70)  
        self.username_entry.place(x=30, y=100)
        self.password.place(x=30,y=130)
        self.password_entry.place(x=30, y=160)
        self.login_button.place(x=37, y=210)
        self.register_button.place(x=37, y=240)    
    
    def get_register_page(self):
        """Open the Flask register page by running the Flask app."""
        try:
            # Assuming app.py is in the same directory as this script
            # subprocess.Popen(['python', 'Server_Side/app.py'], cwd=os.getcwd())
            webbrowser.open('http://127.0.0.1:5000/')
            print('Flask app started successfully.')
        except Exception as e:
            print(f"Failed to start the Flask app: {e}")
            
        
    def hide_widgets(self):
        self.sys_name.place_forget()
        self.username.place_forget()
        self.username_entry.place_forget()
        self.password.place_forget()
        self.password_entry.place_forget()
        self.login_button.place_forget()
        self.register_button.place_forget() 
        
        
    def check_password(self,hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def open_monitor_page(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db_email.find_one({'email':email})
        if user and self.check_password(user['password'],password):
            self.hide_widgets()
            self.settingWindow = SettingWindow(self.root)
        else:
            messagebox.showerror('error','Inavalid Credantial.')


    def center_window(self):
        window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 300) // 2
        window.geometry(f"300x300+{x}+{y}")




