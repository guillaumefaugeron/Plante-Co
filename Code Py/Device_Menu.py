from tkinter import *

"------------------------- CONSTANTS -------------------------------"



"------------------------- FUNCTIONS -------------------------------"
def Validate():
    global devices_list
    global devices
    global window
    
    device_name = devices_list.get(devices_list.curselection()) #getting the devices list
    
    if(PullDeviceUpdates() == -1):
        UpdateDeviceList()
        loading_label.config(text="request time out")
        loading_label.placeplace(relx=0.2, rely=0.62, anchor=W)
        loading_label.after(3000, loading_label.place_forget)
        return
    
    for device in devices:
        if(device["device"] == device_name):
            if(device["connection"]["active"] == True):            #if the device is connected switch to the plant menu
                window.destroy()
                from main import SetDevice
                SetDevice(device_name)
                from Plant_Menu import OpenWindow as OpenPlantMenu
                OpenPlantMenu()
            else:
                loading_label.config(text="Le device selectionné est déconnecté", fg="red", font=("Courier", 14))
                loading_label.place(relx=0.2, rely=0.62, anchor=W)
                loading_label.after(3000, loading_label.place_forget)

def Return():
    window.destroy()
    from Login_Menu import OpenWindow as OpenLoginMenu          #return to the login menu
    OpenLoginMenu()

def OnListChange(evt=None):
    global cur_device_label
    global cur_device__status_label
    global devices
    
    device_name = devices_list.get(devices_list.curselection())
    loading_label.config(text="Loading device " + device_name)
    loading_label.place(relx=0.2, rely=0.62, anchor=W)
    
    state_color = "red"
    device_state = "Inactive"

    for device in devices:                                          #checking for the devices status, and changing the color if the state change after a refresh
        if("device" in device and device["device"] == device_name):
            state_color = "#23b2a4" if device["connection"]["active"] else "red"     
            device_state = "Active" if device["connection"]["active"] else "Inactive"
    
    cur_device_label.config(text="- " + device_name)
    cur_device__status_label.config(text=device_state, fg=state_color)

    loading_label.place_forget()

def PullDeviceUpdates():
    try:
        global devices
        from main import GetDevices
        devices = GetDevices()
        return 0
    except requests.exceptions.ConnectionError:
        #time out
        return -1

def UpdateDeviceList():
    global cur_device_label
    global cur_device__status_label
    global loading_label
    global devices_list
    global devices
                                                                    #updating the devices list

    PullDeviceUpdates()
    loading_label.config(text="Loading list")
    loading_label.place(relx=0.2, rely=0.62, anchor=W)
    
    if(len(devices) == 0):
        loading_label.config(text="Error, no devices found")        #if there is no devices, print an error

    devices_list.delete(0, END)
    for device in devices:
        devices_list.insert(END, device["device"])                  #inserting devices in the choice list

    loading_label.place_forget()

def OpenWindow():
    global window
    window = Tk()
    window.wm_title("Devices")              #window name
    window.resizable(0,0)                   #the window cant be resized
    window.iconbitmap("PlanteCo.ico")          #icon on the left top
    window.configure(background="#e94e6d")  #background color
    window.minsize(600, 600)                #window resolution
    
    devices_list_frame = Frame(window)
    devices_list_frame.place(relx=0.1, rely=0.1, anchor=NW)

    devices_list_label = Label(devices_list_frame, text="Devices")
    devices_list_label.pack(side=TOP)
    
    devices_list_scrollbar = Scrollbar(devices_list_frame, orient="vertical")
    devices_list_scrollbar.pack(side=RIGHT, fill=Y)

    global devices_list
    devices_list = Listbox(devices_list_frame, yscrollcommand=devices_list_scrollbar.set, fg="#FFFFFF",bg="#23b2a4" )
    devices_list_scrollbar.config(command=devices_list.yview)
    devices_list.pack(side=LEFT)
    
    devices_list.bind("<<ListboxSelect>>", OnListChange)
    
    cur_device_title = Label(window, text="Current device:", fg="#FFFFFF",bg="#23b2a4")
    cur_device_title.place(relx=0.6, rely=0.2, anchor=W)

    global cur_device_label
    cur_device_label = Label(window, text="- ",fg="#FFFFFF",bg="#23b2a4")
    cur_device_label.place(relx=0.6, rely=0.25, anchor=W)

    cur_device_status_title = Label(window, text="Status:",fg="#FFFFFF",bg="#23b2a4")
    cur_device_status_title.place(relx=0.6, rely=0.4, anchor=W)

    global cur_device__status_label
    cur_device__status_label = Label(window, text="Inactive", fg="red")
    cur_device__status_label.place(relx=0.6, rely=0.45, anchor=W)

    validate_button = Button(window, text="Validate", width=20, height=4, command=Validate, fg="#23b2a4")
    validate_button.place(relx=0.3, rely=0.8, anchor=CENTER)

    return_button = Button(window, text="Return", width=20, height=4, command=Return, fg="red")
    return_button.place(relx=0.7, rely=0.8, anchor=CENTER)

    global refresh_image
    refresh_image = PhotoImage(file="refresh.png")


    global logo_image
    logo_image = PhotoImage(file="logo.png")
    
    global logo
    logo = Button(window, image=logo_image, width=80, height=108,command=None)
    logo.place(relx=0.92, rely=0.1, anchor=CENTER)

    global refresh_button
    refresh_button = Button(window, image=refresh_image, width=25, height=25, command=UpdateDeviceList)
    refresh_button.place(relx=0.14, rely=0.62, anchor=CENTER)

    global loading_label
    loading_label = Label(window, text="loading...")
    loading_label.place(relx=0.2, rely=0.62, anchor=W)

    

    if(PullDeviceUpdates() == -1):
        loading_label.config(text="request time out")
        loading_label.after(3000, loading_label.place_forget)
    UpdateDeviceList()
