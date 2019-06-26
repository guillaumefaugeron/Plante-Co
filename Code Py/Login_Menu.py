from tkinter import *
from time import sleep

"------------------------- FUNCTIONS -------------------------------"
def Login(evt=None):
    username = username_entry.get()     #User entry
    password = password_entry.get()     #User entry
    
    loading_label.config(text="loading...")
    loading_label.place(relx=0.5, rely=0.55, anchor=CENTER)
    
    from main import Connection
    global window
    Logged(Connection(username, password))  #Check if the username and the password are correct

def Logged(logs):
    loading_label.config(text=logs)
    loading_label.place(relx=0.5, rely=0.55, anchor=CENTER)
    loading_label.after(3000, loading_label.place_forget)
    
    global window
    if(logs == "succes"):
        window.destroy()
        from Device_Menu import OpenWindow as OpenDeviceMenu  #switching to the device menu if the user is log in
        OpenDeviceMenu()

def OpenWindow():
    global window
    window = Tk()
    window.minsize(600, 300)    #window resolution
    window.bind("<Return>", Login)
    window.wm_title("Login")
    window.iconbitmap("PlanteCo.ico")
    window.resizable(0,0)       #the window can't be resized
    window.configure(background="#e94e6d")
    username_label = Label(window,fg="#FFFFFF",bg="#23b2a4", anchor=CENTER, text="Username :")
    username_label.place(relx=0.1, rely=0.3, anchor=CENTER)

    global username_entry
    username_entry = Entry(window)
    username_entry.place(relx=0.3, rely=0.3, anchor=CENTER)

    password_label = Label(window,fg="#FFFFFF",bg="#23b2a4", text="Password :")
    password_label.place(relx=0.6, rely=0.3, anchor=CENTER)

    global password_entry
    password_entry = Entry(window)
    password_entry.config(show="*")
    password_entry.place(relx=0.8, rely=0.3, anchor=CENTER)

    login_button = Button(window, text="Login your thinger.io account",fg="#FFFFFF",bg="#23b2a4", command=Login)
    login_button.config(width=40, height=2)
    login_button.place(relx=0.5, rely=0.7, anchor=CENTER)

    global loading_label
    loading_label = Label(window, text="loading...")
