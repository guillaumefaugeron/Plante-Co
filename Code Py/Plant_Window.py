from tkinter import *

"------------------------- CONSTANTS -------------------------------"
PLANT_NAME_INDEX = 0                        #Definition of the index's value in the csv file                     
PLANT_TEMPERATURE_INDEX = 1 
PLANT_AIR_HUMIDTY_INDEX = 2
PLANT_GROUND_HUMIDTY_INDEX = 3
PLANT_LUMINOSITY_INDEX = 4

database_plant_name = "LocalDB.csv"            #Path of the local DB
"------------------------- FUNCTIONS -------------------------------"
def FillPlantListBox(plants):                
    global plant_datas
    global plant_list
    
    plant_datas = plants
    for plant in plants:
        plant_list.insert(END, plant[PLANT_NAME_INDEX])

def ReadPlantData(file_name, separator):
    global plant_datas
    
    plant_datas = []                    #Reading in theDb and putting the values in a table
    with open(file_name, "r") as f:
        for elem in f.read().split("\n"):
            if(elem != ""):
                plant_datas.append(elem.split(separator))
        
def OnListChange(evt):
    global plant_datas
    DisplayOptimalPlantData(plant_datas[plant_list.curselection()[0]])

def OnEntrySearch(evt=None):
    global search_entry                 #Name plant that the user wants to find in the DB 
    global plant_datas                  
    
    search_value = search_entry.get()
    if(search_value == ""):             #Verifing if the fieeld is empty 
        return
    
    searched_plant=None
    for plant in plant_datas:           #Searching the name of the plant in the DB
        if(plant[PLANT_NAME_INDEX] == search_value):
            searched_plant=plant
            
    if(searched_plant != None):                      
        DisplayOptimalPlantData(searched_plant)
    else:                               
        from tkinter import messagebox  #Printing a message error if the plant is not find
        messagebox.showwarning("Error", "The plant " + search_value + " n'a pas été trouvé")

def DisplayCurrentPlant():
    global current_temp_value_label
    global current_humi_air_value_label
    global current_humi_sol_value_label
    global current_lumi_value_label
    global window
    
    from main import GetPlantData
    from main import ressources
    datas = GetPlantData()  
    
    plant_temp = datas[0]["out"][ressources[0]]         #reading the data from thinger.io, by requesting data to thinger.io's API 
    plant_humi_air = datas[1]["out"][ressources[1]]
    plant_humi_sol = datas[2]["out"][ressources[2]]
    plant_lumi = datas[3]["out"][ressources[3]]

    current_temp_value_label.config(
        text=str(plant_temp),
        fg="red" if (plant_temp=="error" or plant_temp=="Attention un capteur est débranché") else "#000fff000"         #returning an alert if a captor is unplug
        )
    current_humi_air_value_label.config(
        text=str(plant_humi_air),
        fg="red" if (plant_humi_air=="error" or plant_humi_air=="Attention un capteur est débranché") else "#000fff000"  #returning an alert if a captor is unplug
        )
    current_humi_sol_value_label.config(
        text=str(plant_humi_sol),
        fg="red" if (plant_humi_sol=="error" or plant_humi_sol=="Attention un capteur est débranché") else "#000fff000" #returning an alert if a captor is unplug
        )
    current_lumi_value_label.config(
        text=str(plant_lumi),
        fg="red" if (plant_lumi=="error" or plant_lumi=="Attention un capteur est débranché") else "#000fff000"         #returning an alert if a captor is unplug
        )
    window.after(30000, DisplayCurrentPlant)

def DisplayOptimalPlantData(plant):
    global optimal_temp_value_label
    global optimal_hair_value_label
    global optimal_hsol_value_label
    global optimal_lumi_value_label

    optimal_temp = plant[PLANT_TEMPERATURE_INDEX]
    optimal_temp_value_label.config(text=str(optimal_temp) + "°")

    optimal_hair = plant[PLANT_AIR_HUMIDTY_INDEX]
    optimal_hair_value_label.config(text=str(optimal_hair) + "%")

    optimal_hsol = plant[PLANT_GROUND_HUMIDTY_INDEX]
    optimal_hsol_value_label.config(text=str(optimal_hsol) + "/550")

    optimal_lumi = plant[PLANT_LUMINOSITY_INDEX]
    optimal_lumi_value_label.config(text=str(optimal_lumi) + "lux")

    
def Return():
    window.destroy()
    from Login_Menu import OpenWindow as OpenLoginMenu
    OpenLoginMenu()


