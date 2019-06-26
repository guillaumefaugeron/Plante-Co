import requests     
import json

from Login_Menu import OpenWindow as OpenLoginMenu      #Open the login menu

"------------------------- FUNCTIONS -------------------------------"
def Connection(username, password):
    global api_json
    
    mydata["username"] = username
    mydata["password"] = password

    try:
        api_json = requests.post(url+para, data=mydata).json() #requesting the token to thinger.io in order to be connect
    except:
        return "Delai d'attente dépasser"

    if("error" in api_json):
        return "wrong username / password"
    else:
        return "succes"

def GetDevices():
    global api_json
    global mydata
    global url

    device_para = "v1/users/" + mydata["username"] + "/devices?authorization=" + api_json["access_token"] #requesting the list of the devices, using the valid token generated before

    main_url = url + device_para
    return requests.get(main_url, params=mydata).json()     #Return a json table wtith the list of devices in

def SetDevice(device):
    global device_name
    device_name = device

def GetPlantData():
    global api_json
    global mydata
    global url
    global device_name
    global ressources

    datas = []
    for ressource in ressources:
        print(datas)
        try:
            final_url = url + "v2/users/" + mydata["username"] + "/devices/" + device_name + "/" + ressource + "?authorization=" + api_json["access_token"]#requesting the ressources stream on thinger.io by the arduino card
            value = requests.get(final_url).json()
            if value["out"][ressource] != -1:               #Check if the arduino card has stream an message error
                datas.append(value)
            else:
                datas.append({"out":{ressource:"Veuillez rebrancher le capteur !!"}})
        except:
            datas.append({"out":{ressource:"error"}})
    return datas

"------------------------- VALUES -------------------------------"
mydata = {  #data define the connection parameters 
        "Content-Type" : "application/x-www-form-urlencoded",
        "grant_type" : "password",
        "username" : "",
        "password" : ""
     }

url = "https://api.thinger.io/"
para = "oauth/token"

device_name = ""
ressources = ["DHT11Cel", "DHT11Hum","SoilMoistureV1.0" ,"APDS9301" ] #defining the name of the resources witch have been stream on thinger.io

"------------------------- MAIN -------------------------------"
if(__name__ == "__main__"):
    OpenLoginMenu()
