import tkinter as tk
import sys
from UI.loginWindow import LoginWindow

main_application = tk.Tk()

mainwindow = LoginWindow(main_application)

main_application.mainloop()

try:
    sys.exit(main_application.exec_())  
except:
    print('Exiting')        