def OpenWindow():
    global window
    window = Tk()
    window.title("Plant searcher")
    window.minsize(400, 400)
    window.resizable(0, 0)
    window.iconbitmap("PlanteCo.ico")
    window.configure(background="#e94e6d")
    window.minsize(600, 600)

    plant_list_frame = Frame(window)
    plant_list_frame.place(relx=0.1, rely=0.1, anchor=NW)

    plant_list_scrollbar = Scrollbar(plant_list_frame, orient="vertical")
    
    global plant_list
    plant_list = Listbox(plant_list_frame, yscrollcommand=plant_list_scrollbar.set)
    plant_list.bind("<<ListboxSelect>>", OnListChange)
    plant_list.pack(side=LEFT)

    plant_list_scrollbar.config(command=plant_list.yview)
    plant_list_scrollbar.pack(side=RIGHT, fill=Y)

    search_entry_title = Label(window, text="Entrer le nom de votre plante:", bg="#23b2a4", fg="#FFFFFF")
    search_entry_title.place(relx=0.55, rely=0.13, anchor=W)

    return_button = Button(window, text="Return", width=20, height=4, command=Return, fg="red")
    return_button.place(relx=0.7, rely=0.435, anchor=CENTER)

    
    global search_entry
    search_entry = Entry(window)
    search_entry.bind("<Return>", OnEntrySearch)
    search_entry.place(relx=0.55, rely=0.2, anchor=W)

    search_validate_button = Button(window, text="Valider", command=OnEntrySearch, bg="#23b2a4", fg="#FFFFFF")
    search_validate_button.place(relx=0.7, rely=0.3, anchor=CENTER)

    optimal_condition_frame = Frame(window)
    optimal_condition_frame.place(relx=0.25, rely=0.75, anchor=CENTER)
    optimal_condition_frame.configure(background="#23b2a4")
    
    optimal_condition_label = Label(optimal_condition_frame, text="Condition optimal de la plante", bg="#23b2a4", fg="#FFFFFF")
    optimal_condition_label.pack()

    optimal_temp_label = Label(optimal_condition_frame, text="Température", bg="#23b2a4", fg="#FFFFFF")
    optimal_temp_label.pack()

    global optimal_temp_value_label
    optimal_temp_value_label = Label(optimal_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    optimal_temp_value_label.pack()

    optimal_hair_label = Label(optimal_condition_frame, text="Humidité de l'air", bg="#23b2a4", fg="#FFFFFF")
    optimal_hair_label.pack()

    global optimal_hair_value_label
    optimal_hair_value_label = Label(optimal_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    optimal_hair_value_label.pack()

    optimal_hsol_label = Label(optimal_condition_frame, text="Humidité du sol", bg="#23b2a4", fg="#FFFFFF")
    optimal_hsol_label.pack()

    global optimal_hsol_value_label
    optimal_hsol_value_label = Label(optimal_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    optimal_hsol_value_label.pack()

    optimal_lumni_label = Label(optimal_condition_frame, text="Luminosité", bg="#23b2a4", fg="#FFFFFF")
    optimal_lumni_label.pack()

    global optimal_lumi_value_label
    optimal_lumi_value_label = Label(optimal_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    optimal_lumi_value_label.pack()

    current_condition_frame = Frame(window)
    current_condition_frame.place(relx=0.7, rely=0.75, anchor=CENTER)
    current_condition_frame.configure(background="#23b2a4")

    current_condition_label = Label(current_condition_frame, text="Condition actuel de la plante connecté", bg="#23b2a4", fg="#FFFFFF")
    current_condition_label.pack()

    current_temp_label = Label(current_condition_frame, text="Temperature", bg="#23b2a4", fg="#FFFFFF")
    current_temp_label.pack()

    global current_temp_value_label
    current_temp_value_label = Label(current_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    current_temp_value_label.pack()

    current_humidity_air_label = Label(current_condition_frame, text="Humidité de l'air", bg="#23b2a4", fg="#FFFFFF")
    current_humidity_air_label.pack()

    global current_humi_air_value_label
    current_humi_air_value_label = Label(current_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    current_humi_air_value_label.pack()

    current_humidity_sol_label = Label(current_condition_frame, text="Humidité du sol", bg="#23b2a4", fg="#FFFFFF")
    current_humidity_sol_label.pack()

    global current_humi_sol_value_label
    current_humi_sol_value_label = Label(current_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    current_humi_sol_value_label.pack()

    current_lumi_label = Label(current_condition_frame, text="Luminosité", bg="#23b2a4", fg="#FFFFFF")
    current_lumi_label.pack()

    global current_lumi_value_label
    current_lumi_value_label = Label(current_condition_frame, text="0°", bg="#23b2a4", fg="#FFFFFF")
    current_lumi_value_label.pack()

    global logo_image
    logo_image = PhotoImage(file="logo.png")
    
    global logo
    logo = Button(window, image=logo_image, width=80, height=108,command=None)
    logo.place(relx=0.92, rely=0.1, anchor=CENTER)

    ReadPlantData(database_plant_name, ";") #the reader separator is ;
    FillPlantListBox(plant_datas)
    
    DisplayCurrentPlant()
    window.mainloop()

